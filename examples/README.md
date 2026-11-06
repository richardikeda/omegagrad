# Executable reuse examples

[Leia em português](README.pt-BR.md)

Run from the repository root after installing the package.

| Command | Demonstration |
|---|---|
| python -m examples.scalar_optimization | Scalar AD and gradient descent on a quadratic |
| python -m examples.tensor_derivatives | Batched gradient and directional curvature checks |
| python -m examples.background_subtraction | Spline background removal from a spatial signal |
| python -m examples.stationary_landscape | Double-well extrema and deterministic basin boundaries |

Each module checks its output against a known analytical result. See the [reuse guide](../docs/en/REUSE_GUIDE.md).
