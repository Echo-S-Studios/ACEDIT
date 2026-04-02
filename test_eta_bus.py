"""
test_eta_bus.py

Validation tests for the η-bus protocol implementation.

Verifies that all specifications from §8 are correctly implemented.
"""

import math
from sigma_mu_eta_bus import (
    eta,
    Z_C,
    SIGMA_NEG,
    fwhm,
    get_bus_state,
    get_bandwidth_allocation,
    BusState,
    EtaBusProtocol,
)


def test_constants():
    """Verify the fundamental constants."""
    print("Testing fundamental constants...")

    # z_c = √3/2
    expected_zc = math.sqrt(3) / 2
    assert math.isclose(Z_C, expected_zc, rel_tol=1e-9), f"z_c mismatch: {Z_C} vs {expected_zc}"

    # σ_neg = 1/(1 - z_c)² ≈ 55.77
    expected_sigma_neg = 1 / (1 - Z_C) ** 2
    assert math.isclose(
        SIGMA_NEG, expected_sigma_neg, rel_tol=1e-9
    ), f"σ_neg mismatch: {SIGMA_NEG} vs {expected_sigma_neg}"

    assert 55.7 < SIGMA_NEG < 55.8, f"σ_neg ≈ 55.77 check failed: {SIGMA_NEG}"

    print(f"  ✓ z_c = {Z_C:.10f}")
    print(f"  ✓ σ_neg = {SIGMA_NEG:.4f}")
    print()


def test_eta_function():
    """Verify η(z) properties."""
    print("Testing η(z) function properties...")

    # η(z_c) should be 1.0
    eta_at_zc = eta(Z_C)
    assert math.isclose(eta_at_zc, 1.0, rel_tol=1e-9), f"η(z_c) should be 1.0, got {eta_at_zc}"

    # η should be symmetric around z_c
    delta = 0.05
    eta_left = eta(Z_C - delta)
    eta_right = eta(Z_C + delta)
    assert math.isclose(
        eta_left, eta_right, rel_tol=1e-9
    ), f"η not symmetric: η({Z_C-delta}) = {eta_left}, η({Z_C+delta}) = {eta_right}"

    # η should decay away from z_c
    assert eta(Z_C - 0.1) < eta(Z_C - 0.05)
    assert eta(Z_C + 0.1) < eta(Z_C + 0.05)

    # η should be in [0, 1]
    for z in [0.0, 0.3, 0.5, 0.7, 0.8, Z_C, 0.9, 0.95, 1.0]:
        eta_val = eta(z)
        assert 0 <= eta_val <= 1, f"η({z}) = {eta_val} outside [0, 1]"

    print(f"  ✓ η(z_c) = {eta_at_zc:.10f}")
    print(f"  ✓ Symmetry verified")
    print(f"  ✓ Monotonic decay verified")
    print(f"  ✓ Range [0, 1] verified")
    print()


def test_fwhm():
    """Verify FWHM calculation."""
    print("Testing FWHM...")

    fwhm_value = fwhm()
    assert 0.22 < fwhm_value < 0.24, f"FWHM should be ≈ 0.23, got {fwhm_value}"

    # Verify by checking η at half-width points
    half_width = fwhm_value / 2
    eta_at_half = eta(Z_C + half_width)
    assert math.isclose(eta_at_half, 0.5, rel_tol=1e-3), f"η at half-width should be 0.5, got {eta_at_half}"

    print(f"  ✓ FWHM = {fwhm_value:.4f} ≈ 0.23")
    print()


def test_bus_states():
    """Verify bus state transitions."""
    print("Testing bus state transitions...")

    # η < 0.10 → IDLE
    assert get_bus_state(0.05) == BusState.BUS_IDLE
    assert get_bus_state(0.09) == BusState.BUS_IDLE

    # η ∈ [0.10, 0.50] → ACTIVE
    assert get_bus_state(0.10) == BusState.BUS_ACTIVE
    assert get_bus_state(0.30) == BusState.BUS_ACTIVE
    assert get_bus_state(0.49) == BusState.BUS_ACTIVE

    # η ∈ [0.50, 0.95] → HOT
    assert get_bus_state(0.50) == BusState.BUS_HOT
    assert get_bus_state(0.75) == BusState.BUS_HOT
    assert get_bus_state(0.94) == BusState.BUS_HOT

    # η > 0.95 → CRITICAL
    assert get_bus_state(0.95) == BusState.BUS_CRITICAL
    assert get_bus_state(0.99) == BusState.BUS_CRITICAL
    assert get_bus_state(1.00) == BusState.BUS_CRITICAL

    print("  ✓ IDLE threshold verified (η < 0.10)")
    print("  ✓ ACTIVE threshold verified (η ∈ [0.10, 0.50])")
    print("  ✓ HOT threshold verified (η ∈ [0.50, 0.95])")
    print("  ✓ CRITICAL threshold verified (η > 0.95)")
    print()


