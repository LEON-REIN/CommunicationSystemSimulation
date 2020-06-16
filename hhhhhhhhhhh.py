# @.@ coding:utf-8 ^-^
# @Author   : Leon Rein
# @Time     : 2020-06-15  ~  14:05
# @File     : BPSK.py
# @Software : PyCharm
# @Notice   : It's a WINDOWS version!


from CSModel import CommunicationModel as cm
import numpy as np

Pe_list1 = []
SNR_list1 = []
Pe_list2 = []
SNR_list2 = []
T_list = np.arange(23, 35, 1)  # 23~34
D_list = np.arange(50, 201, 10)  # 50~200

myconfig = {
    'Modulation': '2psk',  # '2fsk' or '2psk'
    # f_c1 must > f_B !
    'f_c1': 40e6,  # Lower carrier frequency in '2fsk' or the carrier frequency in '2psk'.
    'f_c2': None,  # '2fsk' ONLY! Higher carrier frequency.
    'B': 20e6,  # Bandwidth
    'fc': 2.4e9,  # Center frequency = 2.4GHz
    'PT': 0.001,  # Transmitting power(W)! Equal to -30dBW or 0dBm.
    'T': 34,  # Celsius degree
    'D': 100,  # Communication distance
}

"""1. Modulation"""
bpsk = cm.Communication(**myconfig)
# Baseband signal and the length of the generated random sequence
baseband_seq = bpsk.RandomSequence(number=5000)

# Plot the baseband signal
# cm.showsignal(bpsk.config['t'], baseband_seq, bpsk.config['f_B'], figure_num=1,
#               tilte='Baseband Signal')

modulated_seq = bpsk.modulation(baseband_seq)
cm.showsignal(bpsk.config['t'], modulated_seq, bpsk.config['f_B'], figure_num=3,
              tilte='Modulated Signal')

"""2. Transmission"""

received_seq = bpsk.transmitted_to_receiver()
cm.showsignal(bpsk.config['t'], received_seq, bpsk.config['f_B'], figure_num=5,
              tilte='Received Signal({T}℃, {D}m)'.format(T=myconfig['T'], D=myconfig['D']))

"""3. Demodulation"""

demodulation_seq, demodulation_seq2 = bpsk.demodulation()
cm.showsignal(bpsk.config['t'], demodulation_seq, bpsk.config['f_B'], figure_num=7,
              tilte='Demodulated Signal')


