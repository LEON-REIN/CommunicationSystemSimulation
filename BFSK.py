# @.@ coding:utf-8 ^-^
# @Author   : Leon Rein
# @Time     : 2020-06-12  ~  11:53 
# @File     : BFSK.py
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
    'Modulation': '2fsk',  # '2fsk' or '2psk'
    'f_c1': 10e6,  # Lower carrier frequency in '2fsk' or the carrier frequency in '2psk'.
    'f_c2': 20e6,  # '2fsk' ONLY! Higher carrier frequency.
    'B': 20e6,  # Bandwidth
    'fc': 2.4e9,  # Center frequency = 2.4GHz
    'PT': 0.001,  # Transmitting power(W)! Equal to -30dBW or 0dBm.
    'T': 34,  # Celsius degree
    'D': 100,  # Communication distance
}


def get_result(CM_Model):
    """1. Modulation"""

    # Baseband signal and the length of the generated random sequence
    baseband_seq = CM_Model.RandomSequence(number=5000)

    # Plot the baseband signal
    # cm.showsignal(CM_Model.config['t'], baseband_seq, CM_Model.config['f_B'], figure_num=1,
    #               tilte='Baseband Signal')

    modulated_seq = CM_Model.modulation(baseband_seq)
    # cm.showsignal(CM_Model.config['t'], modulated_seq, CM_Model.config['f_B'], figure_num=3,
    #               tilte='Modulated Signal')

    """2. Transmission"""

    received_seq = CM_Model.transmitted_to_receiver()
    # cm.showsignal(CM_Model.config['t'], received_seq, CM_Model.config['f_B'], figure_num=5,
    #               tilte='Received Signal({T}℃, {D}m)'.format(T=config['T'], D=config['D']))

    """3. Demodulation"""

    demodulation_seq, demodulation_seq2 = CM_Model.demodulation()
    # cm.showsignal(CM_Model.config['t'], demodulation_seq, CM_Model.config['f_B'], figure_num=1,
    #               tilte='Demodulated Signal')
    # cm.showsignal(CM_Model.config['t'], demodulation_seq2, CM_Model.config['f_B'], figure_num=3, max_frequency=5,
    #               tilte='Demodulated Signal 2')

    '''4. Calculating the Pe'''
    Pe, SNR = CM_Model.calculate_Pe()
    return Pe, SNR


"""
Initialization
"""

bfsk = cm.Communication(**myconfig)
# get_result(bfsk)


"""
Question.1
"""

bfsk.config['T'] = 25

for D in D_list:
    bfsk.config['D'] = D
    Pe_, SNR_ = get_result(bfsk)
    Pe_list1.append(Pe_)
    SNR_list1.append(SNR_)

cm.BER_curve('2fsk', 'm', D_list, SNR_list1, Pe_list1, figure_num=3)

"""
Question.2
"""

bfsk.config['D'] = 100

for T in T_list:
    bfsk.config['T'] = T
    Pe_, SNR_ = get_result(bfsk)
    Pe_list2.append(Pe_)
    SNR_list2.append(SNR_)

cm.BER_curve('2fsk', '℃', T_list, SNR_list2, Pe_list2, figure_num=5)
