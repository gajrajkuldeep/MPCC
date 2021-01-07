# -*- coding: utf-8 -*-
"""
decryption performed at Superuser

@author: gajraj kuldeep
"""

from Cryptodome.Cipher import Salsa20
import numpy as np
import matplotlib as mp
from fxpmath import Fxp
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
iv=bytes(np.load('SU/iv.npy'))
P_cipher=Salsa20.new(K_p_1 ,iv)
r_cipher=Salsa20.new(K_r_1,iv)
N=512
int_length=16
frac_length=11
prime_number=65537
P=permutation_indexes(N,P_cipher)

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

xx_r=xx_r.reshape(N,)
inverse_perm = np.arange(len(P))[np.argsort(P)]
xx_r=xx_r[inverse_perm]

f2,=mp.pyplot.plot(xx_r,'o',label='Reconstructed signal at SU')
mp.pyplot.legend(handles=[f2])
mp.pyplot.show()
