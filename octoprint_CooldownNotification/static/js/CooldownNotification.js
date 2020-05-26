/*
 * View model for OctoPrint-CooldownNotification
 *
 * Author: George McCauley
 * License: AGPLv3
 */
$(function() {
    function CooldownnotificationViewModel(parameters) {
        var self = this;
		
        // assign the injected parameters, e.g.:
        self.settingsViewModel = parameters[0];
        self.printerStateViewModel = parameters[1];
		//console.log(self.settingsViewModel);
		//console.log(self.printerStateViewModel);

        // TODO: Implement your plugin's view model here.
		var PLUGIN_ID = 'CooldownNotification'
		self.isReady = ko.observable();
		self.inProgress = ko.observable();


		self.onDataUpdaterPluginMessage = function(plugin, data) {
			if (plugin != PLUGIN_ID) {
				console.log("Ignoring Plugin: " + plugin);
				return;
			}

			if(data.action == "popup") {
				new PNotify({
					title: 'Cooldown Notification',
					text: data.text,
					type: data.type,
					hide: true
				});
			}

			if(data.action == "startTimer") {
				console.log("Timer Started");
				self.inProgress(true);
			}

			if(data.action == "doneExecute") {
				console.log("Execution Complete");
				self.inProgress(false);
			}
		}


		self.testNow = function() {
			console.log("Starting Test");
			console.log("Sending GCODE: \n" + $('#settings_plugin_CooldownNotification_GCODE').val())
			
			self.inProgress(true);
			//self.settingsViewModel.saveData();
			
			$.ajax({
				url: API_BASEURL + 'plugin/' + PLUGIN_ID,
				type: 'POST',
				datatype: "json",
				data: JSON.stringify({
					command: "testGCODE",
					GCODE: $('#settings_plugin_CooldownNotification_GCODE').val()
				}),
				contentType: "application/json; charset-UTF-8"
			});
		};


		self.onSettingsShown = function() {
			self.isReady(self.printerStateViewModel.isReady());
			//console.log("isReady: " + self.isReady());
			//console.log("inProgress: " + self.inProgress());
		};
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: CooldownnotificationViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel", "printerStateViewModel"],
        // Elements to bind to, e.g. #settings_plugin_CooldownNotification, #tab_plugin_CooldownNotification, ...
        elements: ["#settings_plugin_CooldownNotification"]
    });
});
