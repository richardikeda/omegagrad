"""Scalar reverse-mode AD. backward() resets the reachable graph by default.

Values must not be mutated between forward and backward. Derivatives are numeric;
this small engine does not construct a graph for higher-order derivatives.
"""
import math
from numbers import Real


class Value:
    __slots__ = ("data", "grad", "_prev", "_backward", "_op")

    def __init__(self, data, _children=(), _op=""):
        self.data = float(data)
        self.grad = 0.0
        self._prev = tuple(_children)
        self._backward = lambda: None
        self._op = _op

    def __repr__(self):
        return f"Value(data={self.data:g}, grad={self.grad:g})"

    @staticmethod
    def _coerce(other):
        if isinstance(other, Value):
            return other
        if not isinstance(other, Real):
            raise TypeError("Expected a real scalar or Value")
        return Value(other)

    def __add__(self, other):
        other = self._coerce(other)
        out = Value(self.data + other.data, (self, other), "+")
        def backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = backward
        return out

    __radd__ = __add__

    def __mul__(self, other):
        other = self._coerce(other)
        a, b = self.data, other.data
        out = Value(a * b, (self, other), "*")
        def backward():
            self.grad += b * out.grad
            other.grad += a * out.grad
        out._backward = backward
        return out

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __truediv__(self, other):
        return self * self._coerce(other)**-1

    def __rtruediv__(self, other):
        return self._coerce(other) * self**-1

    def __pow__(self, exponent):
        if isinstance(exponent, Value):
            return (exponent * self.log()).exp()
        if not isinstance(exponent, Real):
            raise TypeError("Exponent must be real")
        x = self.data
        if x < 0 and not float(exponent).is_integer():
            raise ValueError("Fractional power of a negative real")
        if x == 0 and exponent < 0:
            raise ZeroDivisionError("Negative power of zero")
        if x == 0 and 0 < exponent < 1:
            raise ValueError("Derivative is singular at zero")
        out = Value(x**exponent, (self,), "pow")
        slope = 0.0 if exponent == 0 else exponent * x**(exponent - 1)
        out._backward = lambda: self._accumulate(slope * out.grad)
        return out

    def __rpow__(self, base):
        return self._coerce(base)**self

    def _accumulate(self, amount):
        self.grad += amount

    def _unary(self, data, slope, name):
        out = Value(data, (self,), name)
        out._backward = lambda: self._accumulate(slope * out.grad)
        return out

    def sin(self):
        return self._unary(math.sin(self.data), math.cos(self.data), "sin")

    def cos(self):
        return self._unary(math.cos(self.data), -math.sin(self.data), "cos")

    def log(self):
        if self.data <= 0:
            raise ValueError("log requires x > 0")
        return self._unary(math.log(self.data), 1 / self.data, "log")

    def exp(self):
        y = math.exp(self.data)
        return self._unary(y, y, "exp")

    def backward(self, seed=1.0):
        """Iterative postorder avoids recursion limits on large sums/shared DAGs."""
        topo, visited = [], set()
        stack = [(self, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                topo.append(node)
            elif node not in visited:
                visited.add(node)
                stack.append((node, True))
                stack.extend((p, False) for p in reversed(node._prev))
        for node in topo:
            node.grad = 0.0
        self.grad = float(seed)
        for node in reversed(topo):
            node._backward()
