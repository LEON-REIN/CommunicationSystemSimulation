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
    'f_c1': 10e6,  # '2fsk' ONLY! Lower carrier frequency.
    'f_c2': 20e6,  # '2fsk' ONLY! Higher carrier frequency.

    'B': 20e6,  # Bandwidth
    'fc': 2.4e9,  # Center frequency = 2.4GHz
    'PT': 0.001,  # Transmitting power(W)! Equal to -30dBW or 0dBm.
    'T': 34,  # Celsius degree
    'D': 200,  # Communication distance
}

bfsk = cm.Communication(**config)

'''1. Modulation'''

# Baseband signal and the length of the generated random sequence
baseband_seq, num = bfsk.RandomSequence()
# Plot the baseband signal
# cm.showsignal(bfsk.config['t'], baseband_seq, bfsk.config['f_B'], figure_num=1, tilte='Baseband Signal')

modulated_seq = bfsk.modulation(num, baseband_seq)
# cm.showsignal(bfsk.config['t'], modulated_seq, bfsk.config['f_B'], figure_num=3, tilte='Modulated Signal')

'''2. Transmission'''

received_seq = bfsk.transmitted_to_receiver()
cm.showsignal(bfsk.config['t'], received_seq, bfsk.config['f_B'], figure_num=5, tilte='Received Signal(34℃, 200m)')

'''3. Demodulation'''

demodulation_seq = bfsk.demodulation()


'''4. Calculating Pe'''
