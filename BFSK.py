# @.@ coding:utf-8 ^-^
# @Author   : Leon Rein
# @Time     : 2020-06-12  ~  11:53 
# @File     : BFSK.py
# @Software : PyCharm
# @Notice   : It's a WINDOWS version!


from CSModel import CommunicationModel as cm
from matplotlib import pyplot as plt
import numpy as np

config = {
    'Modulation': '2fsk',  # '2fsk' or '2psk'
    'f_c1': 10e6,  # Lower carrier frequency in '2fsk' or the carrier frequency in '2psk'.
    'f_c2': 20e6,  # '2fsk' ONLY! Higher carrier frequency.

    'B': 20e6,  # Bandwidth
    'fc': 2.4e9,  # Center frequency = 2.4GHz
    'PT': 0.001,  # Transmitting power(W)! Equal to -30dBW or 0dBm.
    'T': 34,  # Celsius degree
    'D': 100,  # Communication distance
}

bfsk = cm.Communication(**config)

'''1. Modulation'''

# Baseband signal and the length of the generated random sequence
baseband_seq = bfsk.RandomSequence()

# Plot the baseband signal
# cm.showsignal(bfsk.config['t'], baseband_seq, bfsk.config['f_B'], figure_num=1, tilte='Baseband Signal')

modulated_seq = bfsk.modulation(baseband_seq)
# cm.showsignal(bfsk.config['t'], modulated_seq, bfsk.config['f_B'], figure_num=3, tilte='Modulated Signal')

'''2. Transmission'''

received_seq = bfsk.transmitted_to_receiver()
# cm.showsignal(bfsk.config['t'], received_seq, bfsk.config['f_B'], figure_num=5,
#               tilte='Received Signal({T}℃, {D}m)'.format(T=config['T'], D=config['D']))

'''3. Demodulation'''

demodulation_seq, demodulation_seq2 = bfsk.demodulation()
# cm.showsignal(bfsk.config['t'], demodulation_seq, bfsk.config['f_B'], figure_num=1, tilte='Demodulated Signal')
# cm.showsignal(bfsk.config['t'], demodulation_seq2, bfsk.config['f_B'], figure_num=3, max_frequency=5,
#               tilte='Demodulated Signal 2')

'''4. Calculating the Pe'''
Pe, SNR = bfsk.calculate_Pe()  # TODO: Pe is easy to get 0 QwQ
