"""
Support for reading Thruk monitoring webinterface data using Thruk Livestatus API.

configuration.yaml

sensor:
 - platform: thruk_livestatus
   name: Friendly name
   host: http[s]://FQDN
   api_key: xxxxxx

"""

import asyncio
import logging
from datetime import timedelta

import aiohttp
import async_timeout
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.entity import Entity

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_API_KEY,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import Throttle

from .const import *

BASE_URL = "{0}/thruk/r/"
_LOGGER = logging.getLogger(__name__)

QUERIES = {
    "service_stats": "hosts?columns=sum(num_services_crit):num_services_crit,sum(num_services_warn):num_services_warn,sum(num_services_unknown):num_services_unknown,sum(num_services_ok):num_services_ok,count(*):host_count",
    "host_stats": "hosts?columns=count(state):count,state",
}

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=15)
DEFAULT_NAME = "Thruk Livestatus"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_PORT, default=80): cv.positive_int,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Add sensors for passed config_entry in HA."""

    session = async_get_clientsession(hass)
    data = ToonBoilerStatusData(
        session, config.get(CONF_HOST), config.get(CONF_API_KEY)
    )
    await data.async_update()

    async_add_entities([ThrukLivestatusStatusSensor(data, config)], True)


# pylint: disable=abstract-method
class ToonBoilerStatusData:
    """Handle Toon object and limit updates."""

    def __init__(self, session, host, api_key):
        """Initialize the data object."""

        self._session = session
        self._url_orig = BASE_URL.format(host)
        self._headers = {"X-Thruk-Auth-Key": api_key}
        self._data = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Download and update data from Livestatus."""

        self._data = {}
        for URI_NAME, URI in QUERIES.items():
            try:
                self._url = self._url_orig + URI
                with async_timeout.timeout(5):
                    response = await self._session.get(self._url, headers=self._headers)
            except aiohttp.ClientError:
                _LOGGER.error("Cannot poll Livestatus using url: %s", self._url)
                return
            except asyncio.TimeoutError:
                _LOGGER.error(
                    "Timeout error occurred while polling Livestatus using url: %s",
                    self._url,
                )
                return
            except Exception as err:
                _LOGGER.error(
                    "Unknown error occurred while polling Livestatus: %s", err
                )
                self._data = None
                return

            try:
                self._data[URI_NAME] = await response.json(
                    content_type="application/json"
                )
                _LOGGER.debug("Data received from Livestatus: %s", self._data)
            except Exception as err:
                _LOGGER.error("Cannot parse data received from Livestatus: %s", err)
                self._data = None
                return

    @property
    def latest_data(self):
        """Return the latest data object."""
        return self._data


class ThrukLivestatusStatusSensor(Entity):
    """Representation of a Thruk Livestatus sensor."""

    def __init__(self, data, config):
        """Initialize the sensor."""
        self._data = data
        self._name = config.get(CONF_NAME)
        self._id = "server_{self._name}"
        self._type = "host"
        self._attr_icon = "mdi:server"
        self._attr_name = "server_{self._name}"
        self._attr_unique_id = f"server_{self._name}"
        self._state = "Online"
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self):
        """Get the latest data and use it to update our sensor state."""

        await self._data.async_update()
        new_data = self._data.latest_data

        if new_data:
            self._state = "Online"
            self._attributes = {}
            for k, v in new_data.items():
                if k == "service_stats":
                    self._attributes[HOST_COUNT] = v["host_count"]
                    self._attributes[NUM_SERVICES_CRIT] = v["num_services_crit"]
                    self._attributes[NUM_SERVICES_WARN] = v["num_services_warn"]
                    self._attributes[NUM_SERVICES_OK] = v["num_services_ok"]
                    self._attributes[NUM_SERVICES_UNKNOWN] = v["num_services_unknown"]
                elif k == "host_stats":
                    for state in v:
                        if state["state"] == "0":
                            self._attributes[HOSTS_UP] = state["count"]
                        elif state["state"] == "1":
                            self._attributes[HOSTS_DOWN] = state["count"]
                        else:
                            self._attributes[HOSTS_UNKNOWN] = state["count"]
                    if not HOSTS_UP in self._attributes:
                        self._attributes[HOSTS_UP] = 0
                    if not HOSTS_DOWN in self._attributes:
                        self._attributes[HOSTS_DOWN] = 0
                    if not HOSTS_UNKNOWN in self._attributes:
                        self._attributes[HOSTS_UNKNOWN] = 0
        else:
            self._state = "Offline"
            _LOGGER.debug("State: %s", self._state)
