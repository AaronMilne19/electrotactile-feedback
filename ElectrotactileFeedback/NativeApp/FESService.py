import atexit
import FESDriver as fes

class FESService:

    #initialise connection to device
    def __init__(self, port='COM3', baudrate=38400):
        self.device = fes.FESDriver(port, baudrate)
        self.device.connect()
        atexit.register(self.disconnect_device)
    
    #disconnect from device
    def disconnect_device(self):
        print("Disconnecting from device")
        self.device.disconnect()

    #Send pulse to the device with the given parameters
    def send_pulse(self, pulsewidth, frequency, amplitude, channels=None):
        if channels is None:
            self.device.set_global_pulsewidth(pulsewidth)
            self.device.set_global_frequency(frequency)
            self.device.set_global_amplitude(amplitude)
        else:
            for channel in channels:
                self.device.set_channel_pulsewidth(channel, pulsewidth)
                self.device.set_channel_frequency(channel, frequency)
                self.device.set_channel_amplitude(channel, amplitude)

        self.device.reset()


    #lookup the params for device based on type of widget being used 
    def lookup_widget_parameters(self, type):
        #TODO: Add some sort of library of parameters which are custom for each widget
        return 100, 20, 10
    
    