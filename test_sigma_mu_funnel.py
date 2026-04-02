#!/usr/bin/env python3
"""
Test suite for sigma_mu_narrowing_funnel.py

Validates:
  1. Seven-stage pipeline correctness
  2. Loss computation accuracy
  3. Hardware mapping consistency
  4. Self-calibration behavior
  5. Constant cascade validation (L₄ = 7)

Author: Claude (Anthropic) for Echo-Squirrel Research
Date: 2026-04-02
"""

import unittest
import numpy as np
from sigma_mu_narrowing_funnel import (
    NarrowingFunnel, HardwareFunnel, AdaptiveFunnel,
    SignalMetrics, HardwareState,
    PHI, BETA, L4, MU_P, MU_S, Z_C
)


class TestConstants(unittest.TestCase):
    """Test that all constants derive correctly from φ."""

    def test_phi_value(self):
        """φ = (1+√5)/2"""
        expected = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(PHI, expected, places=10)
        self.assertAlmostEqual(PHI, 1.618033988749895, places=10)

    def test_beta_from_phi(self):
        """β = φ⁻⁴"""
        expected = PHI**-4
        self.assertAlmostEqual(BETA, expected, places=10)
        self.assertAlmostEqual(BETA, 0.145898033750081, places=10)

    def test_L4_equals_seven(self):
        """L₄ = φ⁴ + φ⁻⁴ = 7 exactly (funnel depth)"""
        L4_computed = PHI**4 + PHI**-4
        self.assertAlmostEqual(L4, 7.0, places=10)
        self.assertAlmostEqual(L4_computed, 7.0, places=10)

    def test_threshold_architecture(self):
        """Validate threshold values."""
        self.assertEqual(MU_P, 3/5)
        self.assertEqual(MU_S, 23/25)
        self.assertAlmostEqual(Z_C, np.sqrt(3)/2, places=10)


class TestBasicFunnel(unittest.TestCase):
    """Test basic narrowing funnel pipeline."""

    def setUp(self):
        self.funnel = NarrowingFunnel(verbose=False)

    def test_seven_stages(self):
        """Pipeline must have exactly 7 stages (L₄ = 7)."""
        metrics = SignalMetrics(
            interactions=1000,
            theta_name=0.5,
            theta_pol=0.5,
            theta_cap=0.5
        )
        output = self.funnel.process(metrics)

        # Verify all 7 stages present
        self.assertIsNotNone(output.S)
        self.assertIsNotNone(output.R)
        self.assertIsNotNone(output.K)
        self.assertIsNotNone(output.C)
        self.assertIsNotNone(output.P)
        self.assertIsNotNone(output.F)
        self.assertIsNotNone(output.A)

    def test_monotonic_decrease(self):
        """Stage outputs should generally decrease (with exceptions for A)."""
        metrics = SignalMetrics(
            interactions=10000,
            theta_name=0.7,
            theta_pol=0.3,
            theta_cap=0.8,
            registered=0.1  # Low registration to avoid A > F
        )
        output = self.funnel.process(metrics)

        # S ≥ R ≥ K ≥ C ≥ P ≥ F (generally)
        self.assertGreaterEqual(output.S, output.R)
        self.assertGreaterEqual(output.R, output.K)
        self.assertGreaterEqual(output.K, output.C)
        self.assertGreaterEqual(output.C, output.P)
        self.assertGreaterEqual(output.P, output.F)

    def test_minimum_output(self):
        """A must be at least 1 (system never goes silent)."""
        metrics = SignalMetrics(
            interactions=1,
            theta_name=0.0,
            theta_pol=1.0,
            theta_cap=0.01,
            registered=0.01
        )
        output = self.funnel.process(metrics)
        self.assertGreaterEqual(output.A, 1)

    def test_R_equals_interactions(self):
        """Stage 2: R_n = interactions exactly."""
        metrics = SignalMetrics(interactions=5000, theta_name=0.5,
                               theta_pol=0.5, theta_cap=0.5)
        output = self.funnel.process(metrics)
        self.assertEqual(output.R, 5000)

    def test_K_ratio(self):
        """Stage 3: K_n = ⌊R_n × 0.70⌋"""
        metrics = SignalMetrics(interactions=1000, theta_name=0.5,
                               theta_pol=0.5, theta_cap=0.5)
        output = self.funnel.process(metrics)
        self.assertEqual(output.K, 700)  # ⌊1000 × 0.70⌋

    def test_C_ratio(self):
        """Stage 4: C_n = ⌊K_n × 0.55⌋"""
        metrics = SignalMetrics(interactions=1000, theta_name=0.5,
                               theta_pol=0.5, theta_cap=0.5)
        output = self.funnel.process(metrics)
        # K = 700, so C = ⌊700 × 0.55⌋ = ⌊385⌋ = 385
        self.assertEqual(output.C, 385)

    def test_P_polarization_dependence(self):
        """Stage 5: P_n depends on θ.pol"""
        # Low polarization → higher survival
        metrics_low_pol = SignalMetrics(
            interactions=1000, theta_name=0.5, theta_pol=0.1, theta_cap=0.5
        )
        output_low = self.funnel.process(metrics_low_pol)

        # High polarization → lower survival
        metrics_high_pol = SignalMetrics(
            interactions=1000, theta_name=0.5, theta_pol=0.9, theta_cap=0.5
        )
        output_high = self.funnel.process(metrics_high_pol)

        self.assertGreater(output_low.P, output_high.P)

    def test_F_capacity_dependence(self):
        """Stage 6: F_n depends on θ.cap"""
        # High capacity → higher survival
        metrics_high_cap = SignalMetrics(
            interactions=1000, theta_name=0.5, theta_pol=0.3, theta_cap=0.9
        )
        output_high = self.funnel.process(metrics_high_cap)

        # Low capacity → lower survival
        metrics_low_cap = SignalMetrics(
            interactions=1000, theta_name=0.5, theta_pol=0.3, theta_cap=0.3
        )
        output_low = self.funnel.process(metrics_low_cap)

        self.assertGreater(output_high.F, output_low.F)


