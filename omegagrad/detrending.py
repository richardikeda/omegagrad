"""Prime-position-free continuum background, quadrature and spline derivatives."""
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
class Background:
    def __init__(self, horizon, epsilon, samples=1025):
        self.horizon,self.epsilon=horizon,epsilon
        a=2/horizon
        grid=np.unique(np.r_[np.linspace(0,1,samples),np.clip(a+np.sqrt(epsilon)*np.linspace(-16,16,129),0,1),np.clip(1+np.sqrt(epsilon)*np.linspace(-16,0,65),0,1)])
        def integral(z):
            return quad(lambda u: horizon/np.log(u*horizon)*np.log((z-u)**2+epsilon),a,1,points=sorted({float(v) for v in z+np.sqrt(epsilon)*np.array([-64,-8,-1,0,1,8,64]) if a<v<1}),epsabs=1e-7,epsrel=1e-10,limit=250)[0]
        self.spline=CubicSpline(grid,[integral(z) for z in grid])
    def field(self,z,derivative=0):
        return self.spline(z,derivative)
class Residual:
    def __init__(self,universe,background):
        self.universe,self.background=universe,background
    def field(self,z,derivative=0):
        return self.universe.field(z,derivative)-self.background.field(z,derivative)
