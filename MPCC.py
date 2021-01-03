# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 19:42:20 2021

@author: Gajraj Kuldeep
"""
# for l1 minimization

import cvxpy as cvx
import numpy as np
import matplotlib as mp

# CS parameters 
N=512 # signal length
M=260 # Number of measurements

K=20 # Saprsity of the signal

# Signal construction
x=np.zeros([N,1])
x[0:K]=np.random.rand(K,1)
np.random.shuffle(x)
# Sensing matrix
phi=np.random.normal(0,1,[M,N])

y=phi.dot(x)

########################### L1 solver ################

xOpt = cvx.Variable((N,1))
obj = cvx.Minimize(cvx.norm(xOpt ,1))
const = [phi@xOpt == y]
prob = cvx.Problem(obj,const)
prob.solve()

######################################################

mp.pyplot.plot(x)
mp.pyplot.plot(xOpt.value,'o')
mp.pyplot.show()
