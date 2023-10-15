import FESDriver as fes

#Send pulse to the device with the given parameters
def send_pulse(pulsewidth, frequency, amplitude, channels=None, port='COM3', baudrate=38400):
    device = fes.FESDriver(port, baudrate)
    device.connect()
    if channels is None:
        device.set_global_pulsewidth(pulsewidth)
        device.set_global_frequency(frequency)
        device.set_global_amplitude(amplitude)
    else:
        for channel in channels:
            device.set_channel_pulsewidth(channel, pulsewidth)
            device.set_channel_frequency(channel, frequency)
            device.set_channel_amplitude(channel, amplitude)

    device.reset()
    device.disconnect()

#lookup the params for device based on type of widget being used 
def lookup_widget_parameters(type):
    return 150, 20, 15