# Experimental methodology

**Richard Ikeda — Author & Lead Investigator**

## Phase 1: smoothing and navigation

Four scales (6,8,10,12 bits), two epsilon policies (fixed 1e-6 and inverse-square scaled), and seeds 0,1,2 produce 24 trajectories. A separate 6-bit run computes navigation gradients directly through scalar autograd. The main campaign uses analytical vectorized evaluations, checked against autograd.

Stationary roots are bracketed on grids tied to sqrt(epsilon), refined by Brent and a safeguarded Newton correction. Resolution doubles until successive catalogs agree, subject to a maximum. Sign-change methods can miss tangent or nearly degenerate roots. Residuals and local error estimates are reported; no symbolic exactness or completeness certification is claimed.

Basins are intervals bounded by maxima under deterministic flow dz/dt=-L'(z). The navigator uses momentum 0.5, relative noise 0.02, bounded steps and backtracking. It explicitly transports the state leftward after a capture to cross a barrier. Escape is recorded separately and does not follow from pure gradient descent.

A capture requires small gradient and positive curvature. Only afterward is the integer coordinate rounded, accepted if within 0.25 of the rounded integer and that integer belongs to the reference prime set. Thus minima count, visited wells and recovered-prime coverage are different measurements.

## Phase 2: background and blind wave

Quadrature and cubic spline interpolation approximate the background. Global and edge refinement control numerical sensitivity. The two-feature regression uses log(lambda) and log(abs(barrier Hessian)); comparison uses matched intervals with a unique maximum both before and after subtraction.

For p[k]<p[k+1], lambda=(z*-p[k]/P)/(p[k+1]/P-z*); the target is p[k]-p[k-1]. Training uses the upper 70% in descending spatial order, followed by a one-row embargo and lower-region testing. Targets remain present in the full potential. Scores are retrospective even though coefficient fitting is separated from testing.

The blind wave receives only the horizon and primes up to its square root. Gradient sign changes are scanned top-down and roots refined by Brent. Candidate integers are rounded minima, without divisibility filtering. Truth is used only by the evaluator. Steps 0.05 and 0.025 check candidate stability, not a proof of complete root enumeration.

The removal experiment hides approximately 10% of internal primes using seed 42. It records root shifts and neighbor Hessians. The tested coordinate-recovery rule proposes the midpoint of retained gaps larger than twice their median. This heuristic must not be described as an optimized Hessian-based inverse solver.

## Phase 3: spectral filtering and hybrid verification

Remove 2 and 3 from the logarithmic base. Scan width-0.98 cells centered at integers 6k±1. Extract energy, positive curvature and distance to the integer from stationary minima. Center energy using the calibration-minimum mean. Energy and curvature ceilings are selected from four quantiles; distance cutoffs are 0.1, 0.25 or 0.49. Training F1 is optimized only using small-base labels.

Calibration and target distributions differ structurally: a base prime divides its own phase term, whereas an unseen large prime does not. This is a plausible limitation of the calibration design; the experiment does not isolate it as the sole cause of declining performance.

Apply actual strong Miller–Rabin base 2 to survivors. Fermat base 2 is separately implemented and tested. One base can accept composites, so independent truth remains necessary for precision measurement. Wall-time comparison includes radar and verification, versus direct base-2 Miller–Rabin across all integers. A 6k±1 call-count baseline is also reported. Single-run wall times do not establish hardware-independent speed ratios.

## Extended geometry

At 12,14,16 bits, batched bisection searches central-gap brackets and rejects absent brackets or nonnegative barrier Hessians. Adjacent accepted barriers define relative basin widths. The three-feature regression adds residual-to-original barrier displacement in integer units to log(lambda) and log(abs(H)). The background is recomputed with 4097 global knots plus edge refinement and split integration; integration warnings become errors. The earlier 2049-knot estimates are retained for sensitivity assessment.

KS is a descriptive distance between empirical CDFs; there is no independent-sample p-value interpretation. Selection and normalization can generate apparent distributional stability. No scale-invariance theorem is inferred.
