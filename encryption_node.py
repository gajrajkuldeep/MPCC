# -*- coding: utf-8 -*-
"""
Sensing and encryption for sensor node 1

@author: gajraj kuldeep
"""

from Cryptodome.Cipher import Salsa20
from Cryptodome.Random import get_random_bytes
import pandas as pd
import numpy as np
import matplotlib as mp
def pick_random(j,stream_cipher):
    """
    Parameters
    ----------
    j : int
        Generates a uniform random number,a, between j to 0 using Salse20. 
    stream_cipher : cipher object
            
    Returns
    -------
    a : int
    """
    encrypted=stream_cipher.encrypt(b'02')
    a=[]
    if encrypted[1]&1:
        a=encrypted[0]+256
    else:
        a=encrypted[0]

    while j<a:
        encrypted=stream_cipher.encrypt(b'03')
        if encrypted[1]&1:
            a=encrypted[0]+256
        else:
            a=encrypted[0]
    return a

def permutation_indexes(N,stream_cipher):
    """
    Parameters
    ----------
    N : int
        length of data.
    stream_cipher : cipher object
    Returns
    -------
    P : list(int)
        permuted index.
    """
    P=np.array(range(N))
    for i in range(N-1,0,-1): 
        k = pick_random(i,stream_cipher)
        temp = P[i]
        P[i]= P[k]
        P[k]=temp
    return P 




K_p_1 = bytes(np.load('keys/K_p_1.npy'))
K_r_1= bytes(np.load('keys/K_r_1.npy'))

iv = get_random_bytes(8)

P_cipher=Salsa20.new(K_p_1,iv)
r_cipher=Salsa20.new(K_r_1,iv)

N=512
meter_numbers=70
N=512 #signal length
M=5*meter_numbers # number of measurements



data_length=N*1 # the number of reading from a smart meter
data_matrix=np.zeros([meter_numbers,data_length])

################### Read smart meter readings ##########################
for i in range(0,meter_numbers):
    file_name='2015/Apt'+str(i+1)+'_2015.csv'
    meter_readings = pd.read_csv(file_name, header=None,index_col=False,usecols=[ 1] )
    data_matrix[i][:]=meter_readings[1][0:data_length]
x=np.zeros([N,1]);
x[0:meter_numbers]=data_matrix[:,[1]]
np.random.shuffle(x)
################### Measurement matrix and sensing #########################

P=permutation_indexes(N,P_cipher)
x_permuted=x[P]

r=[]
for i in range(1,17,1):
    r=r+list(np.ones((16,),dtype=int)*i)+list(np.ones((16,),dtype=int)*-i  )
P1=permutation_indexes(N,r_cipher)
r=np.array(r)
r_permuted=r[P1]

rx_permuted=x_permuted.reshape(N,)*r_permuted

# preshared sensing matrix between cloud and sensor
phi=np.load('phi.npy')
y=phi.dot(rx_permuted.reshape(N,1))

np.save('storage/y.npy', y)
np.save('storage/iv.npy', iv)
f1,=mp.pyplot.plot(x,label='Original signal')

mp.pyplot.legend(handles=[f1])
mp.pyplot.show()
