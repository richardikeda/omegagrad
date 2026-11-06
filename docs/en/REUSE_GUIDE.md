# Reusing OMEGAGRAD numerical components

**Richard Ikeda — Author & Lead Investigator**

The components can support teaching, small nonlinear optimization studies and one-dimensional energy-landscape experiments. Install the package from the repository root. Run examples as modules so imports resolve consistently on Windows, macOS and Linux.

## Scalar differentiation and optimization

`python -m examples.scalar_optimization` minimizes a quadratic potential and checks its exact derivative. Value supports arithmetic, real powers, sin, cos, log and exp. `backward()` resets the reachable graph on each call and accumulates contributions from shared nodes during that call. It calculates numeric first derivatives, not differentiable derivative graphs. Do not mutate data between forward and backward; reconstruct the graph for a new optimization step.

## Batched gradients and directional curvature

`python -m examples.tensor_derivatives` evaluates independent quartic energies. A TensorValue seeded with direction v carries the forward tangent and second directional derivative d²f(x+t*v)/dt². Calling `sum().backward()` gives reverse gradients of the summed outputs. For independent scalar coordinates with unit directions, second directional values are their local second derivatives. For coupled coordinates, they are directional contractions, not the dense Hessian or automatically its diagonal.

Broadcasting is supported for the implemented operations. This compact engine is not a drop-in tensor framework: only documented elementary operators are implemented, and users should validate domains, shapes, conditioning and independent derivative checks for each application. Avoid singular powers, overflow and zero denominators. Chunk large coordinate-by-source matrices; vectorization does not remove their memory cost.

## Background subtraction beyond prime geometry

`python -m examples.background_subtraction` removes a smooth quadratic drift from a synthetic spatial field, preserving a sinusoidal residual and its derivatives. `Residual` accepts any objects implementing `field(z, derivative=0|1|2)`. The example wraps a CubicSpline background and validates all three outputs.

`Background` itself implements the specific prime-density integral; it should not be presented as a universal denoising model. For other physics, derive a physically motivated macroscopic background, integrate or fit it independently, and wrap its values and derivatives using the same protocol. Fitting to the same data can remove the signal of interest or leak targets. Compare interpolation resolutions and preserve the untouched observations.

## Stationary landscapes and basins

`python -m examples.stationary_landscape` maps a double-well energy through `omegagrad.phase2.roots`. The field evaluates arrays; gradient sign changes are detected in a vectorized scan; each bracket is refined by scalar Brent. The original `omegasieve.stationary_points` adds local prime-scale samples and safeguarded Newton polishing, and is specialized to the universe interface. Phase 3 uses a separate batched bisection implementation inside `extended`.

To use the universe-specific bracket/Brent/Newton path, pass a ToyUniverse to the existing locator:

```python
from omegagrad import ToyUniverse
from omegagrad.omegasieve import geometry, stationary_points

universe = ToyUniverse(6)
points = stationary_points(universe, resolution=8)
basin_intervals = geometry(universe)["basins"]
```

The locator evaluates the screening grid in a batch and refines each root separately. The geometry routine compares successive grids and reports their agreement. For generic fields, use the adapter example, refine the grid, compare root catalogs, and report missing/degenerate cases. In one dimension, local maxima delimit attraction basins of gradient flow; momentum/noise changes the dynamical problem. Multiple-dimensional basins require a different method.

## Attribution and licensing

Richard Ikeda is the Author & Lead Investigator. Cite CITATION.cff for scientific reuse. The MIT license permits reuse with its copyright and permission notice. These examples are executable checks, not validation for safety-critical simulation.
