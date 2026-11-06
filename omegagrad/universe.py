"""Finite toy cutoff and the two functionals from the supplied specification.

The executable cutoff is max(primes <= 2**s_bits), NOT an evaluation of K(p)+T(p).
epsilon is a squared distance in normalized coordinates; its width is sqrt(eps).
"""
import math
import numpy as np
from .engine import Value


class ToyUniverse:
    def __init__(self, s_bits: int, epsilon: float = 1e-6):
        if isinstance(s_bits, bool) or not isinstance(s_bits, int) or not 2 <= s_bits <= 20:
            raise ValueError("This in-memory toy laboratory supports integer s_bits in [2,20]")
        if not math.isfinite(epsilon) or epsilon <= 0:
            raise ValueError("epsilon must be finite and strictly positive")
        self.s_bits, self.epsilon = s_bits, float(epsilon)
        self.max_bound = 2**s_bits
        self.primes = self._sieve_primes(self.max_bound)
        self.p_omega = int(self.primes[-1])
        self.normalized_primes = self.primes / self.p_omega

    @staticmethod
    def _sieve_primes(limit):
        sieve = np.ones(limit + 1, dtype=bool)
        sieve[:2] = False
        for p in range(2, math.isqrt(limit) + 1):
            if sieve[p]:
                sieve[p*p::p] = False
        return np.flatnonzero(sieve)

    def compute_potential(self, z: Value) -> Value:
        return sum((((z - float(p))**2 + self.epsilon).log()
                    for p in self.normalized_primes), Value(0))

    def compute_holographic_wave(self, x: Value) -> Value:
        return sum((((math.pi * x / int(p)).sin())**2
                    for p in self.primes), Value(0))

    def value_gradient(self, z, backend="analytic"):
        if backend == "autograd":
            node = Value(z)
            loss = self.compute_potential(node)
            loss.backward()
            return loss.data, node.grad
        if backend != "analytic":
            raise ValueError("backend must be analytic or autograd")
        d = float(z) - self.normalized_primes
        q = d*d + self.epsilon
        return float(np.log(q).sum()), float((2*d/q).sum())

    def field(self, z, derivative=0):
        """Chunked float64 evaluation; derivative 0=L, 1=L', 2=L''."""
        if derivative not in (0, 1, 2):
            raise ValueError("derivative must be 0, 1 or 2")
        a = np.asarray(z, dtype=float)
        flat = a.ravel()
        result = np.empty_like(flat)
        chunk = max(1, 250_000 // len(self.primes))
        for start in range(0, len(flat), chunk):
            d = flat[start:start+chunk, None] - self.normalized_primes
            q = d*d + self.epsilon
            if derivative == 0:
                terms = np.log(q)
            elif derivative == 1:
                terms = 2*d/q
            else:
                terms = 2*(self.epsilon - d*d)/(q*q)
            result[start:start+chunk] = terms.sum(axis=1)
        result = result.reshape(a.shape)
        return float(result) if result.ndim == 0 else result

    def wave(self, x):
        a = np.asarray(x, dtype=float)
        result = (np.sin(np.pi * a[..., None] / self.primes)**2).sum(axis=-1)
        return float(result) if result.ndim == 0 else result
