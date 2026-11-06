import math
import numpy as np
import pytest
from omegagrad.engine import Value
from omegagrad.blind_sieve import BlindWave
from omegagrad.detrending import Background,Residual
from omegagrad.universe import ToyUniverse
from omegagrad.phase2 import score

def test_blind_base_and_gradient():
 w=BlindWave(1021)
 assert w.base.tolist()==[2,3,5,7,11,13,17,19,23,29,31]
 for x in [37.2,55.7,100.3]:
  n=Value(x);v=w.autograd(n);v.backward()
  assert n.grad==pytest.approx(float(w.field(x,1)),rel=1e-10)
  h=1e-5
  assert float(w.field(x,2))==pytest.approx(float((w.field(x+h,1)-w.field(x-h,1))/(2*h)),rel=1e-6)
 assert abs(w.field(37,1))>1e-6 # prime does not imply stationary minimum

def test_blind_grid_and_no_truth():
 w=BlindWave(61)
 assert not hasattr(w,'primes')
 assert w.discover()['candidates']==w.discover(.025)['candidates']
 assert score([2,4],[2,3])==dict(tp=1,fp=1,fn=1,precision=.5,recall=.5,f1=.5)

def test_background_consistency():
 u=ToyUniverse(6);b=Background(61,u.epsilon,257);r=Residual(u,b)
 z=.432;h=1e-6
 assert b.field(z,1)==pytest.approx((b.field(z+h)-b.field(z-h))/(2*h),rel=1e-6)
 assert r.field(z)==pytest.approx(u.field(z)-b.field(z))
 assert not hasattr(b,'primes')