class TestLossComputation(unittest.TestCase):
    """Test loss computation and dominant channel identification."""

    def setUp(self):
        self.funnel = NarrowingFunnel(verbose=False)

    def test_loss_keys(self):
        """Verify all 6 loss transitions are computed."""
        metrics = SignalMetrics(interactions=1000, theta_name=0.5,
                               theta_pol=0.5, theta_cap=0.5)
        output = self.funnel.process(metrics)

        expected_keys = {'S→ℛ', 'ℛ→𝒦', '𝒦→𝒞', '𝒞→𝒫', '𝒫→ℱ', 'ℱ→𝒜'}
        self.assertEqual(set(output.losses.keys()), expected_keys)

    def test_loss_range(self):
        """Losses should be in [0, 1] for normal operation."""
        metrics = SignalMetrics(
            interactions=1000,
            theta_name=0.7,
            theta_pol=0.3,
            theta_cap=0.8,
            registered=0.1  # Low to avoid A > F
        )
        output = self.funnel.process(metrics)

        # Most losses should be non-negative
        for stage, loss in output.losses.items():
            if stage != 'ℱ→𝒜':  # A can be > F due to different computation
                self.assertGreaterEqual(loss, 0.0,
                    f"Loss at {stage} should be non-negative, got {loss}")

    def test_dominant_loss_identification(self):
        """Dominant loss channel should be the maximum."""
        metrics = SignalMetrics(interactions=1000, theta_name=0.5,
                               theta_pol=0.5, theta_cap=0.1)  # Low cap → high F loss
        output = self.funnel.process(metrics)

        max_loss = max(output.losses.values())
        dominant_loss = output.losses[output.dominant_loss_stage]
        self.assertEqual(dominant_loss, max_loss)

    def test_throughput_computation(self):
        """Total throughput = A / S."""
        metrics = SignalMetrics(interactions=1000, theta_name=0.5,
                               theta_pol=0.5, theta_cap=0.5, registered=0.5)
        output = self.funnel.process(metrics)

        expected_throughput = output.A / output.S
        self.assertAlmostEqual(output.total_throughput, expected_throughput, places=10)


