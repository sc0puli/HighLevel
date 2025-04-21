import dds as dds

class Encoder:
    def __init__(self, _dds):
        self.dds = _dds

    def encode(self, sin_amp, sin_freq, sin_amp_offset, sin_phase_offset, code='1011100001000111011110', code_level_len=10):
        encoded_sin = []

        for bit in code:
            amp = sin_amp if bit == '1' else sin_amp / 2
            sin_signal = self.dds.generate(code_level_len, sin_freq, sin_phase_offset, sin_amp_offset)
            sin_signal = [x * amp for x in sin_signal]
            encoded_sin.extend(sin_signal)

        return encoded_sin

class Decoder:
    def decode(self, encoded_sin, code_level_len):
        code = ''
        for i in range(0, len(encoded_sin), code_level_len):
            segment = encoded_sin[i:i + code_level_len]
            avg_amplitude = sum(segment) / code_level_len
            code += '1' if avg_amplitude > 128 else '0'
        return code
