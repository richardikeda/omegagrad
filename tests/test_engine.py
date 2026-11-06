import math
import pytest
from omegagrad import Value, ToyUniverse


@pytest.mark.parametrize('x', [.2, .8, 1.7, 3.1])
def test_composite_finite_difference(x):
    def f(t):
        return (t.sin()*t.cos() + t.log() + (t/3).exp() + t**2.3 + 2/t)
    node = Value(x)
    out = f(node)
    out.backward()
    h = 1e-5
    numerical = (f(Value(x+h)).data-f(Value(x-h)).data)/(2*h)
    assert node.grad == pytest.approx(numerical, rel=2e-8, abs=1e-8)


def test_shared_graph_repeat_and_deep_chain():
    x = Value(2)
    y = x*x
    z = y*y + y + x
    z.backward()
    assert x.grad == 37
    z.backward()
    assert x.grad == 37
    for _ in range(5000):
        z = z + 1
    z.backward(seed=2)
    assert x.grad == 74


def test_powers_and_domains():
    x, y = Value(2), Value(3)
    z = x**y + 2**x + x**0
    z.backward()
    assert x.grad == pytest.approx(12+4*math.log(2))
    assert y.grad == pytest.approx(8*math.log(2))
    zero = Value(0)
    (zero**0).backward()
    assert zero.grad == 0
    for x in [0, -1]:
        with pytest.raises(ValueError):
            Value(x).log()
    with pytest.raises(ZeroDivisionError):
        Value(1)/0
    with pytest.raises(ValueError):
        Value(-1)**.5


@pytest.mark.parametrize('bits,horizon,count', [(6,61,18),(8,251,54),(10,1021,172),(12,4093,564)])
def test_horizon_and_autograd(bits, horizon, count):
    u = ToyUniverse(bits)
    assert u.p_omega == horizon and len(u.primes) == count
    for z in [.103, .377, .619, .913, 1.0]:
        value, grad = u.value_gradient(z, 'autograd')
        assert value == pytest.approx(u.field(z), rel=1e-13)
        assert grad == pytest.approx(u.field(z,1), rel=1e-11, abs=1e-8)
        h = 1e-7
        numerical_hessian = (u.field(z+h,1)-u.field(z-h,1))/(2*h)
        assert u.field(z,2) == pytest.approx(numerical_hessian, rel=2e-6, abs=.1)


def test_wave_gradient_and_common_multiple():
    u = ToyUniverse(2)  # base 2,3; common period 6
    x = Value(1.4)
    out = u.compute_holographic_wave(x)
    out.backward()
    expected = sum(math.pi/int(p)*math.sin(2*math.pi*1.4/int(p)) for p in u.primes)
    assert x.grad == pytest.approx(expected)
    assert out.data == pytest.approx(u.wave(1.4))
    assert u.wave(6) < 1e-28
    assert u.wave(2) > .1  # wave zeros are not a primality indicator


@pytest.mark.parametrize('bits,eps', [(1,1e-6),(2.5,1e-6),(True,1e-6),(6,0),(6,-1),(6,float('nan'))])
def test_invalid_universe(bits,eps):
    with pytest.raises(ValueError):
        ToyUniverse(bits,eps)
