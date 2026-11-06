"""Differentiate independent quartic energies over a coordinate batch."""
import numpy as np
from omegagrad.tensor_engine import TensorValue


def main():
    coordinates = np.linspace(-2, 2, 1025)
    x = TensorValue(coordinates, direction=1)
    energy = (x**2 - 1)**2
    energy.sum().backward()
    np.testing.assert_allclose(x.grad, 4 * coordinates * (coordinates**2 - 1))
    np.testing.assert_allclose(energy.hessian_direction, 12 * coordinates**2 - 4)
    print(f"Validated first and second derivatives at {coordinates.size} coordinates")


if __name__ == "__main__":
    main()
