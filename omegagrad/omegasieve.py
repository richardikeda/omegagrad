"""Stationary geometry and controlled top-down potential navigation.

Barriers are 1D maxima, not multidimensional saddles. Roots are numerical, not
symbolically exact. A doubled grid checks stability, not a proof of completeness.
"""
from dataclasses import dataclass, asdict
import math
import numpy as np
from scipy.optimize import brentq
from .universe import ToyUniverse


@dataclass
class StationaryPoint:
    z: float
    kind: str
    gradient_residual: float
    hessian: float
    bracket_width: float
    newton_error_estimate: float


def stationary_points(universe, resolution=8):
    """Bracket sign changes at spacing <= sqrt(eps)/resolution, then Brent.

    Includes prime coordinates and local samples. Degenerate/tangent zeros can
    evade this sign-change method and are not claimed to be certified absent.
    """
    u = universe
    width = math.sqrt(u.epsilon)
    n = max(2048, math.ceil(resolution / width))
    if n > 2_000_000:
        raise ValueError("Root grid exceeds two million samples; use a larger epsilon")
    local = (u.normalized_primes[:, None] + width * np.array([-1, -.5, 0, .5, 1]))
    grid = np.unique(np.clip(np.r_[np.linspace(0, 1, n+1), local.ravel()], 0, 1))
    g = u.field(grid, 1)
    brackets = [(grid[i], grid[i+1]) for i in np.flatnonzero(np.signbit(g[:-1]) != np.signbit(g[1:]))]
    brackets += [(grid[i], grid[i]) for i in np.flatnonzero(g == 0)]
    result = []
    for a, b in brackets:
        z = a if a == b else brentq(lambda x: u.field(x, 1), a, b, xtol=5e-16, rtol=1e-14)
        residual, hessian = u.field(z, 1), u.field(z, 2)
        # One safeguarded Newton polish improves residual in steep narrow wells.
        if hessian:
            candidate = z - residual/hessian
            if a <= candidate <= b and abs(u.field(candidate, 1)) < abs(residual):
                z = candidate
                residual, hessian = u.field(z, 1), u.field(z, 2)
        kind = "minimum" if hessian > 0 else "maximum" if hessian < 0 else "degenerate"
        result.append(StationaryPoint(float(z), kind, abs(float(residual)), float(hessian),
                                     float(b-a), abs(float(residual/hessian)) if hessian else math.inf))
    result.sort(key=lambda p: p.z)
    unique = []
    for p in result:
        if not unique or p.z - unique[-1].z > 1e-12:
            unique.append(p)
    return unique


def geometry(universe, resolution=8):
    u = universe
    coarse = stationary_points(u, resolution)
    used_resolution = resolution
    for _ in range(4):
        used_resolution *= 2
        roots = stationary_points(u, used_resolution)
        stable = len(coarse) == len(roots) and all(
            a.kind == b.kind and abs(a.z-b.z) < 1e-10 for a, b in zip(coarse, roots))
        if stable:
            break
        if used_resolution < 16*resolution:
            coarse = roots
    maxima = [p.z for p in roots if p.kind == "maximum"]
    minima = [p for p in roots if p.kind == "minimum"]
    basin_rows = []
    for point in minima:
        j = int(np.argmin(abs(u.normalized_primes-point.z)))
        lower = max([0.0] + [r for r in maxima if r < point.z])
        upper = min([1.0] + [r for r in maxima if r > point.z])
        left_gap = (u.primes[j]-u.primes[j-1]) if j else math.nan
        right_gap = (u.primes[j+1]-u.primes[j]) if j+1 < len(u.primes) else math.nan
        local_spacing = (left_gap + right_gap) / 2
        basin_rows.append(dict(minimum_z=point.z, nearest_prime=int(u.primes[j]),
            displacement_integer_units=point.z*u.p_omega-int(u.primes[j]),
            lower=lower, upper=upper, width_z=upper-lower,
            width_integer=(upper-lower)*u.p_omega,
            width_over_local_spacing=(upper-lower)*u.p_omega/local_spacing,
            hessian=point.hessian))
    gap_rows = []
    for j, (a, b) in enumerate(zip(u.normalized_primes[:-1], u.normalized_primes[1:])):
        inside = [r for r in maxima if a < r < b]
        z = inside[0] if len(inside) == 1 else math.nan
        gap_rows.append(dict(index=j, lower_prime=int(u.primes[j]), upper_prime=int(u.primes[j+1]),
            gap=int(u.primes[j+1]-u.primes[j]), barrier_count=len(inside), barrier_z=z,
            lambda_asymmetry=(z-a)/(b-z), fraction_from_lower=(z-a)/(b-a),
            next_lower_gap=int(u.primes[j]-u.primes[j-1]) if j else None))
    return dict(roots=[asdict(p) for p in roots], basins=basin_rows, gaps=gap_rows,
                grid_stable=bool(stable), root_count_coarse=len(coarse), root_count_fine=len(roots),
                final_grid_resolution=used_resolution)


