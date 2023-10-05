import serial
import struct
import sys
import time

class FESDriver(object):

    def __init__(self, _port, _baudrate, debug=False):
        self.port = _port
        self.baudrate = _baudrate
        self.debug = debug
        self.is_connected = False
        self.serial = None

    def connect(self):
        if self.is_connected:
            self.disconnect()
        print(
            'opening serial connection to FES stimulator on port {} with baudrate {}'.format(self.port, self.baudrate))
        if self.debug:
            self.serial = SerialStub(self.port, self.baudrate)
        else:
            try:
                self.serial = serial.Serial(self.port, self.baudrate, timeout=5)
            except serial.SerialException as err:
                print("SerialException: {0}".format(err))
                print("Unexpected error:", sys.exc_info()[0])
                return False
        if self.serial.isOpen():
            self.is_connected = True
            return True
        else:
            # this should not be happening
            print('WARNING: Serial port not open despite successful initialisation!')
            return False

    # close serial port if connected
    def disconnect(self):
        if not self.is_connected:
            return
        self.serial.close()
        self.is_connected = False
        self.serial = None

    # send command over serial and wait for response bytes with timeout
    def _send(self, message, min_bytes=4):
        if not self.is_connected:
            print("WARNING: FESDriver disconnected.")
            return
        self._clear_input_buffer()
        self.serial.write(message)
        time.sleep(0.005)
        return self._wait_response(min_bytes=min_bytes)

    # wait for response from serial of length min_bytes from FES device or timeout
    def _wait_response(self, min_bytes=4, timeout=3):
        if not self.is_connected:
            print("WARNING: FESDriver disconnected.")
            return

        tic = time.time()
        num_bytes = 0
        data = []
        while num_bytes < min_bytes:
            toc = time.time()
            if toc - tic > timeout:
                msg = self._clear_input_buffer()
                print("FES:inputError - Incomplete message from FES")
                print(msg)
                break
            if num_bytes < self.serial.in_waiting:
                num_bytes = self.serial.in_waiting
                tic = time.time()
        if num_bytes >= min_bytes:
            data = self._clear_input_buffer()
        return data

    # pop and return all data from serial input buffer
    def _clear_input_buffer(self):
        if not self.is_connected:
            print("WARNING: FESDriver disconnected.")
            return
        data = []
        for i in range(self.serial.in_waiting):
            data.append(self.serial.read(1))
        return data

    """
    OLD FIRMWARE VERSION: DO NOT USE
    
    """

    # read single channel data from FES device
    def read_channels(self, channels):
        if not isinstance(channels, list):
            channels = [channels]
        for c in channels:
            if not (self._check_channel(c)):
                return
        sof = [255, 255]
        bytes_no = len(channels)
        command = 15
        data = [bytes_no, command] + channels
        checksum = (sum(data)) % 256
        message = sof + data + [checksum]
        response_bytes = 4 + 2 * len(channels)
        data = self._send(message, min_bytes=4 + 2 * len(channels))
        if len(data) < response_bytes:
            print("WARNING: read_channels response shorter than expected.")
        for i in range(len(channels)):
            d1 = struct.unpack(">H", data[i * 2] + data[i * 2 + 1])
            data.append(d1[0])
        return data

    """

        NEW FIRMWARE PROTOCOL
    """

    # set the amplitude in mA of one channel
    def set_channel_amplitude(self, channel, amplitude):
        if not self._check_channel or not self._check_amplitude(amplitude):
            return
        byte_no, command, response_bytes = 2, 26, 4
        data = [byte_no, command, channel, amplitude]
        checksum = (sum(data)) % 256
        data = self._send(data + [checksum], min_bytes=response_bytes)
        return data

    def set_channel_frequency(self, channel, frequency):
        if not self._check_channel or not self._check_frequency(frequency):
            return
        byte_no, command, response_bytes = 3, 3, 4
        fq1, fq2 = frequency // 256, frequency % 256
        data = [byte_no, command, channel, fq1, fq2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    def set_channel_pulsewidth(self, channel, pulsewidth):
        if not self._check_channel(channel) or not self._check_pulsewidth(pulsewidth):
            return
        byte_no, command, response_bytes = 3, 7, 4
        pw1, pw2 = pulsewidth // 256, pulsewidth % 256
        data = [byte_no, command, channel, pw1, pw2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    # update amplitude and pulsewidth of a single channel
    def set_channel_amplitude_pulsewidth(self, channel, amplitude, pulsewidth):
        if not self._check_channel(channel) or \
                not self._check_amplitude(amplitude) or \
                not self._check_pulsewidth(pulsewidth):
            return
        bytes_no, command, response_bytes = 4, 1, 4
        pw1, pw2 = pulsewidth // 256, pulsewidth % 256
        data = [bytes_no, command, channel, amplitude, pw1, pw2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    def set_global_amplitude(self, amplitude):
        if not self._check_amplitude(amplitude):
            return
        byte_no, command, response_bytes = 1, 28, 4
        data = [byte_no, command, amplitude]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    def set_global_frequency(self, frequency):
        if not self._check_frequency(frequency):
            return
        byte_no, command, response_bytes = 1, 2, 4
        data = [byte_no, command, frequency]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    # update pulsewidth for all channels
    def set_global_pulsewidth(self, pulsewidth):
        if not self._check_pulsewidth(pulsewidth):
            return
        byte_no, command, response_bytes = 2, 4, 4
        pw1, pw2 = pulsewidth // 256, pulsewidth % 256
        data = [byte_no, command, pw1, pw2]
        checksum = sum(data) % 256
        return self._send(data + [checksum], min_bytes=response_bytes)

    # reset all parameters to startup configuration
    def reset(self):
        byte_no, command, checksum, response_bytes = 0, 32, 32, 2
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # manually refresh LCD to display latest channel settings
    def refresh_lcd(self):
        byte_no, command, checksum, response_bytes = 0, 23, 23, 4
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # by default, the lcd screen does not refresh automatically after each
    # change of parameters to preserve battery. Updates to the LCD screen can
    # be performed manually (see refresh_lcd), or you can activate this globally
    # using enable_refresh_lcd
    def enable_refresh_lcd(self):
        byte_no, command, checksum, response_bytes = 0, 24, 24, 4
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # disables refreshing the screen after parameter updates by default.
    def disable_refresh_lcd(self):
        byte_no, command, checksum, response_bytes = 0, 25, 25, 4
        return self._send([byte_no, command, checksum], min_bytes=response_bytes)

    # get device firmware version
    def read_version(self):
        byte_no, command, checksum, response_bytes = 0, 8, 8, 7
        return self._send([byte_no, command, checksum], min_bytes=2)

    def stimulate(self, tacton):
        print('Stimulating {}'.format(vars(tacton)))
        start = time.time()
        self.set_channel_amplitude_pulsewidth(tacton.channel, tacton.amplitude, tacton.pulse_width)
        self.set_channel_frequency(tacton.channel, tacton.frequency)
        if tacton.duration > 0:
            time.sleep(tacton.duration - (time.time() - start))
            self.stop(tacton)
            return False
        else:
            return True

    def stop(self, tacton=None):
        if tacton is None:
            print("Stopping stimulation on all channels.")
            self.reset()
        else:
            print('Stopping stimulation on channel {}'.format(tacton.channel))
            self.set_channel_amplitude_pulsewidth(tacton.channel, tacton.amplitude, 0)

    @staticmethod
    def _check_channel(channel):
        if (channel < 1) or (channel > 8):
            print("WARNING: channel {} out of range [1, 8].".format(channel))
            return False
        return True

    @staticmethod
    def _check_amplitude(amplitude):
        if (amplitude < -1) or (amplitude > 50):
            print("WARNING: amplitude {} out of range [-1, 50].".format(amplitude))
            return False
        return True

    @staticmethod
    def _check_pulsewidth(pulsewidth):
        if (pulsewidth < 0) or (pulsewidth > 500):
            print("WARNING: pulsewidth {} out of range [0, 500]".format(pulsewidth))
            return False
        return True

    @staticmethod
    def _check_frequency(frequency):
        if (frequency < 0) or (frequency > 100):
            print("WARNING: frequency {} out of range [1, 99]".format(frequency))
            return False
        return True