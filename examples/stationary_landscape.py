"""Bracket and refine the extrema of a double-well energy."""
import numpy as np
from omegagrad.phase2 import roots


class DoubleWell:
    def field(self, z, derivative=0):
        if derivative == 0:
            return (z**2 - 1)**2
        if derivative == 1:
            return 4 * z * (z**2 - 1)
        if derivative == 2:
            return 12 * z**2 - 4
        raise ValueError("Expected derivative order 0, 1 or 2")


def main():
    domain = (-2.0, 2.0)
    points = roots(DoubleWell(), np.linspace(*domain, 400))
    np.testing.assert_allclose([p["z"] for p in points], [-1, 0, 1], atol=1e-12)
    assert [p["kind"] for p in points] == ["minimum", "maximum", "minimum"]
    barrier = points[1]["z"]
    print(f"Attractors at -1 and 1. Basin boundaries: {domain[0]}, {barrier:g}, {domain[1]}")


if __name__ == "__main__":
    main()
