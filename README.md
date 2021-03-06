# Thruk Livestatus

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from Livestatus API.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `thruk_livestatus`.
4. Download _all_ the files from the `custom_components/thruk_livestatus/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
8. In the HA `configuration.yaml` file, add the below lines replacing the name, host and api_key parameters as required"
```
sensor:
  - platform: thruk_livestatus
    name: Friendly Name
    host: http[s]://FQDN
    api_key: xxxxxx
```

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/thruk_livestatus/__init__.py
custom_components/thruk_livestatus/const.py
custom_components/thruk_livestatus/manifest.json
custom_components/thruk_livestatus/sensor.py
```


<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[thruk_livestatus]: https://github.com/KevSex/ha-thruk-livestatus
[buymecoffee]: https://www.buymeacoffee.com/bmac2
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/blueprint.svg?style=for-the-badge
[commits]: https://github.com/KevSex/ha-thruk-livestatus/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/blueprint.svg?style=for-the-badge
[releases]: https://github.com/KevSex/ha-thruk-livestatus/releases
