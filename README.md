# OctoPrint-CooldownNotification

This plugin is designed to execute gcode commands when the print bed cools to a certain temperature.

The intended usage is to utilize the M300 gcode to alert that the bed has cooled and it's safe to remove prints printed in PETG.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/gmccauley/OctoPrint-CooldownNotification/archive/master.zip

## Configuration

### Enabled
This can be used to enable/disable the plugin

### Temperature Threshold
Define the temperature for when the GCODE is executed

### GCODE to Execute
The GCODE that is executed when the temperature threshold is reached

## Screenshots
![CooldownNotification](octoprint_CooldownNotification/static/img/settings.png?raw=true)

## Changelog:
### [v0.1.2] - 27 May 2020

**Fixed**
- Threshold saved as string which causes immediate trigging of GCODE after finished print



### [v0.1.1] - 27 May 2020
- Updated Python Compatibility



### [v0.1.0] - 26 May 2020
- Initial Release