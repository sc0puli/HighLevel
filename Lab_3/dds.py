import numpy as np

class dds:
    def __init__(self, phase_acc_width, freq_word_width, phase_width, amp_width):
        self.phase_acc_width = phase_acc_width
        self.freq_word_width = freq_word_width
        self.phase_width = phase_width
        self.amp_width = amp_width

    def generate(self, count, freq, phase_offset=0, amp_offset=0):
        phase_acc = 0
        phase_inc = (freq << self.phase_acc_width) // (1 << self.freq_word_width)
        amplitude = (1 << self.amp_width) - 1
        signal = []

        for _ in range(count):
            phase_acc = (phase_acc + phase_inc) % (1 << self.phase_acc_width)
            phase = (phase_acc >> (self.phase_acc_width - self.phase_width)) + phase_offset
            sin_value = amplitude * np.sin(2 * np.pi * phase / (1 << self.phase_width)) + amp_offset
            signal.append(sin_value)

        return signal
