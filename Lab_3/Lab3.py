import matplotlib.pyplot as plt
import numpy as np
import rx_tx
import dds


if __name__ == '__main__':
    my_dds = dds.DDS(phase_accumulator_width=32,
                 freq_clock=100000,
                 phase_width=15,
                 amplitude_width=10,
                 amplitude=1,
                 amplitude_offset=0,
                 phase_offset=0,
                 freq_out=1000)


    binary_seq = [1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0]
    # samples_per_bit = int((freq_clock / freq_out) * periods_per_bit)
    samples_per_bit = int((100000 / 1000) * 1)
    samples = samples_per_bit * len(binary_seq)

    sin = np.array(my_dds.run(samples))

    # modulation ASK (OOK)
    modulated_signal = rx_tx.modulator(sin, binary_seq, samples_per_bit, 0)

    # demodulation
    demodulated_seq = rx_tx.demodulator(modulated_signal, samples_per_bit)

    print("Исходная последовательность: ", binary_seq)
    print("Демодулированная последовательность:", demodulated_seq)
    print("Совпадение =", demodulated_seq == binary_seq)

    # graphics
    plt.figure(figsize=(10, 10))

    # sin
    plt.subplot(3, 1, 1)
    plt.plot(sin)
    plt.title("Синусоида")
    plt.xlabel("Шаг")
    plt.ylabel("Значенеи амплитуды")
    plt.grid(True)

    # binary sequence
    plt.subplot(3, 1, 2)
    bit_seq = []
    for bit in binary_seq:
        level = int(bit)
        bit_seq.extend([level] * samples_per_bit)
    plt.plot(bit_seq)
    plt.title("Бинарная последовательность")
    plt.grid(True)

    # ASK modulated signal
    plt.subplot(3, 1, 3)
    plt.plot(modulated_signal)
    plt.title("ASK-модулированный сигнал")
    plt.xlabel("Шаг")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.show()