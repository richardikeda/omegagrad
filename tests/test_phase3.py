import numpy as np
import pytest
from omegagrad.tensor_engine import TensorValue
from omegagrad.radar import OmegaRadar,miller_rabin_base2,fermat_base2
from omegagrad.blind_sieve import BlindWave

def test_tensor_batch_gradient_hessian():
 w=BlindWave(251);x=np.linspace(40.1,100.1,1000)[:,None];node=TensorValue(x,direction=1)
 out=-((node*(np.pi/w.base)).sin()**2+1e-6).log().sum(axis=1);out.sum().backward()
 assert np.allclose(out.data,w.field(x[:,0]),rtol=1e-10)
 assert np.allclose(node.grad[:,0],w.field(x[:,0],1),rtol=1e-8,atol=1e-7)
 assert np.allclose(out.hessian_direction,w.field(x[:,0],2),rtol=1e-8)

def test_tensor_shared_broadcast():
 x=TensorValue(np.array([[1.],[2.]]),direction=1);b=TensorValue([2.,3.,4.]);y=(x*b+x*x).sum();y.backward()
 assert np.allclose(x.grad[:,0],[15,21]);assert np.allclose(b.grad,[3,3,3])
 y.backward();assert np.allclose(x.grad[:,0],[15,21])

def test_verifier_is_not_certificate():
 assert fermat_base2(341) and not miller_rabin_base2(341)
 assert miller_rabin_base2(2047) # strong pseudoprime: 23*89
 assert not miller_rabin_base2(1)
 assert all(miller_rabin_base2(p) for p in [2,3,5,101,65521])

def test_radar_calibration_reproducible():
 a=OmegaRadar(251);assert a.calibrate()==a.calibrate()
 assert not hasattr(a,'truth')
 assert not any(p in (2,3) for p in a.wave.base)

def test_tensor_potential_batch():
 from omegagrad.tensor_engine import batch_potential
 from omegagrad.universe import ToyUniverse
 from omegagrad.detrending import Background,Residual
 u=ToyUniverse(6);bg=Background(61,u.epsilon,257);z=np.linspace(.1,.9,40)
 v,g,h=batch_potential(z,u.normalized_primes,u.epsilon,bg);r=Residual(u,bg)
 assert np.allclose(v,r.field(z))
 assert np.allclose(g,r.field(z,1))
 assert np.allclose(h,r.field(z,2))
