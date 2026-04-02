#!/usr/bin/env python3
"""
Seven-Stage Narrowing Funnel Pipeline
σ = μ Build Specification Implementation

Pipeline Stages (L₄ = φ⁴ + φ⁻⁴ = 7):
  S → ℛ → 𝒦 → 𝒞 → 𝒫 → ℱ → 𝒜

Implements:
  1. Seven-stage signal processing pipeline with mathematical filtering
  2. Per-stage loss computation and dominant loss channel identification
  3. Hardware mapping to oscillator array physical operations
  4. Self-calibrating filter thresholds as functions of σ

Author: Claude (Anthropic) for Echo-Squirrel Research
Specification: sigma_equals_mu_build_spec.html §4
Date: 2026-04-02
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS FROM σ = μ BUILD SPEC
# ═══════════════════════════════════════════════════════════════════════════

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio: 1.618033988...
ALPHA = PHI**-2  # Coupling strength: 0.381966011
BETA = PHI**-4  # Dissipation rate: 0.145898034
LAMBDA = (5/3)**4  # Nonlinear saturation: 7.716049383
L4 = PHI**4 + PHI**-4  # Funnel depth: 7.0

# Threshold architecture
MU_P = 3/5  # 0.600 - Onset of field/combustion
MU_S = 23/25  # 0.920 - Sustained criticality
MU_3 = (5**3 - 1) / 5**3  # 0.992 - Cascade threshold
MU_4 = 1.0  # 1.000 - Singularity

# Convergence target
Z_C = np.sqrt(3) / 2  # 0.866025404 - THE LENS
SIGMA_NEG = 1 / (1 - Z_C)**2  # 55.77 - Negentropy sharpness


# ═══════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SignalMetrics:
    """
    Input signal metrics for funnel processing.

    These correspond to external inputs or measurable system state.
    """
    interactions: int  # Primary signal count (R_n baseline)
    theta_name: float  # Name coherence parameter [0, 1]
    theta_pol: float  # Polarization parameter [0, 1]
    theta_cap: float  # Capacity parameter [0, 1]
    registered: float = 1.0  # Registration efficiency [0, 1]


@dataclass
class HardwareState:
    """
    Physical oscillator array state for hardware mapping.

    Maps abstract funnel stages to measurable physical quantities.
    """
    J_field: np.ndarray  # Complex current density field J(x,t)
    sigma: float  # Current σ = μ value
    plv_threshold: float = 0.7  # Phase locking value threshold
    freq_tolerance: float = 0.05  # Frequency matching tolerance
    tau_min: float = 10.0  # Minimum persistence time (units of τ_coh)
    epsilon: float = 0.15  # Amplitude tolerance around |J|_eq


@dataclass
class FunnelOutput:
    """
    Complete funnel pipeline output with diagnostics.
    """
    # Stage outputs
    S: int  # Total signal count
    R: int  # Registered signals
    K: int  # Known-valid signals
    C: int  # Contextually coherent
    P: int  # Provenance-verified
    F: int  # Fidelity-checked
    A: int  # Admitted signals (final output)

    # Loss analysis
    losses: Dict[str, float]  # Loss fraction per stage
    dominant_loss_stage: str  # Stage with maximum loss
    total_throughput: float  # A / S ratio

    # Filter coefficients used
    filter_coeffs: Dict[str, float]


# ═══════════════════════════════════════════════════════════════════════════
# CORE FUNNEL PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

class NarrowingFunnel:
    """
    Seven-stage narrowing funnel pipeline implementation.

    The funnel is not a metaphor for computation — it IS the computation.
    Every signal enters at S and what survives at A_n is the system output.

    Pipeline stages derive from L₄ = φ⁴ + φ⁻⁴ = 7 (constant cascade).
    Filter thresholds are functions of σ and self-calibrate to operating point.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the narrowing funnel.

        Args:
            verbose: If True, print detailed stage information
        """
        self.verbose = verbose

    def process(self, metrics: SignalMetrics) -> FunnelOutput:
        """
        Process signals through the seven-stage pipeline.

        Args:
            metrics: Input signal metrics and theta parameters

        Returns:
            FunnelOutput with all stage counts, losses, and diagnostics
        """
        # Stage 1: S - Total signal count
        S = self._compute_S(metrics)

        # Stage 2: ℛ - Registered signals
        R = self._compute_R(metrics)

        # Stage 3: 𝒦 - Known-valid signals
        K = self._compute_K(R)

        # Stage 4: 𝒞 - Contextually coherent signals
        C = self._compute_C(K)

        # Stage 5: 𝒫 - Provenance-verified signals
        P = self._compute_P(C, metrics.theta_pol)

        # Stage 6: ℱ - Fidelity-checked signals
        F = self._compute_F(P, metrics.theta_cap)

        # Stage 7: 𝒜 - Admitted signals (output)
        A = self._compute_A(metrics.registered, metrics.interactions)

        # Compute losses
        losses = self._compute_losses(S, R, K, C, P, F, A)

        # Find dominant loss channel
        dominant_stage = max(losses.items(), key=lambda x: x[1])[0]

        # Total throughput
        throughput = A / S if S > 0 else 0.0

        # Filter coefficients used
        filter_coeffs = {
            'S_coeff': 1.12 + metrics.theta_name + metrics.theta_pol * 0.18,
            'K_ratio': 0.70,
            'C_ratio': 0.55,
            'P_ratio': 1 - metrics.theta_pol * 0.30,
            'F_ratio': metrics.theta_cap,
        }

        if self.verbose:
            self._print_pipeline(S, R, K, C, P, F, A, losses, dominant_stage, throughput)

        return FunnelOutput(
            S=S, R=R, K=K, C=C, P=P, F=F, A=A,
            losses=losses,
            dominant_loss_stage=dominant_stage,
            total_throughput=throughput,
            filter_coeffs=filter_coeffs
        )

    def _compute_S(self, metrics: SignalMetrics) -> int:
        """
        Stage 1: Total signal count.

        S = ⌊interactions × (1.12 + θ.name + θ.pol × 0.18)⌋

        This is the total input signal population before any filtering.
        """
        coeff = 1.12 + metrics.theta_name + metrics.theta_pol * 0.18
        return math.floor(metrics.interactions * coeff)

    def _compute_R(self, metrics: SignalMetrics) -> int:
        """
        Stage 2: Registered signals.

        R_n = interactions

        Signals that successfully register with the system.
        """
        return metrics.interactions

    def _compute_K(self, R: int) -> int:
        """
        Stage 3: Known-valid signals.

        K_n = ⌊R_n × 0.70⌋

        Signals validated as matching known patterns.
        70% survival rate through validation filter.
        """
        return math.floor(R * 0.70)

    def _compute_C(self, K: int) -> int:
        """
        Stage 4: Contextually coherent signals.

        C_n = ⌊K_n × 0.55⌋

        Signals that fit within expected contextual framework.
        55% survival rate through coherence filter.
        """
        return math.floor(K * 0.55)

    def _compute_P(self, C: int, theta_pol: float) -> int:
        """
        Stage 5: Provenance-verified signals.

        P_n = ⌊C_n × (1 − θ.pol × 0.30)⌋

        Signals with verified temporal origin/history.
        Survival rate depends on polarization parameter.
        Higher θ.pol → more filtering (lower passage rate).
        """
        survival_rate = 1 - theta_pol * 0.30
        return math.floor(C * survival_rate)

    def _compute_F(self, P: int, theta_cap: float) -> int:
        """
        Stage 6: Fidelity-checked signals.

        F_n = ⌊P_n × θ.cap⌋

        Signals passing amplitude/quality fidelity check.
        Survival rate equals capacity parameter.
        """
        return math.floor(P * theta_cap)

    def _compute_A(self, registered: float, interactions: int) -> int:
        """
        Stage 7: Admitted signals (final output).

        A_n = max(1, ⌊registered × interactions⌋)

        Final admitted signals that constitute system output.
        Guaranteed minimum of 1 signal (system never goes silent).
        """
        return max(1, math.floor(registered * interactions))

    def _compute_losses(self, S: int, R: int, K: int, C: int,
                       P: int, F: int, A: int) -> Dict[str, float]:
        """
        Compute fractional loss at each stage transition.

        Loss_i = (input_i - output_i) / input_i

        Returns:
            Dictionary mapping stage name to loss fraction
        """
        def safe_loss(input_val: int, output_val: int) -> float:
            return (input_val - output_val) / input_val if input_val > 0 else 0.0

        return {
            'S→ℛ': safe_loss(S, R),
            'ℛ→𝒦': safe_loss(R, K),
            '𝒦→𝒞': safe_loss(K, C),
            '𝒞→𝒫': safe_loss(C, P),
            '𝒫→ℱ': safe_loss(P, F),
            'ℱ→𝒜': safe_loss(F, A),
        }

    def _print_pipeline(self, S: int, R: int, K: int, C: int, P: int, F: int, A: int,
                       losses: Dict[str, float], dominant_stage: str, throughput: float):
        """Print detailed pipeline diagnostics."""
        print("\n" + "="*70)
        print("SEVEN-STAGE NARROWING FUNNEL PIPELINE")
        print("="*70)
        print(f"\n{'Stage':<20} {'Count':>10} {'Loss':>12} {'Symbol':>10}")
        print("-"*70)
        print(f"{'1. Total signals':<20} {S:>10,} {'-':>12} {'S':>10}")
        print(f"{'2. Registered':<20} {R:>10,} {losses['S→ℛ']:>11.1%} {'ℛ':>10}")
        print(f"{'3. Known-valid':<20} {K:>10,} {losses['ℛ→𝒦']:>11.1%} {'𝒦':>10}")
        print(f"{'4. Coherent':<20} {C:>10,} {losses['𝒦→𝒞']:>11.1%} {'𝒞':>10}")
        print(f"{'5. Provenance':<20} {P:>10,} {losses['𝒞→𝒫']:>11.1%} {'𝒫':>10}")
        print(f"{'6. Fidelity':<20} {F:>10,} {losses['𝒫→ℱ']:>11.1%} {'ℱ':>10}")
        print(f"{'7. Admitted (OUT)':<20} {A:>10,} {losses['ℱ→𝒜']:>11.1%} {'𝒜':>10}")
        print("-"*70)
        print(f"\nDominant loss channel: {dominant_stage}")
        print(f"Total throughput:      {throughput:.4%} ({A:,} / {S:,})")
        print("="*70 + "\n")


# ═══════════════════════════════════════════════════════════════════════════
# HARDWARE MAPPING
# ═══════════════════════════════════════════════════════════════════════════

class HardwareFunnel:
    """
    Hardware implementation of the narrowing funnel.

    Maps abstract funnel stages to physical operations on the oscillator array.
    Each stage corresponds to a measurable filtering operation on the J-field.

    From §4.1 of build spec:
      S: Sum of |J_i|² across all elements (total energy)
      ℛ: Elements with PLV > threshold (phase-locked)
      𝒦: Elements matching expected frequency (spectral filter)
      𝒞: Connected components of phase-locked regions (spatial coherence)
      𝒫: Clusters persisting > τ_min (temporal stability)
      ℱ: |J_i| within ε of |J|_eq (amplitude fidelity)
      𝒜: Elements passing all 6 filters (final output)
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize hardware funnel mapper.

        Args:
            verbose: If True, print detailed hardware diagnostics
        """
        self.verbose = verbose

    def process_hardware(self, hw_state: HardwareState) -> FunnelOutput:
        """
        Process oscillator array through hardware-mapped funnel.

        Args:
            hw_state: Physical state of oscillator array

        Returns:
            FunnelOutput with hardware-measured stage counts
        """
        J = hw_state.J_field
        sigma = hw_state.sigma

        # Stage 1: S - Total energy in array
        S = self._measure_S(J)

        # Stage 2: ℛ - Phase-locked elements
        R_mask = self._measure_R(J, hw_state.plv_threshold)
        R = np.sum(R_mask)

        # Stage 3: 𝒦 - Frequency-matched elements
        K_mask = self._measure_K(J, sigma, hw_state.freq_tolerance) & R_mask
        K = np.sum(K_mask)

        # Stage 4: 𝒞 - Spatially coherent clusters
        C_mask, num_clusters = self._measure_C(K_mask)
        C = num_clusters

        # Stage 5: 𝒫 - Temporally persistent clusters
        # Note: Requires temporal history; here we estimate from spatial extent
        P_mask = self._measure_P(C_mask, hw_state.tau_min)
        P = np.sum(P_mask)

        # Stage 6: ℱ - Amplitude-verified elements
        F_mask = self._measure_F(J, sigma, hw_state.epsilon) & P_mask
        F = np.sum(F_mask)

        # Stage 7: 𝒜 - Elements passing all filters
        A = F  # Final count is fidelity-checked count

        # Compute losses
        losses = self._compute_hardware_losses(S, R, K, C, P, F, A)

        # Find dominant loss
        dominant_stage = max(losses.items(), key=lambda x: x[1])[0]

        # Total throughput
        throughput = A / S if S > 0 else 0.0

        # Filter thresholds used
        filter_coeffs = {
            'PLV_threshold': hw_state.plv_threshold,
            'freq_tolerance': hw_state.freq_tolerance,
            'tau_min': hw_state.tau_min,
            'epsilon': hw_state.epsilon,
            'sigma': sigma,
        }

        if self.verbose:
            self._print_hardware_pipeline(S, R, K, C, P, F, A, losses,
                                         dominant_stage, throughput, sigma)

        return FunnelOutput(
            S=S, R=int(R), K=int(K), C=C, P=int(P), F=int(F), A=A,
            losses=losses,
            dominant_loss_stage=dominant_stage,
            total_throughput=throughput,
            filter_coeffs=filter_coeffs
        )

    def _measure_S(self, J: np.ndarray) -> int:
        """
        S: Total signal count = sum of |J_i|² across all elements.

        This is the total energy in the oscillator array.
        """
        energy = np.sum(np.abs(J)**2)
        # Convert to integer signal count (normalized energy)
        return int(np.round(energy * 1000))  # Scale for discrete counts

    def _measure_R(self, J: np.ndarray, plv_threshold: float) -> np.ndarray:
        """
        ℛ: Elements with PLV > threshold (phase-locked).

        Phase Locking Value (PLV) measures phase coherence with neighbors.
        Returns boolean mask of phase-locked elements.
        """
        # Compute local phase coherence (simplified PLV)
        phases = np.angle(J)

        # For each element, compute phase coherence with neighbors
        # Using gradient as proxy for phase alignment
        phase_grad = np.gradient(phases)
        phase_coherence = 1.0 / (1.0 + np.abs(phase_grad[0]) + np.abs(phase_grad[1]))

        return phase_coherence > plv_threshold

    def _measure_K(self, J: np.ndarray, sigma: float,
                   freq_tolerance: float) -> np.ndarray:
        """
        𝒦: Elements matching expected frequency.

        Expected frequency ω₀ depends on σ via the governing equation.
        Returns boolean mask of frequency-matched elements.
        """
        # Expected equilibrium amplitude from governing equation
        if sigma > MU_P + BETA:
            J_eq = np.sqrt((sigma - MU_P - BETA) / LAMBDA)
        else:
            J_eq = 0.0

        # Elements near equilibrium amplitude are on-frequency
        amplitude = np.abs(J)
        freq_matched = np.abs(amplitude - J_eq) < (freq_tolerance * max(J_eq, 0.1))

        return freq_matched

    def _measure_C(self, K_mask: np.ndarray) -> Tuple[np.ndarray, int]:
        """
        𝒞: Connected components of phase-locked regions.

        Returns spatially coherent clusters as connected components.
        Returns (cluster_mask, num_clusters).
        """
        # Simple connected components via convolution
        # Each True cell connected to neighbors forms a cluster
        if not np.any(K_mask):
            return K_mask, 0

        # Count clusters using simple flood-fill algorithm
        labeled_array, num_clusters = self._label_connected_components(K_mask)

        return labeled_array > 0, num_clusters

    def _label_connected_components(self, binary_mask: np.ndarray) -> Tuple[np.ndarray, int]:
        """
        Label connected components in a binary mask (4-connectivity).

        Returns (labeled_array, num_components)
        """
        labeled = np.zeros_like(binary_mask, dtype=int)
        current_label = 0

        def flood_fill(i: int, j: int, label: int):
            """Recursive flood fill for 4-connected region."""
            if i < 0 or i >= binary_mask.shape[0] or j < 0 or j >= binary_mask.shape[1]:
                return
            if not binary_mask[i, j] or labeled[i, j] != 0:
                return

            labeled[i, j] = label

            # 4-connected neighbors
            flood_fill(i-1, j, label)
            flood_fill(i+1, j, label)
            flood_fill(i, j-1, label)
            flood_fill(i, j+1, label)

        # Find all connected components
        for i in range(binary_mask.shape[0]):
            for j in range(binary_mask.shape[1]):
                if binary_mask[i, j] and labeled[i, j] == 0:
                    current_label += 1
                    flood_fill(i, j, current_label)

        return labeled, current_label

    def _measure_P(self, C_mask: np.ndarray, tau_min: float) -> np.ndarray:
        """
        𝒫: Clusters persisting > τ_min.

        Temporal persistence requires history tracking.
        Here we estimate from spatial extent (larger clusters = more stable).
        """
        # Proxy: clusters with sufficient spatial extent are temporally stable
        # This is a simplification; real implementation needs temporal buffer

        # Simple dilation using convolution
        dilated = self._binary_dilation(C_mask, iterations=int(tau_min / 10))

        # Intersection gives "core" of stable clusters
        return C_mask & dilated

    def _binary_dilation(self, binary_mask: np.ndarray, iterations: int = 1) -> np.ndarray:
        """
        Simple binary dilation using 4-connectivity.

        Args:
            binary_mask: Input binary mask
            iterations: Number of dilation iterations

        Returns:
            Dilated binary mask
        """
        result = binary_mask.copy()

        for _ in range(iterations):
            dilated = result.copy()
            rows, cols = result.shape

            for i in range(rows):
                for j in range(cols):
                    if result[i, j]:
                        # Dilate to 4-connected neighbors
                        if i > 0:
                            dilated[i-1, j] = True
                        if i < rows - 1:
                            dilated[i+1, j] = True
                        if j > 0:
                            dilated[i, j-1] = True
                        if j < cols - 1:
                            dilated[i, j+1] = True

            result = dilated

        return result

    def _measure_F(self, J: np.ndarray, sigma: float, epsilon: float) -> np.ndarray:
        """
        ℱ: |J_i| within ε of |J|_eq (amplitude fidelity).

        Final fidelity check: elements at expected equilibrium amplitude.
        """
        if sigma > MU_P + BETA:
            J_eq = np.sqrt((sigma - MU_P - BETA) / LAMBDA)
        else:
            J_eq = 0.0

        amplitude = np.abs(J)
        fidelity_check = np.abs(amplitude - J_eq) < (epsilon * max(J_eq, 0.1))

        return fidelity_check

    def _compute_hardware_losses(self, S: int, R: int, K: int, C: int,
                                P: int, F: int, A: int) -> Dict[str, float]:
        """Compute losses for hardware pipeline."""
        def safe_loss(input_val: int, output_val: int) -> float:
            return (input_val - output_val) / input_val if input_val > 0 else 0.0

        return {
            'S→ℛ (energy→PLV)': safe_loss(S, R),
            'ℛ→𝒦 (PLV→freq)': safe_loss(R, K),
            '𝒦→𝒞 (freq→spatial)': safe_loss(K, C),
            '𝒞→𝒫 (spatial→temporal)': safe_loss(C, P),
            '𝒫→ℱ (temporal→amplitude)': safe_loss(P, F),
            'ℱ→𝒜 (amplitude→output)': safe_loss(F, A),
        }

    def _print_hardware_pipeline(self, S: int, R: int, K: int, C: int, P: int,
                                F: int, A: int, losses: Dict[str, float],
                                dominant_stage: str, throughput: float, sigma: float):
        """Print hardware pipeline diagnostics."""
        print("\n" + "="*80)
        print("HARDWARE-MAPPED NARROWING FUNNEL")
        print(f"σ = μ = {sigma:.3f}")
        print("="*80)
        print(f"\n{'Stage':<30} {'Count':>12} {'Loss':>12}")
        print("-"*80)
        print(f"{'S: Total energy':<30} {S:>12,} {'-':>12}")
        print(f"{'ℛ: Phase-locked elements':<30} {R:>12,} {losses['S→ℛ (energy→PLV)']:>11.1%}")
        print(f"{'𝒦: Frequency-matched':<30} {K:>12,} {losses['ℛ→𝒦 (PLV→freq)']:>11.1%}")
        print(f"{'𝒞: Spatial clusters':<30} {C:>12,} {losses['𝒦→𝒞 (freq→spatial)']:>11.1%}")
        print(f"{'𝒫: Persistent clusters':<30} {P:>12,} {losses['𝒞→𝒫 (spatial→temporal)']:>11.1%}")
        print(f"{'ℱ: Amplitude-verified':<30} {F:>12,} {losses['𝒫→ℱ (temporal→amplitude)']:>11.1%}")
        print(f"{'𝒜: Final output':<30} {A:>12,} {losses['ℱ→𝒜 (amplitude→output)']:>11.1%}")
        print("-"*80)
        print(f"\nDominant loss channel: {dominant_stage}")
        print(f"Total throughput:      {throughput:.4%}")
        print("="*80 + "\n")


# ═══════════════════════════════════════════════════════════════════════════
# SELF-CALIBRATING FILTER THRESHOLDS
# ═══════════════════════════════════════════════════════════════════════════

class AdaptiveFunnel(NarrowingFunnel):
    """
    Self-calibrating narrowing funnel with σ-dependent filter thresholds.

    From build spec §4.1: "The filter thresholds at each stage are functions
    of σ. At low σ, the filters are loose (most signals pass). At high σ,
    the filters tighten because the equilibrium is more precisely defined."
    """

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)

    def process_adaptive(self, metrics: SignalMetrics, sigma: float) -> FunnelOutput:
        """
        Process with σ-dependent adaptive filter thresholds.

        Args:
            metrics: Input signal metrics
            sigma: Current σ = μ value

        Returns:
            FunnelOutput with adaptive filtering applied
        """
        # Calibrate filter coefficients based on σ
        adaptive_metrics = self._calibrate_filters(metrics, sigma)

        # Process through standard pipeline with calibrated metrics
        return self.process(adaptive_metrics)

    def _calibrate_filters(self, metrics: SignalMetrics, sigma: float) -> SignalMetrics:
        """
        Calibrate filter thresholds as functions of σ.

        Filter tightness increases with σ:
          - Low σ (subcritical): loose filters, high throughput
          - σ → 1 (critical): tight filters, precise selection
        """
        # Compute tightness factor based on phase state
        if sigma < MU_P:  # Subcritical
            tightness = 0.5
        elif sigma < MU_S:  # Critical onset → sustained critical
            # Linear interpolation from 0.5 to 1.0
            tightness = 0.5 + 0.5 * (sigma - MU_P) / (MU_S - MU_P)
        elif sigma < MU_3:  # Sustained critical → supercritical
            tightness = 1.0
        else:  # Supercritical → singularity
            tightness = 1.0 + 0.5 * (sigma - MU_3) / (MU_4 - MU_3)

        # Adjust theta parameters based on tightness
        # Higher tightness → more selective filtering
        calibrated = SignalMetrics(
            interactions=metrics.interactions,
            theta_name=metrics.theta_name * tightness,
            theta_pol=min(1.0, metrics.theta_pol * tightness),
            theta_cap=max(0.1, metrics.theta_cap / tightness),  # Cap inversely related
            registered=metrics.registered
        )

        if self.verbose:
            print(f"\nAdaptive calibration at σ = {sigma:.3f}")
            print(f"  Phase state: {self._phase_state_name(sigma)}")
            print(f"  Tightness factor: {tightness:.3f}")
            print(f"  θ.name: {metrics.theta_name:.3f} → {calibrated.theta_name:.3f}")
            print(f"  θ.pol:  {metrics.theta_pol:.3f} → {calibrated.theta_pol:.3f}")
            print(f"  θ.cap:  {metrics.theta_cap:.3f} → {calibrated.theta_cap:.3f}\n")

        return calibrated

    def _phase_state_name(self, sigma: float) -> str:
        """Get human-readable phase state name."""
        if sigma < MU_P:
            return "Sub-critical"
        elif sigma < MU_P + BETA:
            return "Critical onset"
        elif sigma < MU_S:
            return "Critical (σ → 1)"
        elif sigma < MU_3:
            return "Sustained critical (K-formation)"
        elif sigma < MU_4:
            return "Super-critical"
        else:
            return "Singularity"


# ═══════════════════════════════════════════════════════════════════════════
# DEMONSTRATION AND VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

def demo_basic_funnel():
    """Demonstrate basic narrowing funnel operation."""
    print("\n" + "="*80)
    print("DEMO 1: Basic Narrowing Funnel")
    print("="*80)

    funnel = NarrowingFunnel(verbose=True)

    # Example signal metrics
    metrics = SignalMetrics(
        interactions=10000,
        theta_name=0.75,
        theta_pol=0.40,
        theta_cap=0.85,
        registered=0.95
    )

    output = funnel.process(metrics)

    print(f"\nInput: {metrics.interactions:,} interactions")
    print(f"Output: {output.A:,} admitted signals")
    print(f"Throughput: {output.total_throughput:.2%}")
    print(f"Bottleneck: {output.dominant_loss_stage}")


def demo_hardware_funnel():
    """Demonstrate hardware-mapped funnel with synthetic J-field."""
    print("\n" + "="*80)
    print("DEMO 2: Hardware-Mapped Funnel")
    print("="*80)

    # Create synthetic oscillator array (32x32 grid)
    N = 32
    sigma = 0.85  # Critical phase

    # Generate synthetic J-field with coherent region
    x = np.linspace(0, 2*np.pi, N)
    y = np.linspace(0, 2*np.pi, N)
    X, Y = np.meshgrid(x, y)

    # Equilibrium amplitude for this σ
    if sigma > MU_P + BETA:
        J_eq = np.sqrt((sigma - MU_P - BETA) / LAMBDA)
    else:
        J_eq = 0.0

    # Create field with phase coherence in center, noise at edges
    center_mask = (X - np.pi)**2 + (Y - np.pi)**2 < (np.pi/2)**2
    J_field = np.zeros((N, N), dtype=complex)

    # Coherent region
    phase_coherent = np.exp(1j * (X + Y)) * center_mask
    J_field = J_eq * phase_coherent

    # Add noise
    noise = 0.1 * J_eq * (np.random.randn(N, N) + 1j * np.random.randn(N, N))
    J_field += noise

    hw_state = HardwareState(
        J_field=J_field,
        sigma=sigma,
        plv_threshold=0.6,
        freq_tolerance=0.1,
        tau_min=5.0,
        epsilon=0.2
    )

    hw_funnel = HardwareFunnel(verbose=True)
    output = hw_funnel.process_hardware(hw_state)

    print(f"\nArray size: {N}×{N} = {N*N} elements")
    print(f"σ = μ = {sigma:.3f}")
    print(f"|J|_eq = {J_eq:.4f}")
    print(f"Final output: {output.A} coherent elements")


def demo_adaptive_funnel():
    """Demonstrate σ-dependent adaptive filtering."""
    print("\n" + "="*80)
    print("DEMO 3: Adaptive Self-Calibrating Funnel")
    print("="*80)

    adaptive_funnel = AdaptiveFunnel(verbose=True)

    # Fixed input metrics
    metrics = SignalMetrics(
        interactions=5000,
        theta_name=0.65,
        theta_pol=0.50,
        theta_cap=0.80,
        registered=0.90
    )

    # Test across different σ values
    sigma_values = [0.5, 0.75, 0.92, 0.995]

    results = []
    for sigma in sigma_values:
        output = adaptive_funnel.process_adaptive(metrics, sigma)
        results.append((sigma, output))

    print("\n" + "="*80)
    print("ADAPTIVE FILTERING COMPARISON")
    print("="*80)
    print(f"\n{'σ value':<12} {'Phase State':<25} {'Throughput':>12} {'Output':>10}")
    print("-"*80)

    for sigma, output in results:
        phase = adaptive_funnel._phase_state_name(sigma)
        print(f"{sigma:<12.3f} {phase:<25} {output.total_throughput:>11.2%} {output.A:>10,}")

    print("\nNote: Lower σ → looser filters → higher throughput")
    print("      Higher σ → tighter filters → more selective output")


def demo_loss_analysis():
    """Demonstrate dominant loss channel identification."""
    print("\n" + "="*80)
    print("DEMO 4: Loss Channel Analysis")
    print("="*80)

    funnel = NarrowingFunnel(verbose=False)

    # Scenario 1: Low capacity bottleneck
    print("\nScenario 1: Low Capacity (θ.cap = 0.3)")
    metrics1 = SignalMetrics(
        interactions=10000, theta_name=0.8, theta_pol=0.3, theta_cap=0.3, registered=0.95
    )
    out1 = funnel.process(metrics1)
    print(f"Dominant loss: {out1.dominant_loss_stage}")
    print(f"Loss magnitude: {out1.losses[out1.dominant_loss_stage]:.1%}")

    # Scenario 2: High polarization bottleneck
    print("\nScenario 2: High Polarization (θ.pol = 0.9)")
    metrics2 = SignalMetrics(
        interactions=10000, theta_name=0.8, theta_pol=0.9, theta_cap=0.8, registered=0.95
    )
    out2 = funnel.process(metrics2)
    print(f"Dominant loss: {out2.dominant_loss_stage}")
    print(f"Loss magnitude: {out2.losses[out2.dominant_loss_stage]:.1%}")

    # Scenario 3: Balanced pipeline
    print("\nScenario 3: Balanced Pipeline")
    metrics3 = SignalMetrics(
        interactions=10000, theta_name=0.7, theta_pol=0.5, theta_cap=0.7, registered=0.95
    )
    out3 = funnel.process(metrics3)
    print(f"Dominant loss: {out3.dominant_loss_stage}")
    print(f"Loss magnitude: {out3.losses[out3.dominant_loss_stage]:.1%}")

    print("\n" + "="*80)


if __name__ == '__main__':
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║              SEVEN-STAGE NARROWING FUNNEL PIPELINE                         ║")
    print("║                      σ = μ Implementation                                  ║")
    print("║                                                                            ║")
    print("║  Pipeline: S → ℛ → 𝒦 → 𝒞 → 𝒫 → ℱ → 𝒜                                       ║")
    print("║  Depth: L₄ = φ⁴ + φ⁻⁴ = 7 stages                                          ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()

    # Run all demonstrations
    demo_basic_funnel()
    demo_hardware_funnel()
    demo_adaptive_funnel()
    demo_loss_analysis()

    print("\n" + "="*80)
    print("σ = μ ⟐ Everything follows from the foundational identity.")
    print("="*80 + "\n")
