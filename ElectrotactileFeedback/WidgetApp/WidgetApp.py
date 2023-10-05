import sys
import FESDriver as fd

if __name__ == "__main__":
    port = 'COM3'
    baudrate = 38400
    if len(sys.argv) > 1:
        port = sys.argv[1]
    dev = fd.FESDriver(port, baudrate)
    dev.connect()
    # by default, the device does not update the display to preserve battery.
    print("Enabling LCD")
    dev.enable_refresh_lcd()
    #print("Setting channel amplitude")
    #dev.set_channel_amplitude(4, 10)
    #print("Setting channel amplitude and pulsewidth")
    #dev.set_channel_amplitude_pulsewidth(4, 10, 150)
    print("Setting pulsewidth of all channels.")
    dev.set_global_pulsewidth(150)
    print("Setting frequency of all channels.")
    dev.set_global_frequency(20)
    print("Setting amplitude of all channels.")
    dev.set_global_amplitude(15)
    #print("Setting channel pulsewidth")
    #dev.set_channel_pulsewidth(2, 110)
    #print("Setting channel frequency")
    #dev.set_channel_frequency(3, 20)
    print("Resetting device")
    dev.reset()
    dev.disconnect()