import numpy as np
import pytest
from omegagrad import ToyUniverse
from omegagrad.omegasieve import geometry, OmegaSieve


def test_small_universe_geometry_and_basin_partition():
    u = ToyUniverse(6)
    data = geometry(u)
    assert data['grid_stable']
    assert len(data['basins']) == 18
    assert sum(r['barrier_count'] for r in data['gaps']) == 17
    assert sum(r['width_z'] for r in data['basins']) == pytest.approx(1)
    assert max(r['gradient_residual'] for r in data['roots']) < 1e-6
    for b in data['basins']:
        assert b['lower'] < b['minimum_z'] < b['upper']
        # Local field on either side points toward the minimum.
        dx = min(b['minimum_z']-b['lower'], b['upper']-b['minimum_z']) * .01
        assert u.field(b['minimum_z']-dx,1) < 0 < u.field(b['minimum_z']+dx,1)
    assert abs(u.field(1,1)) > 1  # normalized prime is not a stationary point


def test_large_smoothing_merges_wells():
    data = geometry(ToyUniverse(6, .1))
    assert len(data['basins']) < 18
    assert any(r['barrier_count'] == 0 for r in data['gaps'])


def test_navigation_recovers_wells_and_is_reproducible():
    u = ToyUniverse(6)
    a = OmegaSieve(u, seed=7).run()
    b = OmegaSieve(u, seed=7).run()
    assert a == b
    assert a['status'] == 'lower_boundary'
    assert a['detected_primes'] == list(map(int, u.primes[::-1]))
    assert a['trajectory'][0]['z'] == 1
    assert all(0 <= r['z'] <= 1 for r in a['trajectory'])
    assert all(x['z'] > y['z'] for x,y in zip(a['captures'],a['captures'][1:]))


def test_autograd_navigation_matches_analytic():
    u = ToyUniverse(3, 1e-4)
    a = OmegaSieve(u, noise=0, backend='autograd').run()
    b = OmegaSieve(u, noise=0, backend='analytic').run()
    assert a['status'] == b['status'] == 'lower_boundary'
    assert a['detected_primes'] == b['detected_primes']
    assert np.allclose([c['z'] for c in a['captures']], [c['z'] for c in b['captures']])


def test_scaled_epsilon_crosses_flat_intervals():
    reference = ToyUniverse(8)
    u = ToyUniverse(8, 1e-6*(61/reference.p_omega)**2)
    run = OmegaSieve(u, seed=0).run()
    assert run['status'] == 'lower_boundary'
    assert run['coverage'] == 1


def test_root_refinement_resolves_close_pair():
    data = geometry(ToyUniverse(12))
    assert data['grid_stable']
    assert data['final_grid_resolution'] > 16
    assert len(data['basins']) == 74
    assert sum(b['width_z'] for b in data['basins']) == pytest.approx(1)
