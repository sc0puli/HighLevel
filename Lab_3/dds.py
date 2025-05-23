import numpy as np


class DDS:
    """
    Класс, реализующий генератор цифровых дифференциальных сигналов (DDS).

    Этот класс имитирует поведение DDS-чипа, преобразуя входную частоту в выходной сигнал с заданной амплитудой и фазой.
    Использует аккумулятор фазы для хранения информации о фазе сигнала и преобразования ее в амплитуду.
    """

    def __init__(self, phase_accumulator_width, freq_clock, phase_width, amplitude_width, amplitude,
                 amplitude_offset, phase_offset, freq_out):
        """
        Конструктор класса DDS.

        Args:
            phase_accumulator_width (int): Ширина аккумулятора фазы в битах.  Определяет точность хранения фазы.
            freq_clock (float): Частота тактового сигнала в Гц.
            phase_width (int): Ширина выходной фазы в битах. Определяет разрешение фазы.
            amplitude_width (int): Ширина выходной амплитуды в битах.  Определяет разрешение амплитуды.
            amplitude (float): Амплитуда выходного сигнала.
            amplitude_offset (float): Смещение амплитуды выходного сигнала.
            phase_offset (float): Смещение фазы выходного сигнала в градусах.
            freq_out (float): Частота выходного сигнала в Гц

        Raises:
            ValueError: Если freq_clock равна нулю или если phase_accumulator_width, phase_width или amplitude_width не являются положительными целыми числами.

        Attributes:
            phase_accumulator_width (int): Ширина аккумулятора фазы.
            freq_clock (float): Частота тактового сигнала.
            phase_width (int): Ширина выходной фазы.
            amplitude_width (int): Ширина выходной амплитуды.
            freq_out (float):  Частота выходного сигнала.
            amplitude (float): Амплитуда выходного сигнала.
            amplitude_offset (float): Смещение амплитуды выходного сигнала.
            phase_offset (float): Смещение фазы выходного сигнала.
        """

        if freq_clock == 0:
            raise ValueError("Частота тактового сигнала (freq_clock) не может быть равна нулю.")
        if not isinstance(phase_accumulator_width, int) or phase_accumulator_width <= 0:
            raise ValueError(
                "Ширина аккумулятора фазы (phase_accumulator_width) должна быть положительным целым числом.")
        if not isinstance(phase_width, int) or phase_width <= 0:
            raise ValueError("Ширина выходной фазы (phase_width) должна быть положительным целым числом.")
        if not isinstance(amplitude_width, int) or amplitude_width <= 0:
            raise ValueError("Ширина выходной амплитуды (amplitude_width) должна быть положительным целым числом.")

        # Параметризация
        self.phase_accumulator_width = phase_accumulator_width
        self.freq_clock = freq_clock
        self.phase_out_width = phase_width
        self.amp_out_width = amplitude_width
        self.amplitude = amplitude
        self.amplitude_offset = amplitude_offset
        self.phase_offset = phase_offset
        self.freq_out = freq_out

        # Выходные сигналы
        self.phase_accumulator = 0
        self.out_signal = []

        # Внутренняя логика
        # M =  (Fout * 2^n) / Fclk  , M - phase increment value, n - acc bit-width
        self.phase_incr = int((2 ** self.phase_accumulator_width) * self.freq_out / self.freq_clock)

        # degree -> radians
        self.phase_offset_rad = np.deg2rad(self.phase_offset)


    def step(self):
        """
        Генерирует выходной сигнал DDS. Выполняет 1 шаг.

        Returns:
            list: Список амплитуд выходного сигнала.
        """
        # phase truncation
        phase = self.phase_accumulator >> (self.phase_accumulator_width - self.phase_out_width)

        # phase-to-amplitude converter (lookup sin table)
        phase2amp = np.sin(2 * np.pi * (phase) / (2 ** self.phase_out_width) + self.phase_offset_rad)
        amplitude = phase2amp * self.amplitude + self.amplitude_offset

        ## if amplitude is proportional self.amp_out_width
        # amp_max = (2 ** (self.amp_out_width - 1)) - 1
        # amplitude = (phase2amp * self.amplitude + self.amplitude_offset) * amp_max

        # save sample
        self.out_signal.append(amplitude)

        # phase accumulator
        if self.phase_accumulator == 2 ** self.phase_accumulator_width - 1:
            phase_accumulator = 0
        else:
            self.phase_accumulator += self.phase_incr

        return self.out_signal


    def run(self, steps):
        """
        Генерирует выходной сигнал DDS. Выполняет steps шагов.

        Args:
            steps (int): Количество семплов в выходном сигнале.

        Returns:
            list: Список амплитуд выходного сигнала.

        Raises:
            ValueError: Если количество семплов меньше или равно 0.
        """

        for i in range(steps):
            self.step()

        return self.out_signal

