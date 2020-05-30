# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
from octoprint.util import RepeatedTimer
import logging
import flask
import threading
import time

class CooldownnotificationPlugin(octoprint.plugin.SettingsPlugin,
                                 octoprint.plugin.StartupPlugin,
                                 octoprint.plugin.AssetPlugin,
                                 octoprint.plugin.TemplatePlugin,
								 octoprint.plugin.SimpleApiPlugin,
								 octoprint.plugin.EventHandlerPlugin):

	def __init__(self):
		self.inProgress = False
		self._TempTimer = None


	##~~ SettingsPlugin
	def get_settings_defaults(self):
		return dict(
			Enabled=False,
			Threshold='40',
			GCODE=""
		)


	##~~ AssetPlugin
	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/CooldownNotification.js"]
		)


	##~~ StartupPlugin
	def on_after_startup(self):
		self.inProgress = False


	##~~ SimpleApiPlugin
	def get_api_commands(self):
		return dict(
			testGCODE=["GCODE"]
		)
	
	def on_api_command(self, command, data):
		if command == "testGCODE":
			if not self.inProgress:
				self._logger.debug("Testing GOCDE")
				thread = threading.Timer(0, self.doExecute,[data['GCODE']])
				thread.start()


	##~~EventHandlerPlugin
	def on_event(self, event, payload):
		if not self.inProgress and self._settings.get(["Enabled"]):
			notify_events = ['PrintFailed', 'PrintDone']
			
			if event in notify_events:
				self._logger.debug("Received Event: " + event)
				self._logger.info("Print Ended, Watching Heatbed Temp")
				self.inProgress = True
				self._plugin_manager.send_plugin_message(self._identifier, dict(action="startTimer"))
				self._TempTimer = RepeatedTimer(5, self.checkTemp, run_first=True)
				self._TempTimer.start()


	##~~Custom Functions
	def checkTemp(self):
		if 'bed' in self._printer.get_current_temperatures():
			bedTemp = self._printer.get_current_temperatures()['bed']['actual']
			threshold = int(self._settings.get(["Threshold"]))
			self._logger.debug("Heatbed Temp: " + str(bedTemp))
			if bedTemp <= threshold:
				self._logger.debug("Heatbed Temp Reached Threshold")
				self._logger.debug("Heatbed Temp: " + str(bedTemp) + "   Type: " + str(type(bedTemp).__name__))
				self._logger.debug("Threshold: " + str(threshold) + "   Type: " + str(type(threshold).__name__))
				self.doExecute(self._settings.get(["GCODE"]))
				self._TempTimer.cancel()

	def doExecute(self, GCODE):
		for line in GCODE.splitlines():
			self._logger.debug("Sending GCODE: " + line)
			self._printer.commands(line)

		self.inProgress = False
		self._plugin_manager.send_plugin_message(self._identifier, dict(action="doneExecute"))
		self._plugin_manager.send_plugin_message(self._identifier, dict(action="popup", type="info", text="Cooldown Notification Sent"))
		self._logger.info("Cooldown Notification Sent")


	##~~ Softwareupdate hook
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			CooldownNotification=dict(
				displayName="Cooldownnotification Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="gmccauley",
				repo="OctoPrint-CooldownNotification",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/gmccauley/OctoPrint-CooldownNotification/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Cooldown Notification"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = CooldownnotificationPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

