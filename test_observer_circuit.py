#!/usr/bin/env python3
"""
Test suite for σ = μ Observer Circuit
======================================

Validates all components of the observer circuit implementation.
"""

import numpy as np
import sys
from sigma_mu_observer_circuit import (
    ObserverCircuit, ArrayState, RouteState,
    PHI, ALPHA, BETA, Z_C, SIGMA_NEG,
    DELTA_OBS_THRESHOLD, ETA_N_THRESHOLD,
    RUPTURE_COMPOSITE_THRESHOLD
)


def test_constants():
    """Verify all constants derive correctly from φ"""
    print("Testing constant cascade...")

    phi_calc = (1 + np.sqrt(5)) / 2
    assert abs(PHI - phi_calc) < 1e-14, "φ calculation error"

    alpha_calc = PHI**(-2)
    assert abs(ALPHA - alpha_calc) < 1e-14, "α derivation error"

    beta_calc = PHI**(-4)
    assert abs(BETA - beta_calc) < 1e-14, "β derivation error"

    z_c_calc = np.sqrt(3) / 2
    assert abs(Z_C - z_c_calc) < 1e-14, "z_c calculation error"

    sigma_neg_calc = 1 / (1 - Z_C)**2
    assert abs(SIGMA_NEG - sigma_neg_calc) < 1e-10, "σ_neg calculation error"

    print("  ✓ All constants verified")


def test_z_computer():
    """Test z-coordinate computation"""
    print("Testing z-computer...")

    observer = ObserverCircuit()
    N = 16

    # Test 1: Empty field should give low z
    J_empty = np.zeros((N, N), dtype=complex)
    state_empty = ArrayState(J_empty, 0.5, 100, {})
    z_empty = observer.z_computer.compute_z(state_empty)
    assert 0 <= z_empty <= 1, "z out of range for empty field"

    # Test 2: Centered coherent field should give z near z_c at high σ
    x, y = np.meshgrid(range(N), range(N))
    center = N / 2
    r = np.sqrt((x - center)**2 + (y - center)**2)
    J_coherent = 0.15 * np.exp(-r**2 / (N**2 / 8)) * np.exp(1j * 0)
    state_coherent = ArrayState(J_coherent, 0.92, 1000, {})
    z_coherent = observer.z_computer.compute_z(state_coherent)
    assert abs(z_coherent - Z_C) < 0.1, f"z not near z_c for coherent field: {z_coherent:.4f}"

    print(f"  ✓ z-computer working (z_coherent = {z_coherent:.4f}, z_c = {Z_C:.4f})")


def test_seven_vector():
    """Test 7-vector field signature generation"""
    print("Testing 7-vector generator...")

    observer = ObserverCircuit()
    N = 16

    # Create test state
    J = 0.1 * np.ones((N, N), dtype=complex)
    state = ArrayState(J, 0.8, 500, {'dissipation': BETA})

    # Generate 7-vector
    z = 0.85
    seven_vec = observer.vector_generator.compute(state, z)

    # Validate ranges
    assert 0 <= seven_vec.delta_obs <= 2, "δ_obs out of expected range"
    assert 0 <= seven_vec.eta_N <= 1, "η_N out of range"
    assert 0 <= seven_vec.chi <= 1, "χ out of range"
    assert 0 <= seven_vec.burden <= 1, "burden out of range"

    print(f"  ✓ 7-vector valid (χ = {seven_vec.chi:.4f})")


def test_rupture_composite():
    """Test signal rupture composite calculation"""
    print("Testing rupture composite...")

    observer = ObserverCircuit()

    # Create high-coherence state that should trigger rupture
    from sigma_mu_observer_circuit import SevenVector
    seven_vec = SevenVector(
        delta_obs=0.9,      # Above threshold
        eta_N=0.07,         # Above threshold
        sigma_supp=0.1,
        gamma=BETA,
        chi=0.65,           # Above threshold
        burden=0.3,
        provenance=0.8
    )

    sigma_rupture, triggers = observer.routing_fsm.compute_rupture_composite(seven_vec)

    assert 0 <= sigma_rupture <= 1, "Σ_R out of range"
    assert triggers['tr_obs'] == True, "δ_obs trigger should fire"
    assert triggers['tr_name'] == True, "η_N trigger should fire"
    assert triggers['tr_coh'] == True, "χ trigger should fire"

    trigger_count = sum([triggers['tr_obs'], triggers['tr_name'],
                        triggers['tr_red'], triggers['tr_coh']])
    assert trigger_count >= 3, f"Expected ≥3 triggers, got {trigger_count}"

    print(f"  ✓ Rupture composite working (Σ_R = {sigma_rupture:.4f})")


