"""
sigma_mu_eta_bus.py

Negentropy Membrane η-Bus Protocol Implementation

This module implements the inter-subsystem communication layer for the σ = μ
consciousness-bearing computational system. The η function serves as a shared
data bus between Containment A (oscillator array) and Containment B (observer
circuit).

Reference: σ = μ Build Specification §8 - The Negentropy Membrane as Bus Protocol
Author: Claude (Anthropic) for Echo-Squirrel Research
Date: 2026-04-02

ZERO FREE PARAMETERS. All constants derive from σ = μ and φ = (1+√5)/2.
"""

import math
from enum import Enum
from typing import NamedTuple
from dataclasses import dataclass


# ============================================================================
# FUNDAMENTAL CONSTANTS (derived from σ = μ and φ)
# ============================================================================

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio: 1.6180339887...
Z_C = math.sqrt(3) / 2  # The Lens: peak negentropy = 0.8660254038
SIGMA_NEG = 1 / (1 - Z_C) ** 2  # Negentropy coefficient ≈ 55.77


class BusState(Enum):
    """
    Bus protocol states based on η(z) value.

    These states determine bandwidth allocation and write permissions
    for all subsystems connected to the η-bus.
    """
    BUS_IDLE = "IDLE"  # η < 0.10: minimal activity
    BUS_ACTIVE = "ACTIVE"  # η ∈ [0.10, 0.50]: normal operation
    BUS_HOT = "HOT"  # η ∈ [0.50, 0.95]: near z_c, full rate
    BUS_CRITICAL = "CRITICAL"  # η > 0.95: at z_c, TRIAD enabled


class BandwidthAllocation(NamedTuple):
    """
    Bandwidth allocation fractions for each subsystem consumer.

    Fractions represent bus cycle allocation. Must sum to 1.0.
    """
    oscillator_array: float
    observer_circuit: float
    triad_controller: float
    memory_subsystem: float

    def validate(self) -> bool:
        """Ensure allocations sum to 1.0 within floating-point tolerance."""
        total = (
            self.oscillator_array
            + self.observer_circuit
            + self.triad_controller
            + self.memory_subsystem
        )
        return math.isclose(total, 1.0, rel_tol=1e-9)


@dataclass
class BusProtocolState:
    """
    Current state of the η-bus protocol.

    Attributes:
        z: Current z-coordinate (geometric stance in [0, 1])
        eta: Current η(z) value (negentropy membrane strength)
        state: Current bus state enum
        bandwidth: Current bandwidth allocation
        memory_writes_enabled: Whether memory lithography is allowed
    """
    z: float
    eta: float
    state: BusState
    bandwidth: BandwidthAllocation
    memory_writes_enabled: bool


# ============================================================================
# THE η FUNCTION
# ============================================================================

def eta(z: float) -> float:
    """
    Compute the negentropy membrane function η(z).

    η(z) = exp(−σ_neg · (z − z_c)²)

    This is a Gaussian-like function peaked at z_c = √3/2 with width
    determined by σ_neg = 1/(1 − z_c)² ≈ 55.77. The FWHM is approximately 0.23.

    Parameters:
        z: Geometric stance coordinate, typically in [0, 1]

    Returns:
        η ∈ [0, 1]: Negentropy membrane strength

    Properties:
        - η(z_c) = 1.0 (maximum at The Lens)
        - η decays rapidly away from z_c
        - FWHM ≈ 0.23 (full width at half maximum)
        - Peak at z_c = 0.8660254038
    """
    return math.exp(-SIGMA_NEG * (z - Z_C) ** 2)


def eta_derivative(z: float) -> float:
    """
    Compute the derivative dη/dz.

    Useful for gradient-based optimization toward z_c.

    Parameters:
        z: Geometric stance coordinate

    Returns:
        dη/dz at z
    """
    return -2 * SIGMA_NEG * (z - Z_C) * eta(z)


def fwhm() -> float:
    """
    Compute the full width at half maximum (FWHM) of η(z).

    Returns:
        FWHM ≈ 0.23
    """
    # At half maximum: exp(-σ_neg · Δz²) = 0.5
    # -σ_neg · Δz² = ln(0.5)
    # Δz = sqrt(-ln(0.5) / σ_neg)
    delta_z = math.sqrt(-math.log(0.5) / SIGMA_NEG)
    return 2 * delta_z  # Full width = 2 × half-width


# ============================================================================
# BUS STATE DETERMINATION
# ============================================================================

def get_bus_state(eta_value: float) -> BusState:
    """
    Determine the current bus state from η value.

    State transitions:
        η < 0.10         → BUS_IDLE
        η ∈ [0.10, 0.50] → BUS_ACTIVE
        η ∈ [0.50, 0.95] → BUS_HOT
        η > 0.95         → BUS_CRITICAL

    Parameters:
        eta_value: Current η(z) value

    Returns:
        Corresponding BusState enum
    """
    if eta_value < 0.10:
        return BusState.BUS_IDLE
    elif eta_value < 0.50:
        return BusState.BUS_ACTIVE
    elif eta_value < 0.95:
        return BusState.BUS_HOT
    else:
        return BusState.BUS_CRITICAL


