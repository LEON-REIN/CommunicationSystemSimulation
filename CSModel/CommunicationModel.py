# @.@ coding:utf-8 ^-^
# @Author   : Leon Rein
# @Time     : 2020-06-12  ~  21:21 
# @File     : CommunicationModel.py
# @Software : PyCharm
# @Notice   : It's a WINDOWS version!
#             I didn't move the center frequency to 2.4GHz after modulation for convenience.


import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import signal


class Communication:
    num_to_show = 6
    figure_num = 1
    fs = 50  # 50*f_B, satisfies the Nyquist criterion.
    d0 = 8  # meter
    c = 3e8  # m/s

    def __init__(self, **config):
        self.randomlist = []  # Random sequence
        self.config = config
        # 'TB' is time width of symbols
        if self.config['Modulation'] == '2fsk':
            self.config['TB'] = 2 / (config['B'] - (config['f_c2'] - config['f_c1']))
        else:
            self.config['TB'] = 2 / self.config['B']
        # Time series. Only to show 'num_to_show' symbols' wave shape.
        self.config['t'] = np.linspace(0, self.num_to_show * self.config['TB'], self.num_to_show * self.fs)
        self.config['f_B'] = 1 / self.config['TB']
        self.config['K'] = self.config['T'] + 273.15

    def RandomSequence(self, number=5000, seed=1):
        """
        number: the length of the random sequence to be generated
        seed: seed of random
        """
        baseband = []
        __list1 = np.ones(self.fs)
        random.seed(seed)  # Make the random sequence the same.
        self.randomlist = [random.randint(0, 1) for i in range(number)]
        # self.randomlist = [0 for i in range(number)]
        for i in range(number):
            baseband = np.append(baseband, self.randomlist[i] * __list1)
        baseband = baseband.astype('int8')
        return baseband, number  # Baseband signal and the length of the generated random sequence

    def __attenuation__(self):

        PL_dB = 20 * np.log10(4 * np.pi * self.config['fc'] * self.d0 / self.c) \
                + 33 * np.log10(self.config['D'] / self.d0)

        PL = 10 ** (PL_dB / 10)
        self.config['received'] = self.config['modulated'] / np.sqrt(PL)
        self.config['PR_s'] = self.config['PT'] / PL  # Or 0.5 * max(self.config['received']) ** 2

    def __awgn__(self):
        __k = 1.38e-23  # J/K
        self.config['PR_n'] = self.config['B'] * self.config['K'] * __k
        self.config['noise'] = np.random.randn(len(self.config['modulated'])) * np.sqrt(self.config['PR_n'])
        self.config['received'] = self.config['received'] + self.config['noise']  # TODO: too powerful noise QwQ

    def modulation(self, number, baseband):
        t = np.linspace(0, self.config['TB'] * number, len(baseband))
        __list1 = np.cos(2 * np.pi * self.config['f_c1'] * t)
        if self.config['Modulation'] == '2fsk':  # keying method
            baseband2 = 1 - baseband
            __list2 = np.cos(2 * np.pi * self.config['f_c2'] * t)
            modulated = __list2 * baseband + __list1 * baseband2
        else:  # keying method
            baseband2 = (baseband - 0.5) * 2  # (0 1 1 0 1 ...) -> (-1 1 1 -1 1 ...)
            modulated = baseband2 * __list1
        # PT(0.001W) == 1/2 * Amp^2, Amp ~=~ 0.0447
        self.config['modulated'] = modulated * np.sqrt(self.config['PT'] * 2)
        # I didn't move the center frequency to 2.4GHz, one for my laziness,
        # another for its not affecting the consequence of 'Lossless' Down-conversion-to-zero.
        return self.config['modulated']

    def transmitted_to_receiver(self):
        self.__attenuation__()
        self.__awgn__()
        return self.config['received']

    def demodulation(self):  # Coherent demodulation TODO: 2fsk & 2psk
        __cut_off = 2 * 1 / self.fs  # Normalized cut-off frequency
        # __b, __a = signal.butter(10, __cut_off, btype='low')  # 10th order IIR LPF named Butterworth
        # self.config['noise'] = signal.filtfilt(__b, __a, self.config['noise'])
        # self.config['received'] = self.config['received'] + self.config['noise']
        # self.config['demodulated'] = self.config['received']
        return self.config['demodulated']

    def calculate_Pe(self):
        self.config['SNR'] = self.config['PR_s'] / self.config['PR_n']
        return self.config['Pe'], self.config['SNR']


def showsignal(t, y, f_B, figure_num=1, tilte='Hello'):
    plt.figure(num=figure_num)
    __fftsize_list = np.array([2 ** i for i in range(20)])
    xticks_list = [r"$%dT_B$" % i for i in range(Communication.num_to_show + 1)]
    plt.xticks(np.linspace(0, t.max(), Communication.num_to_show + 1),
               xticks_list)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude(V)")

    y1 = y[0:Communication.num_to_show * Communication.fs]
    plt.plot(t, y1, 'k')
    plt.title(tilte)
    plt.tight_layout()
    plt.show()

    plt.figure(num=(figure_num + 1))
    __fftsize_list = np.where(__fftsize_list > len(y), 0, __fftsize_list)
    fftsize = max(__fftsize_list)  # Find a number less than len(y) and happened to be 2^N for fft.
    y2 = abs(np.fft.rfft(y[0:fftsize]))
    y2 = y2 / max(y2)  # Amplitude normalization. y2.shape = fftsize(even)/2+1
    freqs = np.linspace(0, 5 * f_B, int(fftsize / 2 + 1))[0:int(10 * len(y2) / Communication.fs)]
    y2 = y2[0:len(freqs)]
    plt.xticks(np.linspace(0, freqs[-1], 6),
               ["0"] + ['%.2f' % (i * f_B / 1e6) for i in range(1, 6)])
    plt.xlabel("Frequency(MHz)")
    plt.ylabel("Normalized Amplitude")
    # print(freqs.shape, )
    plt.plot(freqs, y2, 'k')
    plt.title("FFT Spectrum of " + tilte)
    plt.tight_layout()
    plt.show()
