"""Phase-locked wave radar; calibration uses only small-base labels."""
import math,time
import numpy as np
from scipy.optimize import brentq
from .blind_sieve import BlindWave

def miller_rabin_base2(n):
    n=int(n)
    if n<2:return False
    if n in (2,3):return True
    if n%2==0:return False
    d=n-1;s=0
    while d%2==0:s+=1;d//=2
    x=pow(2,d,n)
    if x in (1,n-1):return True
    for _ in range(s-1):
        x=x*x%n
        if x==n-1:return True
    return False

def fermat_base2(n):
    return n>=2 and pow(2,int(n)-1,int(n))==1

class OmegaRadar:
    def __init__(self,horizon):
        self.wave=BlindWave(horizon);self.small=self.wave.base.copy()
        self.wave.base=self.wave.base[self.wave.base>3]
        self.horizon=horizon
    def features(self,lower,upper):
        # Enumerate brackets within admissible integer cells. No full truth used.
        result=[]
        for n in range(math.ceil(lower),int(upper)+1):
            if n%6 not in (1,5):continue
            grid=n+np.linspace(-.49,.49,9);g=self.wave.field(grid,1)
            for i in np.flatnonzero((g[:-1]<0)&(g[1:]>0)):
                x=brentq(lambda t:float(self.wave.field(t,1)),grid[i],grid[i+1])
                result.append(dict(n=n,x=x,energy=float(self.wave.field(x)),hessian=float(self.wave.field(x,2)),delta=abs(x-n)))
        return result
    def calibrate(self):
        rows=self.features(5,math.isqrt(self.horizon));truth=set(map(int,self.small))
        if not rows:return dict(energy=-math.inf,hessian=0,delta=0,mean=0,status='no_calibration_minima')
        mean=float(np.mean([r['energy'] for r in rows]));best=(-1,None)
        # Training F1 only; deliberately report calibration's distribution shift:
        # small primes divide their own terms, unlike unseen large primes.
        for e in np.quantile([r['energy']-mean for r in rows],[.25,.5,.75,1]):
            for h in np.quantile([r['hessian'] for r in rows],[.25,.5,.75,1]):
                for delta in [.1,.25,.49]:
                    pred={r['n'] for r in rows if r['energy']-mean<=e and r['hessian']<=h and r['delta']<=delta}
                    tp=len(pred&truth);f=2*tp/(len(pred)+len(truth)) if pred else 0
                    if f>best[0]:best=(f,dict(energy=float(e),hessian=float(h),delta=delta,mean=mean,status='small_base_training',train_f1=f))
        return best[1]
    def run(self):
        start=time.perf_counter();threshold=self.calibrate();rows=self.features(math.sqrt(self.horizon)+1e-9,self.horizon)
        candidates=sorted({r['n'] for r in rows if r['energy']-threshold['mean']<=threshold['energy'] and r['hessian']<=threshold['hessian'] and r['delta']<=threshold['delta']})
        return dict(threshold=threshold,features=rows,candidates=candidates,seconds=time.perf_counter()-start)