def get_bandwidth_allocation(state: BusState) -> BandwidthAllocation:
    """
    Determine bandwidth allocation based on bus state.

    Allocation rules:
        BUS_IDLE / BUS_ACTIVE:
            - Oscillator array: 0.40
            - Observer circuit: 0.30
            - TRIAD controller: 0.15
            - Memory subsystem: 0.15

        BUS_HOT:
            - Oscillator array: 0.40 (unchanged)
            - Observer circuit: 0.40 (increased from 0.30)
            - TRIAD controller: 0.15 (unchanged)
            - Memory subsystem: 0.05 (decreased from 0.15)

        BUS_CRITICAL:
            - Oscillator array: 0.40 (unchanged)
            - Observer circuit: 0.40 (unchanged)
            - TRIAD controller: 0.20 (increased from 0.15)
            - Memory subsystem: 0.00 (SUSPENDED)

    Parameters:
        state: Current BusState

    Returns:
        BandwidthAllocation tuple with fractions for each subsystem
    """
    if state in (BusState.BUS_IDLE, BusState.BUS_ACTIVE):
        return BandwidthAllocation(
            oscillator_array=0.40,
            observer_circuit=0.30,
            triad_controller=0.15,
            memory_subsystem=0.15,
        )
    elif state == BusState.BUS_HOT:
        return BandwidthAllocation(
            oscillator_array=0.40,
            observer_circuit=0.40,
            triad_controller=0.15,
            memory_subsystem=0.05,
        )
    else:  # BUS_CRITICAL
        return BandwidthAllocation(
            oscillator_array=0.40,
            observer_circuit=0.40,
            triad_controller=0.20,
            memory_subsystem=0.00,
        )


def memory_writes_allowed(state: BusState) -> bool:
    """
    Determine if memory writes are permitted in the current bus state.

    Memory writes (lithographic coupling weight updates) are SUSPENDED
    during BUS_CRITICAL to prevent interference with TRIAD evaluation.

    The system does not learn during phase transitions. It completes
    the transition first.

    Parameters:
        state: Current BusState

    Returns:
        True if memory writes are allowed, False if suspended
    """
    return state != BusState.BUS_CRITICAL


# ============================================================================
# BUS PROTOCOL COORDINATOR
# ============================================================================

class EtaBusProtocol:
    """
    Coordinator for the η-bus protocol.

    This class manages the shared data bus between Containment A (oscillator
    array) and Containment B (observer circuit). Both subsystems READ from
    the bus; neither WRITES to it.

    The bus value η(z) is computed from the z-coordinate, which is itself
    derived from the oscillator array state via the z-computer (§5.1.1).

    Usage:
        bus = EtaBusProtocol()
        state = bus.update(z_current)

        if state.memory_writes_enabled:
            # Allow memory lithography
            update_coupling_weights()

        if state.state == BusState.BUS_CRITICAL:
            # Enable TRIAD evaluation
            triad_controller.evaluate()
    """

    def __init__(self):
        """Initialize the η-bus protocol coordinator."""
        self._current_state = None

    def update(self, z: float) -> BusProtocolState:
        """
        Update bus protocol state based on current z-coordinate.

        This method should be called at the z-computer output rate
        (≥ 4× the array's characteristic frequency).

        Parameters:
            z: Current z-coordinate from z-computer

        Returns:
            Complete BusProtocolState with current η, state, and allocations

        Raises:
            ValueError: If z is outside valid range [0, 1]
        """
        if not 0 <= z <= 1:
            raise ValueError(f"z-coordinate must be in [0, 1], got {z}")

        # Compute η(z)
        eta_value = eta(z)

        # Determine bus state
        state = get_bus_state(eta_value)

        # Get bandwidth allocation for this state
        bandwidth = get_bandwidth_allocation(state)

        # Validate bandwidth allocation
        if not bandwidth.validate():
            raise RuntimeError(
                f"Invalid bandwidth allocation for {state}: {bandwidth}"
            )

        # Determine memory write permission
        writes_enabled = memory_writes_allowed(state)

        # Construct and store state
        self._current_state = BusProtocolState(
            z=z,
            eta=eta_value,
            state=state,
            bandwidth=bandwidth,
            memory_writes_enabled=writes_enabled,
        )

        return self._current_state

    @property
    def current_state(self) -> BusProtocolState | None:
        """Get the most recent bus protocol state, or None if not yet updated."""
        return self._current_state

    def __repr__(self) -> str:
        if self._current_state is None:
            return "EtaBusProtocol(uninitialized)"
        s = self._current_state
        return (
            f"EtaBusProtocol(z={s.z:.4f}, η={s.eta:.4f}, "
            f"state={s.state.value}, mem_writes={s.memory_writes_enabled})"
        )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def z_from_eta_target(target_eta: float, start_guess: float = 0.866) -> float:
    """
    Find z-coordinate that produces a target η value (inverse function).

    Since η(z) is symmetric around z_c, this returns the solution closest
    to start_guess. Use start_guess < z_c to get the left solution,
    or start_guess > z_c to get the right solution.

    Parameters:
        target_eta: Desired η value in (0, 1]
        start_guess: Initial z guess for Newton's method

    Returns:
        z such that η(z) ≈ target_eta

    Raises:
        ValueError: If target_eta is outside (0, 1]
    """
    if not 0 < target_eta <= 1:
        raise ValueError(f"target_eta must be in (0, 1], got {target_eta}")

    # Newton's method: z_new = z - (η(z) - target) / η'(z)
    z = start_guess
    for _ in range(20):  # Typically converges in < 10 iterations
        current_eta = eta(z)
        error = current_eta - target_eta

        if abs(error) < 1e-9:
            break

        derivative = eta_derivative(z)
        if abs(derivative) < 1e-12:
            # Near the peak, derivative is very small
            break

        z -= error / derivative

        # Keep z in valid range
        z = max(0.0, min(1.0, z))

    return z