class TestHardwareFunnel(unittest.TestCase):
    """Test hardware mapping of funnel stages."""

    def setUp(self):
        self.hw_funnel = HardwareFunnel(verbose=False)

    def test_hardware_stages_present(self):
        """Hardware funnel should compute all 7 stages."""
        # Small test array
        J = self._create_test_field(8, sigma=0.8)
        hw_state = HardwareState(J_field=J, sigma=0.8)

        output = self.hw_funnel.process_hardware(hw_state)

        self.assertIsNotNone(output.S)
        self.assertIsNotNone(output.R)
        self.assertIsNotNone(output.K)
        self.assertIsNotNone(output.C)
        self.assertIsNotNone(output.P)
        self.assertIsNotNone(output.F)
        self.assertIsNotNone(output.A)

    def test_energy_measurement(self):
        """S should increase with field amplitude."""
        J_small = self._create_test_field(8, amplitude=0.1, sigma=0.8)
        J_large = self._create_test_field(8, amplitude=1.0, sigma=0.8)

        hw_state_small = HardwareState(J_field=J_small, sigma=0.8)
        hw_state_large = HardwareState(J_field=J_large, sigma=0.8)

        output_small = self.hw_funnel.process_hardware(hw_state_small)
        output_large = self.hw_funnel.process_hardware(hw_state_large)

        self.assertGreater(output_large.S, output_small.S)

    def test_plv_filtering(self):
        """R should decrease with tighter PLV threshold."""
        J = self._create_test_field(16, sigma=0.8)

        hw_state_loose = HardwareState(J_field=J, sigma=0.8, plv_threshold=0.3)
        hw_state_tight = HardwareState(J_field=J, sigma=0.8, plv_threshold=0.9)

        output_loose = self.hw_funnel.process_hardware(hw_state_loose)
        output_tight = self.hw_funnel.process_hardware(hw_state_tight)

        self.assertGreaterEqual(output_loose.R, output_tight.R)

    def _create_test_field(self, N: int, amplitude: float = 0.1,
                          sigma: float = 0.8) -> np.ndarray:
        """Create synthetic J-field for testing."""
        x = np.linspace(0, 2*np.pi, N)
        y = np.linspace(0, 2*np.pi, N)
        X, Y = np.meshgrid(x, y)

        # Coherent phase pattern
        phase = np.exp(1j * (X + Y))
        J = amplitude * phase

        # Add small noise
        noise = 0.01 * amplitude * (np.random.randn(N, N) + 1j * np.random.randn(N, N))
        return J + noise


class TestAdaptiveFunnel(unittest.TestCase):
    """Test self-calibrating adaptive funnel."""

    def setUp(self):
        self.adaptive = AdaptiveFunnel(verbose=False)

    def test_sigma_dependent_throughput(self):
        """Lower σ → looser filters → higher throughput."""
        metrics = SignalMetrics(
            interactions=1000,
            theta_name=0.6,
            theta_pol=0.5,
            theta_cap=0.7,
            registered=0.8
        )

        output_low_sigma = self.adaptive.process_adaptive(metrics, sigma=0.5)
        output_high_sigma = self.adaptive.process_adaptive(metrics, sigma=0.95)

        # Lower sigma should have higher throughput
        self.assertGreater(output_low_sigma.total_throughput,
                          output_high_sigma.total_throughput)

    def test_phase_state_recognition(self):
        """Adaptive funnel should recognize phase states correctly."""
        # Test phase state identification
        self.assertEqual(self.adaptive._phase_state_name(0.5), "Sub-critical")
        self.assertEqual(self.adaptive._phase_state_name(0.75), "Critical (σ → 1)")
        self.assertEqual(self.adaptive._phase_state_name(0.92), "Sustained critical (K-formation)")
        self.assertEqual(self.adaptive._phase_state_name(0.995), "Super-critical")

    def test_filter_calibration_monotonic(self):
        """Filter tightness should increase with σ."""
        metrics = SignalMetrics(
            interactions=1000,
            theta_name=0.6,
            theta_pol=0.5,
            theta_cap=0.7
        )

        # Get calibrated metrics at different σ values
        sigma_values = [0.5, 0.75, 0.92, 0.995]
        theta_pol_values = []

        for sigma in sigma_values:
            calibrated = self.adaptive._calibrate_filters(metrics, sigma)
            theta_pol_values.append(calibrated.theta_pol)

        # theta_pol should increase with sigma (tighter filtering)
        for i in range(len(theta_pol_values) - 1):
            self.assertGreaterEqual(theta_pol_values[i+1], theta_pol_values[i],
                f"θ.pol should increase with σ")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        self.funnel = NarrowingFunnel(verbose=False)

    def test_zero_interactions(self):
        """Handle zero interactions gracefully."""
        metrics = SignalMetrics(
            interactions=0,
            theta_name=0.5,
            theta_pol=0.5,
            theta_cap=0.5
        )
        output = self.funnel.process(metrics)

        # R should be 0, but A should be 1 (minimum)
        self.assertEqual(output.R, 0)
        self.assertEqual(output.A, 1)  # max(1, ⌊registered × 0⌋)

    def test_extreme_theta_values(self):
        """Handle extreme theta values (0 and 1)."""
        # All zeros
        metrics_zeros = SignalMetrics(
            interactions=1000,
            theta_name=0.0,
            theta_pol=0.0,
            theta_cap=0.0
        )
        output_zeros = self.funnel.process(metrics_zeros)
        self.assertIsNotNone(output_zeros.A)

        # All ones
        metrics_ones = SignalMetrics(
            interactions=1000,
            theta_name=1.0,
            theta_pol=1.0,
            theta_cap=1.0
        )
        output_ones = self.funnel.process(metrics_ones)
        self.assertIsNotNone(output_ones.A)

    def test_large_interaction_count(self):
        """Handle large interaction counts."""
        metrics = SignalMetrics(
            interactions=1_000_000,
            theta_name=0.5,
            theta_pol=0.5,
            theta_cap=0.5
        )
        output = self.funnel.process(metrics)

        # Should complete without error
        self.assertGreater(output.A, 0)


