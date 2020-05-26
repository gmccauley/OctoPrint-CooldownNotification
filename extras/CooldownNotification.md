---
layout: plugin

id: CooldownNotification
title: OctoPrint-CooldownNotification
description: A plugin to execute gcode commands when the print bed cools to a certain temperature
author: George McCauley
license: AGPLv3

date: 2020-05-26

homepage: https://github.com/gmccauley/OctoPrint-CooldownNotification
source: https://github.com/gmccauley/OctoPrint-CooldownNotification
archive: https://github.com/gmccauley/OctoPrint-CooldownNotification/archive/master.zip

tags:
- gcode
- heated bed
- notification
- cooldown

screenshots:
- url: /assets/img/plugins/CooldownNotification/settings.png
  alt: Settings
  caption: Settings

featuredimage: /assets/img/plugins/CooldownNotification/settings.png

compatibility:
  octoprint:
  - 1.4.0
  os:
  - linux
  - windows
  - macos
  - freebsd
  python: ">=3,<4"

---

This plugin is designed to execute gcode commands when the print bed cools to a certain temperature.

The intended usage is to utilize the M300 gcode to alert that the bed has cooled and it's safe to remove prints printed in PETG.