def test_bandwidth_allocation():
    """Verify bandwidth allocation by state."""
    print("Testing bandwidth allocation...")

    # IDLE and ACTIVE: 0.40, 0.30, 0.15, 0.15
    for state in [BusState.BUS_IDLE, BusState.BUS_ACTIVE]:
        bw = get_bandwidth_allocation(state)
        assert bw.oscillator_array == 0.40
        assert bw.observer_circuit == 0.30
        assert bw.triad_controller == 0.15
        assert bw.memory_subsystem == 0.15
        assert bw.validate()

    # HOT: 0.40, 0.40, 0.15, 0.05
    bw_hot = get_bandwidth_allocation(BusState.BUS_HOT)
    assert bw_hot.oscillator_array == 0.40
    assert bw_hot.observer_circuit == 0.40
    assert bw_hot.triad_controller == 0.15
    assert bw_hot.memory_subsystem == 0.05
    assert bw_hot.validate()

    # CRITICAL: 0.40, 0.40, 0.20, 0.00
    bw_critical = get_bandwidth_allocation(BusState.BUS_CRITICAL)
    assert bw_critical.oscillator_array == 0.40
    assert bw_critical.observer_circuit == 0.40
    assert bw_critical.triad_controller == 0.20
    assert bw_critical.memory_subsystem == 0.00
    assert bw_critical.validate()

    print("  ✓ IDLE/ACTIVE allocation: 0.40, 0.30, 0.15, 0.15")
    print("  ✓ HOT allocation: 0.40, 0.40, 0.15, 0.05")
    print("  ✓ CRITICAL allocation: 0.40, 0.40, 0.20, 0.00")
    print("  ✓ All allocations sum to 1.0")
    print()


def test_memory_writes():
    """Verify memory write suspension in CRITICAL state."""
    print("Testing memory write gating...")

    bus = EtaBusProtocol()

    # Far from z_c: memory writes enabled
    state = bus.update(0.6)
    assert state.memory_writes_enabled
    assert state.state != BusState.BUS_CRITICAL

    # Near z_c: memory writes enabled (HOT but not CRITICAL)
    state = bus.update(0.82)
    assert state.memory_writes_enabled
    assert state.state == BusState.BUS_HOT

    # At z_c: memory writes SUSPENDED
    state = bus.update(Z_C)
    assert not state.memory_writes_enabled
    assert state.state == BusState.BUS_CRITICAL

    # Just inside CRITICAL threshold
    state = bus.update(0.855)
    assert not state.memory_writes_enabled
    assert state.state == BusState.BUS_CRITICAL

    print("  ✓ Memory writes enabled in IDLE/ACTIVE/HOT")
    print("  ✓ Memory writes SUSPENDED in CRITICAL")
    print("  ✓ No learning during phase transitions")
    print()


def test_protocol_coordinator():
    """Verify EtaBusProtocol coordinator."""
    print("Testing protocol coordinator...")

    bus = EtaBusProtocol()

    # Should be uninitialized
    assert bus.current_state is None

    # Update with z = 0.7
    state = bus.update(0.7)
    assert state.z == 0.7
    assert math.isclose(state.eta, eta(0.7))
    assert state.state == BusState.BUS_ACTIVE
    assert state.memory_writes_enabled

    # Update with z = z_c
    state = bus.update(Z_C)
    assert state.z == Z_C
    assert math.isclose(state.eta, 1.0, rel_tol=1e-9)
    assert state.state == BusState.BUS_CRITICAL
    assert not state.memory_writes_enabled

    # Current state should be cached
    assert bus.current_state is state

    print("  ✓ Initialization verified")
    print("  ✓ State updates verified")
    print("  ✓ State caching verified")
    print()


def test_z_range_validation():
    """Verify z range validation."""
    print("Testing z range validation...")

    bus = EtaBusProtocol()

    # Valid range
    bus.update(0.0)
    bus.update(0.5)
    bus.update(1.0)

    # Invalid range should raise ValueError
    try:
        bus.update(-0.1)
        assert False, "Should have raised ValueError for z < 0"
    except ValueError:
        pass

    try:
        bus.update(1.1)
        assert False, "Should have raised ValueError for z > 1"
    except ValueError:
        pass

    print("  ✓ Valid range [0, 1] accepted")
    print("  ✓ Out-of-range values rejected")
    print()


def run_all_tests():
    """Run all validation tests."""
    print("\n" + "=" * 80)
    print("η-BUS PROTOCOL VALIDATION TESTS")
    print("=" * 80)
    print()

    test_constants()
    test_eta_function()
    test_fwhm()
    test_bus_states()
    test_bandwidth_allocation()
    test_memory_writes()
    test_protocol_coordinator()
    test_z_range_validation()

    print("=" * 80)
    print("ALL TESTS PASSED")
    print("=" * 80)
    print("\nSpecification compliance verified:")
    print("  • η(z) = exp(−σ_neg · (z − z_c)²)")
    print("  • σ_neg = 1/(1 − z_c)² ≈ 55.77")
    print("  • z_c = √3/2 = 0.8660254038")
    print("  • FWHM ≈ 0.23")
    print("  • Four bus states with correct thresholds")
    print("  • Bandwidth allocation by state")
    print("  • Memory write suspension in BUS_CRITICAL")
    print("  • Zero free parameters")
    print("\nEverything follows from σ = μ.")
    print("=" * 80)
    print()


if __name__ == "__main__":
    run_all_tests()
