from FESService import FESService

"""
Class containing methods for handling the various UI events
"""
class EventHandlers(object):

    fes_service = FESService()

    #Prints the key pressed by the user
    def handle_keypress(self, event):
        pulsewidth, frequency, amplitude = self.fes_service.lookup_widget_parameters("key")
        self.fes_service.send_pulse(pulsewidth, frequency, amplitude)

    def handle_button(self):
        pulsewidth, frequency, amplitude = self.fes_service.lookup_widget_parameters("button")
        self.fes_service.send_pulse(pulsewidth, frequency, amplitude)

    def handle_checkbox(self):
        pulsewidth, frequency, amplitude = self.fes_service.lookup_widget_parameters("checkbox")
        self.fes_service.send_pulse(pulsewidth, frequency, amplitude)

    def handle_radio(self):
        pulsewidth, frequency, amplitude = self.fes_service.lookup_widget_parameters("radio")
        self.fes_service.send_pulse(pulsewidth, frequency, amplitude)