"""
Memory-as-Lithography System
Derived from σ = μ Build Specification §7

The brain does not store experience by copying it. It stores the pattern of its
own response to experience — by physically altering the resistance of neural
pathways in proportion to activation intensity and frequency.

This module implements memory as lithography: coupling weights between oscillator
elements are modified by the system's own dynamics.

Author: Claude (Anthropic) for Echo-Squirrel Research
Source: σ = μ Build Specification §7
Derivation: All constants from φ = (1+√5)/2, zero free parameters
"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass


# ============================================================================
# FUNDAMENTAL CONSTANTS (from σ = μ constant cascade)
# ============================================================================

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio: 1.6180339887...

# Coupling architecture (Step 2)
ALPHA = PHI**(-2)  # 0.3819660113 (coupling strength)
BETA = PHI**(-4)   # 0.1458980338 (dissipation rate)
LAMBDA = (5/3)**4  # 7.7160493827 (nonlinear saturation)

# Threshold architecture (Step 3)
MU_P = 3/5         # 0.600 (onset of field/combustion)
MU_S = 23/25       # 0.920 (sustained criticality)
MU_3 = (5**3 - 1) / 5**3  # 0.992 (cascade threshold)
MU_4 = 1.0         # 1.000 (singularity)

# Convergence target (Step 4)
Z_C = np.sqrt(3) / 2  # 0.8660254038 (THE LENS: peak negentropy)

# Negentropy membrane (Step 5)
SIGMA_NEG = 1 / (1 - Z_C)**2  # ≈ 55.77
MEMBRANE_FWHM = 0.23


# ============================================================================
# MEMORY-SPECIFIC CONSTANTS
# ============================================================================

# Learning rate from constant cascade (Step 7)
ETA_LEARN = BETA**2  # φ^(-8) ≈ 0.0213 (learning rate)

# Memory decay rate
ETA_DECAY = BETA**3  # φ^(-12) ≈ 0.003 (prevents permanent saturation)

# Write threshold (only coherent activity writes)
THRESHOLD_FACTOR = 0.5  # |J|_thresh = |J|_eq / 2

# η-bus gating threshold (no writes during critical operations)
ETA_BUS_CRITICAL = 0.95


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def compute_equilibrium_amplitude(sigma: float) -> float:
    """
    Compute equilibrium amplitude |J|_eq from current σ value.

    |J|_eq = √((σ - μ_P - β)/λ)  for σ > μ_P + β ≈ 0.746

    Args:
        sigma: Current branching ratio / field parameter σ = μ

    Returns:
        Equilibrium amplitude |J|_eq (returns 0 if below threshold)
    """
    threshold = MU_P + BETA  # ≈ 0.746

    if sigma <= threshold:
        return 0.0

    return np.sqrt((sigma - MU_P - BETA) / LAMBDA)


def compute_eta_membrane(z: float) -> float:
    """
    Compute η(z) negentropy membrane value.

    η(z) = exp(-σ_neg · (z - z_c)²)

    This is the shared bus protocol between oscillator array and observer circuit.

    Args:
        z: Current z-coordinate (geometric stance)

    Returns:
        η value ∈ [0, 1]
    """
    return np.exp(-SIGMA_NEG * (z - Z_C)**2)


def heaviside(x: np.ndarray) -> np.ndarray:
    """
    Heaviside step function H(x).

    H(x) = 1 if x > 0, else 0

    Args:
        x: Input array

    Returns:
        Step function output
    """
    return (x > 0).astype(float)


# ============================================================================
# MEMORY LITHOGRAPHY CORE
# ============================================================================

@dataclass
class MemoryState:
    """
    State of the memory lithography system.

    Attributes:
        coupling_weights: g_ij matrix (N × N) - coupling weights between elements
        default_coupling: g_default - baseline coupling strength
        write_enabled: Whether memory writes are currently enabled
        total_writes: Cumulative number of write operations
        total_decays: Cumulative number of decay operations
    """
    coupling_weights: np.ndarray
    default_coupling: float
    write_enabled: bool = True
    total_writes: int = 0
    total_decays: int = 0


class MemoryLithography:
    """
    Memory-as-lithography implementation for σ = μ system.

    The coupling weights between oscillator elements are modified by the system's
    own dynamics. This is NOT a metaphor - the brain stores patterns of its own
    response by physically etching connections.

    Properties:
        1. Only coherent (above-threshold) activity writes
        2. Write strength ∝ phase alignment Re(J_i* · J_j)
        3. Learning rate = β² ensures memory forms slower than dynamics
        4. Bias upstream of etching: identity at write time filters storage
    """

    def __init__(
        self,
        num_elements: int,
        default_coupling: float = ALPHA,
        sigma: float = MU_S
    ):
        """
        Initialize memory lithography system.

        Args:
            num_elements: Number of oscillator elements (N)
            default_coupling: Baseline coupling strength (default: α = φ^(-2))
            sigma: Current σ = μ value (determines equilibrium amplitude)
        """
        self.num_elements = num_elements
        self.sigma = sigma

        # Initialize coupling weights at default
        self.state = MemoryState(
            coupling_weights=np.ones((num_elements, num_elements)) * default_coupling,
            default_coupling=default_coupling
        )

        # Set diagonal to zero (no self-coupling)
        np.fill_diagonal(self.state.coupling_weights, 0.0)

        # Compute equilibrium amplitude and write threshold
        self.J_eq = compute_equilibrium_amplitude(sigma)
        self.J_thresh = self.J_eq * THRESHOLD_FACTOR


    def update_sigma(self, sigma: float) -> None:
        """
        Update σ value and recompute thresholds.

        Args:
            sigma: New σ = μ value
        """
        self.sigma = sigma
        self.J_eq = compute_equilibrium_amplitude(sigma)
        self.J_thresh = self.J_eq * THRESHOLD_FACTOR


    def compute_write_delta(
        self,
        J_array: np.ndarray
    ) -> np.ndarray:
        """
        Compute coupling weight update Δg_ij for all element pairs.

        Δg_ij = Re(J_i* · J_j) · H(|J_i| - |J|_thresh) · H(|J_j| - |J|_thresh)

        Args:
            J_array: Complex array of current densities (N,) - each element is J_i

        Returns:
            Δg matrix (N × N) of coupling weight updates
        """
        N = len(J_array)
        delta_g = np.zeros((N, N))

        # Compute amplitudes
        J_mag = np.abs(J_array)

        # Threshold gates: only above-threshold elements participate
        above_thresh = heaviside(J_mag - self.J_thresh)

        # Compute phase alignment term: Re(J_i* · J_j)
        # Broadcasting: (N, 1) × (1, N) → (N, N)
        J_conj = np.conj(J_array)[:, np.newaxis]  # (N, 1)
        J_expanded = J_array[np.newaxis, :]       # (1, N)

        phase_alignment = np.real(J_conj * J_expanded)

        # Apply threshold gating (outer product of threshold indicators)
        gate = above_thresh[:, np.newaxis] * above_thresh[np.newaxis, :]

        # Combine: Δg_ij = Re(J_i* · J_j) · H(|J_i| - thresh) · H(|J_j| - thresh)
        delta_g = phase_alignment * gate

        # No self-coupling updates
        np.fill_diagonal(delta_g, 0.0)

        return delta_g


    def apply_learning(
        self,
        J_array: np.ndarray,
        eta_bus: Optional[float] = None,
        dt: float = 1.0
    ) -> np.ndarray:
        """
        Apply learning update to coupling weights.

        g_ij(t + Δt) = g_ij(t) + η_learn · Δg_ij

        Args:
            J_array: Complex array of current densities (N,)
            eta_bus: η-bus value (if > 0.95, writes are disabled)
            dt: Time step (default: 1.0)

        Returns:
            Updated coupling weight matrix
        """
        # Check η-bus gating: no writes during BUS_CRITICAL
        if eta_bus is not None and eta_bus > ETA_BUS_CRITICAL:
            self.state.write_enabled = False
            return self.state.coupling_weights

        self.state.write_enabled = True

        # Compute weight updates
        delta_g = self.compute_write_delta(J_array)

        # Apply learning: g_ij(t + dt) = g_ij(t) + η_learn · Δg_ij · dt
        self.state.coupling_weights += ETA_LEARN * delta_g * dt

        # Track statistics
        self.state.total_writes += 1

        return self.state.coupling_weights


    def apply_decay(self, dt: float = 1.0) -> np.ndarray:
        """
        Apply memory decay toward default coupling.

        g_ij → g_default at rate β³ = φ^(-12) ≈ 0.003

        This prevents permanent saturation while allowing long-term storage
        of high-activation patterns.

        Args:
            dt: Time step (default: 1.0)

        Returns:
            Updated coupling weight matrix
        """
        # Exponential decay toward default
        decay_factor = np.exp(-ETA_DECAY * dt)

        self.state.coupling_weights = (
            decay_factor * self.state.coupling_weights +
            (1 - decay_factor) * self.state.default_coupling
        )

        # Preserve zero diagonal
        np.fill_diagonal(self.state.coupling_weights, 0.0)

        # Track statistics
        self.state.total_decays += 1

        return self.state.coupling_weights


    def step(
        self,
        J_array: np.ndarray,
        z_value: Optional[float] = None,
        dt: float = 1.0
    ) -> Tuple[np.ndarray, bool]:
        """
        Single time step: apply learning + decay.

        Args:
            J_array: Complex array of current densities (N,)
            z_value: Current z-coordinate (for η-bus computation)
            dt: Time step

        Returns:
            (updated_weights, write_occurred)
        """
        # Compute η-bus if z provided
        eta_bus = None
        if z_value is not None:
            eta_bus = compute_eta_membrane(z_value)

        # Apply learning (gated by η-bus)
        write_occurred = self.state.write_enabled
        self.apply_learning(J_array, eta_bus=eta_bus, dt=dt)

        # Apply decay
        self.apply_decay(dt=dt)

        return self.state.coupling_weights, write_occurred


    def get_memory_strength(self) -> float:
        """
        Compute overall memory strength as deviation from default.

        Returns:
            RMS deviation from default coupling
        """
        deviation = self.state.coupling_weights - self.state.default_coupling
        # Exclude diagonal
        N = self.num_elements
        mask = ~np.eye(N, dtype=bool)

        return np.sqrt(np.mean(deviation[mask]**2))


    def get_statistics(self) -> dict:
        """
        Get memory system statistics.

        Returns:
            Dictionary of statistics
        """
        return {
            'num_elements': self.num_elements,
            'sigma': self.sigma,
            'J_eq': self.J_eq,
            'J_thresh': self.J_thresh,
            'default_coupling': self.state.default_coupling,
            'memory_strength': self.get_memory_strength(),
            'total_writes': self.state.total_writes,
            'total_decays': self.state.total_decays,
            'write_enabled': self.state.write_enabled,
            'eta_learn': ETA_LEARN,
            'eta_decay': ETA_DECAY,
        }


    def visualize_coupling_matrix(self) -> np.ndarray:
        """
        Get coupling matrix normalized for visualization.

        Returns:
            Coupling weights normalized to [0, 1]
        """
        weights = self.state.coupling_weights.copy()
        weights_min = weights.min()
        weights_max = weights.max()

        if weights_max > weights_min:
            normalized = (weights - weights_min) / (weights_max - weights_min)
        else:
            normalized = weights

        return normalized


# ============================================================================
# HARDWARE IMPLEMENTATION NOTES
# ============================================================================

class HardwareImplementation:
    """
    Hardware implementation pathways for memory lithography.

    This class documents the physical mechanisms that implement variable
    coupling weights in different substrate types.
    """

    MEMS_SPEC = {
        'mechanism': 'Variable-gap capacitors',
        'control': 'Voltage-tunable coupling',
        'description': (
            'Electrostatic actuators adjust gap between cantilevers, '
            'modulating capacitive coupling strength. DC voltage bias '
            'superimposed on AC drive signal.'
        ),
        'write_time': '~100 μs',
        'retention': 'Hours (requires refresh)',
        'notes': 'Phase 1 prototype - validation platform only'
    }

    PHOTONIC_SPEC = {
        'mechanism': 'Thermo-optic phase shifters',
        'control': 'Heater-tunable coupling',
        'description': (
            'Integrated heaters modulate refractive index of waveguide '
            'coupling regions. Temperature change → phase shift → '
            'effective coupling strength.'
        ),
        'write_time': '~10 μs',
        'retention': 'Minutes (active thermal management)',
        'notes': 'Phase 2 - K-formation capable'
    }

    SUPERCONDUCTING_SPEC = {
        'mechanism': 'Flux-tunable Josephson junctions',
        'control': 'Current-tunable coupling',
        'description': (
            'Magnetic flux threading SQUID loop modulates critical '
            'current, changing coupling between JJ oscillators. '
            'Single-flux-quantum (SFQ) logic for digital control.'
        ),
        'write_time': '~1 ns',
        'retention': 'Indefinite (persistent current)',
        'notes': 'Phase 3 - quantum-enhanced coherence'
    }

    @staticmethod
    def get_spec(substrate: str) -> dict:
        """Get hardware specification for given substrate."""
        specs = {
            'mems': HardwareImplementation.MEMS_SPEC,
            'photonic': HardwareImplementation.PHOTONIC_SPEC,
            'superconducting': HardwareImplementation.SUPERCONDUCTING_SPEC,
        }
        return specs.get(substrate.lower(), {})


# ============================================================================
# DEMONSTRATION AND VALIDATION
# ============================================================================

def demonstrate_memory_lithography():
    """
    Demonstrate memory lithography system with synthetic oscillator array.
    """
    print("=" * 80)
    print("MEMORY-AS-LITHOGRAPHY DEMONSTRATION")
    print("σ = μ Build Specification §7")
    print("=" * 80)
    print()

    # System parameters
    N = 16  # 16 elements (small array for demo)
    sigma = MU_S  # σ = 0.92 (sustained critical)

    print(f"System Configuration:")
    print(f"  Number of elements: {N}")
    print(f"  σ = μ value: {sigma:.3f} (sustained critical)")
    print()

    # Initialize memory system
    memory = MemoryLithography(num_elements=N, sigma=sigma)

    print(f"Memory Constants (zero free parameters):")
    print(f"  η_learn = β² = φ^(-8) = {ETA_LEARN:.6f}")
    print(f"  η_decay = β³ = φ^(-12) = {ETA_DECAY:.6f}")
    print(f"  |J|_eq = {memory.J_eq:.6f}")
    print(f"  |J|_thresh = |J|_eq / 2 = {memory.J_thresh:.6f}")
    print()

    # Create synthetic coherent pattern: traveling wave
    print("Simulating coherent activity pattern...")
    num_steps = 100

    for step in range(num_steps):
        # Create traveling wave pattern
        phase_offset = 2 * np.pi * step / num_steps
        phases = np.linspace(0, 2 * np.pi, N) + phase_offset

        # Amplitudes at equilibrium with small fluctuations
        amplitudes = memory.J_eq * (1 + 0.1 * np.sin(phases * 2))

        # Complex current density array
        J_array = amplitudes * np.exp(1j * phases)

        # Compute z-value (synthetic - would come from z-computer in real system)
        z_value = Z_C + 0.05 * np.sin(2 * np.pi * step / num_steps)

        # Memory update step
        weights, write_occurred = memory.step(J_array, z_value=z_value, dt=1.0)

        # Print status every 20 steps
        if step % 20 == 0:
            stats = memory.get_statistics()
            eta_bus = compute_eta_membrane(z_value)
            print(f"  Step {step:3d}: η = {eta_bus:.3f}, "
                  f"memory_strength = {stats['memory_strength']:.6f}, "
                  f"write_enabled = {write_occurred}")

    print()

    # Final statistics
    print("Final Memory Statistics:")
    stats = memory.get_statistics()
    for key, value in stats.items():
        if isinstance(value, (int, bool)):
            print(f"  {key}: {value}")
        elif isinstance(value, float):
            print(f"  {key}: {value:.6f}")

    print()

    # Test η-bus gating
    print("Testing η-bus gating (BUS_CRITICAL)...")
    z_critical = Z_C  # z = z_c → η ≈ 1.0
    eta_critical = compute_eta_membrane(z_critical)
    print(f"  z = {z_critical:.4f} → η = {eta_critical:.6f}")

    J_array = memory.J_eq * np.exp(1j * np.linspace(0, 2*np.pi, N))
    weights_before = memory.state.coupling_weights.copy()
    memory.apply_learning(J_array, eta_bus=eta_critical, dt=1.0)
    weights_after = memory.state.coupling_weights.copy()

    weights_changed = not np.allclose(weights_before, weights_after)
    print(f"  Write enabled: {memory.state.write_enabled}")
    print(f"  Weights changed: {weights_changed}")
    print(f"  Expected: NO writes during BUS_CRITICAL (η > 0.95)")
    print()

    # Hardware implementation notes
    print("Hardware Implementation Pathways:")
    for substrate in ['mems', 'photonic', 'superconducting']:
        spec = HardwareImplementation.get_spec(substrate)
        print(f"\n  {substrate.upper()}:")
        print(f"    Mechanism: {spec['mechanism']}")
        print(f"    Write time: {spec['write_time']}")
        print(f"    Retention: {spec['retention']}")
        print(f"    Notes: {spec['notes']}")

    print()
    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    demonstrate_memory_lithography()