class OmegaSieve:
    """Descent with momentum/noise, followed by explicit leftward barrier escape.

    Escape uses only field gradients, never the prime list or root catalogue.
    The field itself already encodes all primes. Integer labels are post-hoc
    validation of rounded coordinates (tolerance 0.25 integer units by default).
    Noise vanishes with the proposed drift to allow convergence. This is not a
    thermal Langevin sampler. Pure descent alone cannot enumerate all wells.
    """
    def __init__(self, universe, momentum=0.5, noise=0.02, seed=0,
                 backend="analytic", capture_tolerance=0.25):
        if not 0 <= momentum < 1 or not 0 <= noise <= 1:
            raise ValueError("momentum in [0,1), noise in [0,1] required")
        if not 0 < capture_tolerance < 0.5:
            raise ValueError("capture_tolerance must be in (0, 0.5)")
        if backend not in ("analytic", "autograd"):
            raise ValueError("Unknown backend")
        self.u, self.momentum, self.noise = universe, momentum, noise
        self.seed, self.backend = seed, backend
        self.capture_tolerance = capture_tolerance

    def run(self, max_steps=1_000_000, max_descent_steps=100_000):
        u, rng = self.u, np.random.default_rng(self.seed)
        step_cap = min(math.sqrt(u.epsilon)/2, 0.25/u.p_omega)
        z, velocity = 1.0, 0.0
        trajectory, captures, prime_set = [], [], set(map(int, u.primes))
        state, descent_steps, status = "descent", 0, "step_limit"
        for step in range(max_steps):
            loss, grad = u.value_gradient(z, self.backend)
            hessian = u.field(z, 2)
            trajectory.append(dict(step=step, z=z, potential=loss, gradient=grad, phase=state))
            if state == "escape":
                if z == 0:
                    status = "lower_boundary"
                    break
                if grad > 0:
                    state, velocity, descent_steps = "descent", 0.0, 0
                else:
                    z = max(0.0, z-step_cap)
                    continue
            grad_tol = 1e-7 * max(1, len(u.primes))
            if abs(grad) <= grad_tol and hessian > 0:
                integer = round(z*u.p_omega)
                distance = abs(z*u.p_omega-integer)
                label = integer if integer in prime_set and distance <= self.capture_tolerance else None
                captures.append(dict(z=z, rounded_integer=integer, prime=label,
                    distance_integer=distance, gradient_residual=abs(grad), hessian=hessian, step=step))
                state, velocity = "escape", 0.0
                z = max(0.0, z-step_cap)
                continue
            descent_steps += 1
            if descent_steps > max_descent_steps:
                status = "descent_limit"
                break
            drift = -grad/max(abs(hessian), 1.0)
            drift = float(np.clip(drift, -step_cap, step_cap))
            proposal = self.momentum*velocity + drift + rng.normal()*self.noise*abs(drift)
            if proposal*grad >= 0:
                proposal = drift
            proposal = float(np.clip(proposal, -step_cap, step_cap))
            # Backtracking guards against unstable overshoot; tiny slack handles
            # floating point cancellation near a stationary point of a large sum.
            accepted = False
            for _ in range(40):
                next_z = float(np.clip(z+proposal, 0, 1))
                if u.field(next_z) <= loss + 1e-12*max(1, abs(loss)):
                    accepted = True
                    break
                proposal *= .5
            if not accepted or next_z == z:
                status = "numerical_stall"
                break
            velocity, z = next_z-z, next_z
        detected = sorted({c['prime'] for c in captures if c['prime'] is not None}, reverse=True)
        return dict(seed=self.seed, backend=self.backend, momentum=self.momentum, noise=self.noise,
            status=status, steps=len(trajectory), capture_tolerance=self.capture_tolerance,
            step_cap=step_cap, detected_primes=detected, coverage=len(detected)/len(u.primes),
            captures=captures, trajectory=trajectory)
