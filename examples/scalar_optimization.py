"""Optimize a scalar energy with automatic differentiation."""
import math
from omegagrad.engine import Value


def main():
    coordinate = 0.0
    for _ in range(80):
        x = Value(coordinate)
        energy = (x - 3)**2
        energy.backward()
        assert math.isclose(x.grad, 2 * (coordinate - 3), abs_tol=1e-12)
        coordinate -= 0.1 * x.grad
    assert math.isclose(coordinate, 3, abs_tol=1e-7)
    print(f"Minimum coordinate: {coordinate:.8f}")


if __name__ == "__main__":
    main()
