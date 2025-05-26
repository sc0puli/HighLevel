import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

params = {
    # Параметры сигнала
    'fs': 150, # Частота дискретизации
    'amp': np.random.uniform(low=0.5, high=1.0, size=1), # Амплитуда
    'freq': np.random.uniform(low=10.0, high=20.0, size=1), # Частота
    'noise': np.random.uniform(low=-0.001, high=0.001, size=1000) # Шум
}

if __name__ == '__main__':
    print(f'Частота = {params['freq']}')
    print(f'Амплитуда = {params['amp']}')

    # Генерируем синус: x[n]=A⋅sin(2πfnT+ϕ), fn = freq/fs
    sig_no_noise = params['amp'] * np.sin(2 * np.pi * np.arange(1000) * params['freq'] / params['fs'])

    # Накладываем шум на синус
    sig_noise = sig_no_noise + params['noise']

    plt.plot(sig_noise)
    plt.title('Синусоида во временной области')
    plt.xlabel('Сэмплы')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.show()

    # Синусоида в частотной области в линейном масштабе
    fft_complex = sp.fftpack.fft(sig_noise)
    freqs = np.fft.fftfreq(n=1000, d=1/params['fs'])
    #print(freqs)
    fft_abs = np.abs(fft_complex)
    plt.plot(freqs[:500], fft_abs[:500])
    plt.title('Синусоида в частотной области (линейный масштаб)')
    plt.xlabel('Частота')
    plt.ylabel('Амплисюда')
    plt.grid(True)
    plt.show()

    amp_db = 20 * np.log10(fft_abs + 1e-12)
    plt.plot(freqs[:500], amp_db[:500])
    plt.title('Синусоида в частотной области (логарифмический масштаб)')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.show()

    # Спектр после оконного сглаживания
    window = np.hanning(1000)
    sig_windowed = sig_noise * window
    fft_window_complex = sp.fftpack.fft(sig_windowed)
    fft_window = np.abs(fft_window_complex)

    plt.plot(freqs[:500], fft_window[:500])
    plt.title('Синусоида после оконного сглаживания (линейный масштаб)')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.show()

    amp_db = 20 * np.log10(fft_window + 1e-12)
    plt.plot(freqs[:500], amp_db[:500])
    plt.title('Синусоида после оконного сглаживания (логарифмический масштаб)')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.show()