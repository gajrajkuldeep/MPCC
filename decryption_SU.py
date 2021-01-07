# -*- coding: utf-8 -*-
"""
decryption performed at Superuser

@author: gajraj kuldeep
"""

from Cryptodome.Cipher import Salsa20
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
iv=bytes(np.load('SU/iv.npy'))
P_cipher=Salsa20.new(K_p_1 ,iv)
r_cipher=Salsa20.new(K_r_1,iv)
N=512
P=permutation_indexes(N,P_cipher)
r=[]
for i in range(1,17,1):
    r=r+list(np.ones((16,),dtype=int)*i)+list(np.ones((16,),dtype=int)*-i  )
P1=permutation_indexes(N,r_cipher)
r=np.array(r)
r_permuted=r[P1]

xx=np.load('SU/x_decom.npy')
inv_r=1/r_permuted
xx_r=xx.reshape(N,)*inv_r
inverse_perm = np.arange(len(P))[np.argsort(P)]
f2,=mp.pyplot.plot(xx_r[inverse_perm],'o',label='Reconstructed signal at SU')
mp.pyplot.legend(handles=[f2])
mp.pyplot.show()