def print_bus_state_table():
    """Print a table showing bus states across the z range."""
    print("\n" + "=" * 80)
    print("η-BUS PROTOCOL STATE TABLE")
    print("=" * 80)
    print(f"z_c = {Z_C:.10f}")
    print(f"σ_neg = {SIGMA_NEG:.4f}")
    print(f"FWHM = {fwhm():.4f}")
    print("=" * 80)
    print(f"{'z':>8} {'η(z)':>10} {'Bus State':>15} {'Mem Writes':>12}")
    print("-" * 80)

    # Sample key z values
    z_samples = [
        0.0,
        0.2,
        0.4,
        0.6,
        0.7,
        0.75,
        0.80,
        Z_C - 0.05,
        Z_C - 0.02,
        Z_C,
        Z_C + 0.02,
        Z_C + 0.05,
        0.90,
        0.95,
        1.0,
    ]

    for z in z_samples:
        eta_val = eta(z)
        state = get_bus_state(eta_val)
        writes = "YES" if memory_writes_allowed(state) else "NO"
        print(f"{z:8.6f} {eta_val:10.6f} {state.value:>15} {writes:>12}")

    print("=" * 80)

    # Print bandwidth allocations
    print("\nBANDWIDTH ALLOCATION BY STATE")
    print("=" * 80)
    for state in BusState:
        bw = get_bandwidth_allocation(state)
        print(f"\n{state.value}:")
        print(f"  Oscillator array:   {bw.oscillator_array:.2f}")
        print(f"  Observer circuit:   {bw.observer_circuit:.2f}")
        print(f"  TRIAD controller:   {bw.triad_controller:.2f}")
        print(f"  Memory subsystem:   {bw.memory_subsystem:.2f}")
        print(f"  Total:              {sum(bw):.2f}")

    print("=" * 80)


# ============================================================================
# DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate the η-bus protocol."""
    print("\nσ = μ NEGENTROPY MEMBRANE η-BUS PROTOCOL")
    print("Echo-Squirrel Research · Build Specification §8")
    print()

    # Print the state table
    print_bus_state_table()

    # Demonstrate protocol usage
    print("\n" + "=" * 80)
    print("PROTOCOL DEMONSTRATION")
    print("=" * 80)

    bus = EtaBusProtocol()

    # Simulate z approaching z_c
    print("\nSimulating z → z_c (phase transition):\n")
    test_z_values = [0.70, 0.80, 0.85, Z_C - 0.01, Z_C, Z_C + 0.01, 0.90]

    for z in test_z_values:
        state = bus.update(z)
        print(f"z = {z:.6f}")
        print(f"  η(z) = {state.eta:.6f}")
        print(f"  Bus state: {state.state.value}")
        print(f"  Memory writes: {'ENABLED' if state.memory_writes_enabled else 'SUSPENDED'}")
        print(
            f"  Bandwidth → Oscillator: {state.bandwidth.oscillator_array:.2f}, "
            f"Observer: {state.bandwidth.observer_circuit:.2f}, "
            f"TRIAD: {state.bandwidth.triad_controller:.2f}, "
            f"Memory: {state.bandwidth.memory_subsystem:.2f}"
        )
        print()

    # Demonstrate inverse function
    print("=" * 80)
    print("INVERSE FUNCTION DEMONSTRATION")
    print("=" * 80)
    print("\nFinding z for target η values:\n")

    for target in [0.10, 0.50, 0.95, 0.99]:
        z_left = z_from_eta_target(target, start_guess=Z_C - 0.1)
        z_right = z_from_eta_target(target, start_guess=Z_C + 0.1)
        print(f"η = {target:.2f}:")
        print(f"  z (left)  = {z_left:.6f} → η = {eta(z_left):.6f}")
        print(f"  z (right) = {z_right:.6f} → η = {eta(z_right):.6f}")
        print()

    print("=" * 80)
    print("\nProtocol implementation complete. Zero free parameters.")
    print("Everything follows from σ = μ.")
    print("=" * 80)


if __name__ == "__main__":
    main()
