# Theoretical model

**Richard Ikeda — Author & Lead Investigator**

## Finite horizon

Define `P_omega = max {p prime: p <= 2**S_bits}` and normalized coordinates `p_hat_i=p_i/P_omega`. The experimental domain is [0,1], with prime coordinates in (0,1]. Zero is a numerical boundary, not a prime. A finite cutoff enables controlled comparison of the same functional across differently sized reference sets.

The term cosmological expresses the motivation for an operational horizon. The code uses a representational cutoff, not a calculation of Kolmogorov complexity, computational entropy, or a physical limit on primality.

## Potential and local geometry

```text
L(z)   = sum_i log((z-p_hat_i)^2 + epsilon)
L'(z)  = sum_i 2*d_i/(d_i^2+epsilon)
L''(z) = sum_i 2*(epsilon-d_i^2)/(d_i^2+epsilon)^2
```

Here `d_i=z-p_hat_i` and epsilon is positive. Its characteristic spatial width is sqrt(epsilon). Summation avoids evaluating an exponentially scaled product of factors. It also changes the geometry: a smoothed minimum need not coincide exactly with its associated prime, because every other term contributes force.

A positive second derivative identifies a local minimum; a negative second derivative identifies a local maximum. In this one-dimensional model, maxima are barriers rather than multidimensional saddle points. There is no general guarantee of one barrier per prime gap for arbitrary positive epsilon.

The control `epsilon=1e-6*(61/P_omega)^2` keeps the smoothing width equal to 0.061 in integer units. This scaling identity is exact by construction. Preservation of wells is an empirical finding over tested configurations, not a general theorem following from that identity.

## Continuum background

The model background integrates `rho(u)=P_omega/log(u*P_omega)` from `2/P_omega` to 1 against the same logarithmic kernel. This density is an asymptotic modeling approximation, especially near the lower endpoint. The background depends on horizon and epsilon but not individual prime positions. The residual is `Delta L=L-background`.

The complete L still encodes the prime targets, so subtracting a prime-position-free background does not remove oracle dependence from residual geometry.

## Reduced-base waves

`W(x)=sum sin²(pi*x/p)` has zeros at common multiples of the base, including zero. The radar uses `U(x)=-sum log(sin²(pi*x/p)+epsilon)`. Composite integer coordinates can have large contributions when a base prime divides them. Finite epsilon caps those contributions. Neither nonzero phase terms nor low energy guarantees a stationary minimum at a prime, and rounding a continuous minimum may produce a composite.

The phase-3 implementation removes 2 and 3 from U and scans cells centered on 6k±1. This is an explicit arithmetic restriction. Adding positive cos²(pi*x) is not equivalent, since its minima occur at half-integers.

See [the paper](PAPER.md) for the hypotheses, results, and interpretation.