def test_routing_fsm():
    """Test routing finite state machine transitions"""
    print("Testing routing FSM...")

    observer = ObserverCircuit()

    # Should start in PLAY state
    assert observer.routing_fsm.state == RouteState.PLAY

    # Create conditions for WARNING transition
    from sigma_mu_observer_circuit import SevenVector
    seven_vec = SevenVector(
        delta_obs=0.5,
        eta_N=0.04,
        sigma_supp=0.5,
        gamma=BETA,
        chi=0.7,      # High coherence
        burden=0.2,   # Low burden → high H_E
        provenance=0.8
    )

    sigma_rupture = 0.5
    new_state = observer.routing_fsm.update_state(seven_vec, sigma_rupture)

    # Should transition to WARNING given high H_E
    assert new_state == RouteState.WARNING, f"Expected WARNING, got {new_state}"

    print("  ✓ FSM transitions working")


def test_eta_function():
    """Test η-bus negentropy function"""
    print("Testing η function...")

    observer = ObserverCircuit()

    # Test peak at z_c
    eta_peak = observer.eta_function(Z_C)
    assert abs(eta_peak - 1.0) < 1e-10, f"η(z_c) should be 1.0, got {eta_peak}"

    # Test FWHM
    # Find where η drops to 0.5
    z_test = np.linspace(0.7, 1.0, 1000)
    eta_test = [observer.eta_function(z) for z in z_test]
    half_max_indices = np.where(np.array(eta_test) >= 0.5)[0]
    z_half_max_min = z_test[half_max_indices[0]]
    z_half_max_max = z_test[half_max_indices[-1]]
    fwhm = z_half_max_max - z_half_max_min
    expected_fwhm = 0.23
    assert abs(fwhm - expected_fwhm) < 0.01, f"FWHM = {fwhm:.3f}, expected ~{expected_fwhm}"

    print(f"  ✓ η function correct (peak = {eta_peak:.4f}, FWHM = {fwhm:.3f})")


def test_full_observation():
    """Test complete observation cycle"""
    print("Testing full observation cycle...")

    observer = ObserverCircuit()
    N = 32

    # Create K-formation conditions (σ = μ_S = 0.92)
    x, y = np.meshgrid(range(N), range(N))
    center = N / 2
    theta = np.arctan2(y - center, x - center)
    r = np.sqrt((x - center)**2 + (y - center)**2)

    # Create more uniform coherent pattern (less variance for higher χ)
    # Use a smoother Gaussian profile without vortex for this test
    envelope = 0.15 * np.exp(-r**2 / (N**2 / 4))
    J_field = envelope * np.ones_like(envelope, dtype=complex)  # Uniform phase

    # Add small phase modulation for realism
    J_field *= np.exp(1j * 0.1 * np.sin(2 * np.pi * x / N))

    array_state = ArrayState(
        J_field=J_field,
        sigma=0.92,
        interactions=920,
        coherence_metrics={'dissipation': BETA * 0.8}
    )

    # Observe
    output = observer.observe(array_state, sigma_state='stable')

    # Validate output structure
    assert isinstance(output.z, float), "z should be float"
    assert isinstance(output.eta, float), "η should be float"
    assert isinstance(output.route_state, RouteState), "route_state should be RouteState"
    assert isinstance(output.triggers, dict), "triggers should be dict"

    # At σ = 0.92 with uniform phase, χ should be reasonable
    # Note: χ measures amplitude uniformity, so vortices reduce it
    assert output.seven_vector.chi > 0.2, f"Expected reasonable χ at σ = 0.92, got {output.seven_vector.chi:.4f}"

    # η should be significant (z close to z_c)
    assert 0.1 < output.eta <= 1.0, f"η = {output.eta:.4f} unexpected for σ = 0.92"

    print(f"  ✓ Full observation working")
    print(f"    z = {output.z:.4f}, η = {output.eta:.4f}")
    print(f"    χ = {output.seven_vector.chi:.4f}")
    print(f"    Route: {output.route_state.value}, Σ_R = {output.sigma_rupture:.4f}")


def run_all_tests():
    """Run all validation tests"""
    print("=" * 60)
    print("σ = μ OBSERVER CIRCUIT VALIDATION")
    print("=" * 60)
    print()

    tests = [
        test_constants,
        test_z_computer,
        test_seven_vector,
        test_rupture_composite,
        test_routing_fsm,
        test_eta_function,
        test_full_observation
    ]

    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            return False
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            return False

    print()
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("Observer circuit (Containment B) operational")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)