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
    'fc': 2.4e9,  # 2.4GHz
    'PT': 0.001,  # Transmitting power(W)! Equal to -30dBW or 0dBm.
}

bfsk = cm.Communication(**config)
baseband = bfsk.RandomSequence()

cm.showsignal(bfsk.config['t'], baseband, bfsk.config['f_B'], figure_num=1, tilte='Baseband Signal')
