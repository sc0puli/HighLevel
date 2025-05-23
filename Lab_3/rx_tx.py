import numpy as np


def modulator(sin, code, samples_per_bit, amp_offset):
    """
    Модулирует сигнал sin на основе заданного кода.

    Args:
        sin (np.ndarray): Входной сигнал.
        code (list): Код модуляции (0 или 1).
        samples_per_bit (int): Количество семплов на бит.
        amp_offset (float): Смещение амплитуды.

    Returns:
        np.ndarray: Модулированный сигнал.
    """

    encoded_sin = np.zeros_like(sin, dtype=float)
    bin_extend = np.repeat(code, samples_per_bit)
    encoded_sin = sin * bin_extend
    encoded_sin = np.where(encoded_sin == 0, amp_offset, encoded_sin)
    return encoded_sin


def demodulator(encoded_sin, samples_per_bit):
    """
    Демодулирует сигнал, модулированный с помощью modulator.

    Args:
        encoded_sin (np.ndarray): Модулированный сигнал.
        samples_per_bit (int): Количество семплов на бит.

    Returns:
        list: Последовательность битов, полученная в результате демодуляции.
    """

    num_bits = len(encoded_sin) // samples_per_bit
    amp_center = np.max(encoded_sin) * 0.5

    demodulated_seq = []

    for i in range(num_bits):
        start = i * samples_per_bit
        end = start + samples_per_bit
        window = encoded_sin[start:end]
        max_amp = np.max(np.abs(window))

        if max_amp > amp_center:
            bit = 1
        else:
            bit = 0

        demodulated_seq.append(bit)

    return demodulated_seq