import time
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np
import scipy.sparse as sc
from scipy.stats import multivariate_normal
import cma
import utils.network
import utils.game
import sys
import os

#dtype = torch.long
dtype = torch.cuda.FloatTensor
torch.device('cuda')



def progtot(mu):
    global dtype
    CMA=cma.evolution_strategy
    sol,es=CMA.fmin2(utils.game.launch_scenarios,mu,0.5,options={'ftarget':-50000,'maxiter':100000,'popsize':5})
    print(sol,es)
    env.close()
    return(es)


if __name__ == "__main__":
    
    try:
        W=np.load('W.npy',allow_pickle=True)
        print('loaded W')
    except FileNotFoundError:
        print('not found creating W')
        Nr,D=512,15
        W=sc.random(Nr,Nr,density=float(D/Nr))
        W=0.9/max(abs(np.linalg.eigvals(W.A)))*W
        W=(2*W-(W!=0))
        W=W.A
        np.save('W.npy',W)
    try :
        net = torch.load('model.pt')
        net.eval()
        print('loaded net')
    except FileNotFoundError:
        print('creating net')
        net=utils.network.initnet(0.9,dtype,W)
        torch.save(net, 'model.pt')
    try:
        mu=np.load('mu.npy',allow_pickle=True)
        print('loaded mu')
    except FileNotFoundError:
        print('not found creating mu')
        mu=np.zeros(3*1025)
        np.save('mu.npy',mu)
    utils.network.dtype=dtype
    utils.game.dtype=dtype
    utils.network.W=W
    #utils.game.env=env
    utils.game.net=net
    progtot(mu)
