"""Subtract an independently specified smooth background from a field."""
import numpy as np
from scipy.interpolate import CubicSpline
from omegagrad.detrending import Residual


class SplineField:
    def __init__(self, coordinates, values):
        self.spline = CubicSpline(coordinates, values)

    def field(self, z, derivative=0):
        return self.spline(z, derivative)


class ObservedField:
    def field(self, z, derivative=0):
        drift = (1 + z**2, 2 * z, np.full_like(z, 2.0))[derivative]
        return drift + 4**derivative * np.sin(4 * z + derivative * np.pi / 2)


def main():
    knots = np.linspace(0, 1, 17)
    background = SplineField(knots, 1 + knots**2)
    residual = Residual(ObservedField(), background)
    z = np.linspace(0, 1, 101)
    for order in range(3):
        expected = 4**order * np.sin(4 * z + order * np.pi / 2)
        np.testing.assert_allclose(residual.field(z, order), expected, atol=1e-10)
    print("Recovered the sinusoidal residual and its first two derivatives")


if __name__ == "__main__":
    main()
