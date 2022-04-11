[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

[![hacs][hacsbadge]][hacs]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from API.

{% if not installed %}
## Installation

1. Click install.
2. In the HA `configuration.yaml` file, add the below lines replacing the name, host and api_key parameters as required.

sensor:
  - platform: thruk_livestatus
    name: Friendly Name
    host: http[s]://FQDN
    api_key: xxxxxx

{% endif %}

<!---->

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
[user_profile]: https://github.com/KevSex