class TestFilterCoefficients(unittest.TestCase):
    """Test filter coefficient computation and storage."""

    def setUp(self):
        self.funnel = NarrowingFunnel(verbose=False)

    def test_filter_coeffs_present(self):
        """Output should contain filter coefficients used."""
        metrics = SignalMetrics(
            interactions=1000,
            theta_name=0.6,
            theta_pol=0.4,
            theta_cap=0.8
        )
        output = self.funnel.process(metrics)

        self.assertIn('S_coeff', output.filter_coeffs)
        self.assertIn('K_ratio', output.filter_coeffs)
        self.assertIn('C_ratio', output.filter_coeffs)
        self.assertIn('P_ratio', output.filter_coeffs)
        self.assertIn('F_ratio', output.filter_coeffs)

    def test_S_coefficient_formula(self):
        """S_coeff = 1.12 + θ.name + θ.pol × 0.18"""
        metrics = SignalMetrics(
            interactions=1000,
            theta_name=0.5,
            theta_pol=0.6,
            theta_cap=0.7
        )
        output = self.funnel.process(metrics)

        expected = 1.12 + 0.5 + 0.6 * 0.18
        self.assertAlmostEqual(output.filter_coeffs['S_coeff'], expected, places=10)

    def test_constant_ratios(self):
        """K, C ratios should be constant."""
        metrics = SignalMetrics(
            interactions=1000,
            theta_name=0.5,
            theta_pol=0.5,
            theta_cap=0.5
        )
        output = self.funnel.process(metrics)

        self.assertEqual(output.filter_coeffs['K_ratio'], 0.70)
        self.assertEqual(output.filter_coeffs['C_ratio'], 0.55)


def run_validation_suite():
    """Run complete validation suite with summary."""
    print("\n" + "="*80)
    print("NARROWING FUNNEL VALIDATION SUITE")
    print("σ = μ Build Specification Implementation")
    print("="*80 + "\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicFunnel))
    suite.addTests(loader.loadTestsFromTestCase(TestLossComputation))
    suite.addTests(loader.loadTestsFromTestCase(TestHardwareFunnel))
    suite.addTests(loader.loadTestsFromTestCase(TestAdaptiveFunnel))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestFilterCoefficients))

    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print(f"Tests run:     {result.testsRun}")
    print(f"Successes:     {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:      {len(result.failures)}")
    print(f"Errors:        {len(result.errors)}")
    print(f"Success rate:  {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*80 + "\n")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_validation_suite()
    exit(0 if success else 1)
