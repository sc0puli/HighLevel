import matplotlib.pyplot as plt
import numpy as np

import rx_tx
import dds

if __name__ == '__main__':
    dds = dds.dds(phase_acc_width=32, freq_word_width=10, phase_width=15, amp_width=10)
    sine_signal = dds.generate(1000, 10)

    decoder = rx_tx.Decoder(dds)

    plt.plot(sine_signal)
    plt.show()
    #
    # sin_amp = 127
    # sin_freq = 10
    # sin_amp_offset = 0
    # sin_phase_offset = 0
    # code = '1011100001000111011110'
    # code_level_len = 10
    # #
    #
    # # Кодирование сигнала
    # encoded_signal = encoder(sin_amp, sin_freq, sin_amp_offset, sin_phase_offset, code, code_level_len)
    # #
    # # Декодирование сигнала
    # decoded_code = decoder(encoded_signal, code_level_len)
    #
    # print(f"Original code: {code}")
    # print(f"Decoded code: {decoded_code}")
    # print(f"Match: {decoded_code == code}")