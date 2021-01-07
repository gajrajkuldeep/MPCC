# -*- coding: utf-8 -*-
"""
decryption performed at Semi-authorized user

@author: gajraj kuldeep
"""

from Cryptodome.Cipher import Salsa20
import numpy as np
import matplotlib as mp
from fxpmath import Fxp

K_r_1= bytes(np.load('keys/K_r_1.npy'))
iv=bytes(np.load('SU/iv.npy'))
r_cipher=Salsa20.new(K_r_1,iv)
N=512
int_length=16
frac_length=11
prime_number=65537

r=np.zeros([N,1],dtype=int)
inv_r=np.zeros([N,1],dtype=int)
for i in range(N):
    r[i]=int.from_bytes(r_cipher.encrypt(b'02'),byteorder='big', signed=False)
    # Fermat's little theorem
    inv_r[i]=pow(int(r[i]),prime_number-2,prime_number)
xx=np.load('SU/x_decom.npy')
xx=np.round(xx).astype(int)
xx_r=np.zeros([N,1],dtype=float)
xx_int=np.zeros([N,1],dtype=int)
for i in range(N):
    xx_int[i]=np.mod(int(inv_r[i])*int(xx[i]),prime_number)
    xx_r[i]=Fxp(hex(int(xx_int[i])),True,int_length,frac_length).get_val(float)
    
f3,=mp.pyplot.plot(xx_r, label='Reconstructed signal at SU')
mp.pyplot.legend(handles=[f3])
mp.pyplot.show()
