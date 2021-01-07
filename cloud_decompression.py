# -*- coding: utf-8 -*-
"""
Cloud decompression

@author: gajraj kuldeep
"""


import numpy as np
import cvxpy as cvx


def l1_minimization(phi,y,N):
    """
    Parameters
    ----------
    phi : matrix float
        MxN size matrix.
    y : column vector, float
        Measurement vector.
    N : int
        signal length.

    Returns
    -------
    xOpt.value : column vector
        Reconstructed sinal.
    """
    xOpt = cvx.Variable((N,1))
    obj = cvx.Minimize(cvx.norm(xOpt ,1))
    const = [phi@xOpt == y]
    prob = cvx.Problem(obj,const)
    prob.solve()
    return xOpt.value



# preshared sensing matrix between cloud and sensor
N=512
phi=np.load('phi.npy')

iv=np.load('storage/iv.npy')
y=np.load('storage/y.npy')

x_decom=l1_minimization(phi,y,N)
np.save('SU/x_decom.npy', x_decom)
np.save('SAU/x_decom.npy', x_decom)
np.save('SU/iv.npy', iv)
np.save('SAU/iv.npy', iv)
