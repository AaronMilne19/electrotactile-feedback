import atexit
from turtle import pu
import FESDriver as fes

class FESService:

    pulsewidth, frequency, amplitude = 0, 0, 0

    #initialise connection to device
    def __init__(self, port='COM3', baudrate=38400):
        self.device = fes.FESDriver(port, baudrate)
        self.device.connect()
        atexit.register(self.disconnect_device)
    
    #disconnect from device
    def disconnect_device(self):
        print("Disconnecting from device")
        self.device.disconnect()
       
    #Setters for the params
    def set_pulsewidth(self, pulsewidth):
        self.pulsewidth = pulsewidth

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude

    #Getters for the params
    def get_pulsewidth(self):
        return self.pulsewidth
    
    def get_frequency(self):
        return self.frequency
    
    def get_amplitude(self):
        return self.amplitude

    #Send pulse to the device with the given parameters
    def send_pulse(self, channels=None):
        print(f"sending pulsewidth:{self.pulsewidth}, frequency:{self.frequency}, amplitude: {self.amplitude}")
        if channels is None:
            self.device.set_global_pulsewidth(self.pulsewidth)
            self.device.set_global_frequency(self.frequency)
            self.device.set_global_amplitude(self.amplitude)
        else:
            for channel in channels:
                self.device.set_channel_pulsewidth(channel, self.pulsewidth)
                self.device.set_channel_frequency(channel, self.frequency)
                self.device.set_channel_amplitude(channel, self.amplitude)

        self.device.reset()
    
    