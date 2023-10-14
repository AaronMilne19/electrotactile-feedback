import FESDriver as fes

#Send pulse to the device with the given parameters
def send_pulse(pulsewidth, frequency, amplitude, port='COM3', baudrate=38400):
    device = fes.FESDriver(port, baudrate)
    device.connect()
    device.set_global_pulsewidth(pulsewidth)
    device.set_global_frequency(frequency)
    device.set_global_amplitude(amplitude)
    device.reset()
    device.disconnect()

#lookup the params for device based on type of widget being used 
def lookup_widget_parameters(type):
    return 150, 20, 15