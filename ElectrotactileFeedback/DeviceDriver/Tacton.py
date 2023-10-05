""" wrapper for channel properties """
class Tacton:
    def __init__(self, channel, amplitude, pulse_width=310, frequency=-1, duration=-1):
        self.channel = channel
        self.amplitude = amplitude
        self.frequency = frequency
        self.duration = duration  # controller stops after n seconds if duration > 0
        self.pulse_width = pulse_width


