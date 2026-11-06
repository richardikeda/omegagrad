"""Blind stationary-minimum scanner: only the small prime base is available."""
import math
import numpy as np
from scipy.optimize import brentq
from .engine import Value
class BlindWave:
    def __init__(self,horizon,epsilon=1e-6):
        self.horizon,self.epsilon=int(horizon),epsilon
        if horizon<4 or epsilon<=0: raise ValueError('Invalid horizon or epsilon')
        limit=math.isqrt(self.horizon)
        mask=np.ones(limit+1,dtype=bool);mask[:2]=False
        for p in range(2,math.isqrt(limit)+1):
            if mask[p]:mask[p*p::p]=False
        self.base=np.flatnonzero(mask)
    def autograd(self,x):
        return -sum(((math.pi*x/int(p)).sin()**2+self.epsilon).log() for p in self.base)
    def field(self,x,derivative=0):
        t=np.asarray(x)[...,None]*np.pi/self.base;k=np.pi/self.base
        q=np.sin(t)**2+self.epsilon;first=k*np.sin(2*t)
        if derivative==0:r=-np.log(q).sum(axis=-1)
        elif derivative==1:r=-(first/q).sum(axis=-1)
        elif derivative==2:r=((first/q)**2-2*k*k*np.cos(2*t)/q).sum(axis=-1)
        else:raise ValueError('Derivative must be 0,1,2')
        return r
    def discover(self,step=.05):
        # Top-down bracketing of negative-to-positive gradient crossings.
        # No truth, divisibility tests or full prime list in this method.
        lower=math.sqrt(self.horizon)
        grid=np.linspace(lower,self.horizon,math.ceil((self.horizon-lower)/step)+1)
        g=self.field(grid,1);roots=[]
        for i in np.flatnonzero((g[:-1]<0)&(g[1:]>0))[::-1]:
            x=brentq(lambda t:float(self.field(t,1)),grid[i],grid[i+1],xtol=1e-11)
            roots.append(dict(x=x,hessian=float(self.field(x,2)),residual=abs(float(self.field(x,1)))))
        candidates=sorted({round(r['x']) for r in roots if lower<round(r['x'])<=self.horizon},reverse=True)
        return dict(candidates=candidates,minima=roots,step=step)
