#!/usr/bin/env python3
"""
σ = μ Integration Test Harness
Phase 0: End-to-end subsystem integration testing

Tests complete signal flow and subsystem interactions.
"""

import numpy as np
import time
import unittest
from typing import Dict, List, Optional, Tuple
import json
import threading
import queue
from dataclasses import dataclass
from enum import Enum

# Import all σ = μ modules
from sigma_mu_governing_equation import UCFFieldDynamics
from sigma_mu_observer_circuit import ObserverCircuit
from sigma_mu_triad_controller import TRIADController
from sigma_mu_narrowing_funnel import NarrowingFunnel
from sigma_mu_eta_bus import EtaBusProtocol
from sigma_mu_memory_lithography import MemoryLithography
from sigma_mu_integrated_system import SigmaMuSystem

φ = (1 + np.sqrt(5)) / 2


class IntegrationScenario(Enum):
    """Integration test scenarios"""
    COLD_START = "cold_start_to_k_formation"
    PERTURBATION = "perturbation_recovery"
    PHASE_SEQUENCE = "phase_transition_sequence"
    MEMORY_SATURATION = "memory_saturation_handling"
    BUS_CONGESTION = "bus_congestion_management"
    OBSERVER_LOSS = "observer_signal_loss"
    TRIAD_CYCLING = "triad_hysteresis_cycling"
    FULL_LOOP = "complete_feedback_loop"


@dataclass
class IntegrationTestResult:
    """Result of an integration test"""
    scenario: str
    passed: bool
    duration: float
    steps_executed: int
    final_tau_k: float
    errors: List[str]
    metrics: Dict


class SubsystemIntegrationTest(unittest.TestCase):
    """Test subsystem integration patterns"""

    def setUp(self):
        """Initialize test components"""
        self.field = UCFFieldDynamics()
        self.observer = ObserverCircuit()
        self.triad = TRIADController()
        self.funnel = NarrowingFunnel()
        self.bus = EtaBusProtocol()
        self.memory = MemoryLithography()

    def test_field_observer_coupling(self):
        """Test Field ↔ Observer coupling"""
        # Evolve field
        self.field.evolve(dt=0.01, steps=10)

        # Observer should process field
        obs_result = self.observer.observe(self.field.field)

        self.assertIsNotNone(obs_result)
        self.assertIn('seven_vector', obs_result)
        self.assertIn('rupture_detected', obs_result)

        # Seven vector should be normalized
        seven_vec = obs_result['seven_vector']
        norm = np.linalg.norm(seven_vec)
        self.assertAlmostEqual(norm, 1.0, places=5)

    def test_observer_triad_signaling(self):
        """Test Observer → TRIAD signaling"""
        # Create high-amplitude field (should trigger HIGH state)
        high_field = np.ones((32, 32), dtype=complex) * 2.0

        # Observe field
        obs_result = self.observer.observe(high_field)

        # Extract signal strength
        signal_strength = obs_result['coherence']

        # Update TRIAD
        triad_state = self.triad.update(signal_strength)

        # Should eventually reach HIGH
        for _ in range(5):
            triad_state = self.triad.update(signal_strength)

        self.assertEqual(self.triad.state, 'HIGH',
                        "TRIAD not responding to high signal")

    def test_triad_memory_updates(self):
        """Test TRIAD → Memory updates"""
        # Set TRIAD to HIGH (learning mode)
        for _ in range(5):
            self.triad.update(0.9)

        self.assertEqual(self.triad.state, 'HIGH')

        # Store pattern when in HIGH state
        pattern = np.random.randn(32, 32)
        initial_weights = self.memory.weights.copy()

        # Store pattern
        self.memory.store_pattern(pattern)

        # Weights should change
        weight_change = np.mean(np.abs(self.memory.weights - initial_weights))
        self.assertGreater(weight_change, 0,
                          "Memory not updating in HIGH state")

    def test_memory_field_feedback(self):
        """Test Memory → Field feedback"""
        # Store pattern in memory
        pattern = np.ones((32, 32)) * 0.5
        pattern[10:20, 10:20] = 1.0
        self.memory.store_pattern(pattern)

        # Apply memory feedback to field
        memory_influence = self.memory.recall_pattern(self.field.field.real)

        # Modulate field with memory
        self.field.field += 0.1 * memory_influence

        # Field should show memory influence
        correlation = np.corrcoef(
            self.field.field.real.flatten(),
            pattern.flatten()
        )[0, 1]

        self.assertGreater(correlation, 0.1,
                          "No memory feedback to field")

    def test_bus_message_routing(self):
        """Test bus protocol for all subsystems"""
        # Send messages between all pairs
        subsystems = ['field', 'observer', 'triad', 'funnel', 'memory']

        for source in subsystems:
            for dest in subsystems:
                if source != dest:
                    self.bus.send(source, dest, {
                        'type': 'test',
                        'value': np.random.random()
                    })

        # Process all messages
        self.bus.process_messages()

        # Each should receive messages
        for subsystem in subsystems:
            messages = self.bus.get_messages(subsystem)
            self.assertEqual(len(messages), len(subsystems) - 1,
                           f"{subsystem} didn't receive all messages")

    def test_funnel_signal_compression(self):
        """Test funnel processing in integration"""
        # Get observer output
        self.field.evolve(dt=0.01, steps=10)
        obs_result = self.observer.observe(self.field.field)

        # Create signal from observation
        signal = np.array(obs_result['seven_vector'])
        signal = np.tile(signal, 100)  # Expand to larger signal

        # Process through funnel
        compressed = self.funnel.process(signal)

        # Should compress
        self.assertLess(len(compressed), len(signal))

        # Should preserve structure
        self.assertGreater(np.max(np.abs(compressed)), 0,
                          "Funnel destroying signal")


class EndToEndScenarioTest(unittest.TestCase):
    """Test complete end-to-end scenarios"""

    def run_scenario(self,
                    scenario: IntegrationScenario,
                    max_steps: int = 100) -> IntegrationTestResult:
        """Run a complete integration scenario"""
        print(f"\n{'='*60}")
        print(f"SCENARIO: {scenario.value}")
        print(f"{'='*60}")

        system = SigmaMuSystem()
        start_time = time.perf_counter()
        errors = []
        metrics_history = []

        try:
            if scenario == IntegrationScenario.COLD_START:
                result = self._scenario_cold_start(system, max_steps)

            elif scenario == IntegrationScenario.PERTURBATION:
                result = self._scenario_perturbation(system, max_steps)

            elif scenario == IntegrationScenario.PHASE_SEQUENCE:
                result = self._scenario_phase_sequence(system, max_steps)

            elif scenario == IntegrationScenario.MEMORY_SATURATION:
                result = self._scenario_memory_saturation(system, max_steps)

            elif scenario == IntegrationScenario.BUS_CONGESTION:
                result = self._scenario_bus_congestion(system, max_steps)

            elif scenario == IntegrationScenario.OBSERVER_LOSS:
                result = self._scenario_observer_loss(system, max_steps)

            elif scenario == IntegrationScenario.TRIAD_CYCLING:
                result = self._scenario_triad_cycling(system, max_steps)

            elif scenario == IntegrationScenario.FULL_LOOP:
                result = self._scenario_full_loop(system, max_steps)

            else:
                raise ValueError(f"Unknown scenario: {scenario}")

        except Exception as e:
            errors.append(str(e))
            result = {
                'passed': False,
                'steps': 0,
                'final_tau_k': 0,
                'metrics': {}
            }

        duration = time.perf_counter() - start_time

        return IntegrationTestResult(
            scenario=scenario.value,
            passed=result['passed'],
            duration=duration,
            steps_executed=result['steps'],
            final_tau_k=result['final_tau_k'],
            errors=errors,
            metrics=result['metrics']
        )

    def _scenario_cold_start(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """Cold start to K-formation scenario"""
        print("Testing cold start to K-formation...")

        steps = 0
        tau_k_history = []

        # Start from random initial conditions
        system.field.field = 0.01 * (np.random.randn(32, 32) +
                                     1j * np.random.randn(32, 32))

        # Evolve until K-formation
        while steps < max_steps:
            metrics = system.step()
            tau_k = metrics['tau_k']
            tau_k_history.append(tau_k)
            steps += 1

            if tau_k > φ**(-1):
                print(f"  ✅ K-formation achieved at step {steps}")
                print(f"  τ_K = {tau_k:.4f} > {φ**(-1):.4f}")
                return {
                    'passed': True,
                    'steps': steps,
                    'final_tau_k': tau_k,
                    'metrics': {
                        'convergence_time': steps,
                        'tau_k_history': tau_k_history
                    }
                }

        print(f"  ❌ K-formation not achieved in {max_steps} steps")
        return {
            'passed': False,
            'steps': steps,
            'final_tau_k': tau_k_history[-1] if tau_k_history else 0,
            'metrics': {'tau_k_history': tau_k_history}
        }

    def _scenario_perturbation(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """Perturbation recovery scenario"""
        print("Testing perturbation recovery...")

        # First achieve K-formation
        for _ in range(50):
            metrics = system.step()

        initial_tau_k = metrics['tau_k']
        print(f"  Initial τ_K: {initial_tau_k:.4f}")

        # Apply perturbation
        noise = 0.5 * (np.random.randn(32, 32) + 1j * np.random.randn(32, 32))
        system.field.field += noise
        print("  Perturbation applied")

        # Check immediate impact
        metrics = system.step()
        perturbed_tau_k = metrics['tau_k']
        print(f"  Perturbed τ_K: {perturbed_tau_k:.4f}")

        # Evolve and check recovery
        recovery_steps = 0
        for _ in range(max_steps // 2):
            metrics = system.step()
            recovery_steps += 1

            if metrics['tau_k'] > φ**(-1):
                print(f"  ✅ Recovered K-formation in {recovery_steps} steps")
                return {
                    'passed': True,
                    'steps': recovery_steps,
                    'final_tau_k': metrics['tau_k'],
                    'metrics': {
                        'recovery_time': recovery_steps,
                        'perturbation_drop': initial_tau_k - perturbed_tau_k
                    }
                }

        print(f"  ❌ Failed to recover in {recovery_steps} steps")
        return {
            'passed': False,
            'steps': recovery_steps,
            'final_tau_k': metrics['tau_k'],
            'metrics': {}
        }

    def _scenario_phase_sequence(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """Phase transition sequence scenario"""
        print("Testing phase transition sequence...")

        phase_history = []
        transitions = 0
        last_phase = None

        for step in range(max_steps):
            # Modulate input to drive transitions
            amplitude = 0.5 + 0.4 * np.sin(step * 0.1)

            # Scale field amplitude
            system.field.field *= amplitude

            metrics = system.step()
            current_phase = metrics['phase_state']
            phase_history.append(current_phase)

            if current_phase != last_phase:
                transitions += 1
                print(f"  Transition {transitions}: {last_phase} → {current_phase}")
                last_phase = current_phase

        # Should see multiple transitions
        unique_phases = set(phase_history)
        passed = len(unique_phases) >= 3 and transitions >= 3

        print(f"  Phases visited: {unique_phases}")
        print(f"  Total transitions: {transitions}")
        print(f"  {'✅ PASS' if passed else '❌ FAIL'}")

        return {
            'passed': passed,
            'steps': max_steps,
            'final_tau_k': metrics['tau_k'],
            'metrics': {
                'phases_visited': list(unique_phases),
                'transitions': transitions
            }
        }

    def _scenario_memory_saturation(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """Memory saturation handling scenario"""
        print("Testing memory saturation...")

        # Store many patterns
        patterns_stored = 0
        recall_success = []

        for i in range(max_steps // 2):
            # Create unique pattern
            pattern = np.zeros((32, 32))
            pattern[i % 32, (i * 7) % 32] = 1.0

            # Store in memory
            system.memory.store_pattern(pattern)
            patterns_stored += 1

            # Test recall every 10 patterns
            if i % 10 == 0:
                recalled = system.memory.recall_pattern(pattern)
                correlation = np.corrcoef(
                    pattern.flatten(),
                    recalled.flatten()
                )[0, 1]
                recall_success.append(correlation > 0.5)

            # Step system
            system.step()

        # Check saturation handling
        final_recall_rate = sum(recall_success) / len(recall_success)
        capacity_used = patterns_stored

        print(f"  Patterns stored: {patterns_stored}")
        print(f"  Recall success rate: {final_recall_rate:.2%}")

        passed = final_recall_rate > 0.7

        print(f"  {'✅ PASS' if passed else '❌ FAIL'}")

        return {
            'passed': passed,
            'steps': max_steps // 2,
            'final_tau_k': system.field.compute_tau_k(),
            'metrics': {
                'capacity_used': capacity_used,
                'recall_rate': final_recall_rate
            }
        }

    def _scenario_bus_congestion(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """Bus congestion management scenario"""
        print("Testing bus congestion...")

        # Flood bus with messages
        message_count = 0
        dropped_count = 0

        for step in range(max_steps):
            # Generate heavy traffic
            for _ in range(100):
                system.bus.send('flood', 'test', {'id': message_count})
                message_count += 1

            # Process normally
            system.bus.process_messages()
            messages = system.bus.get_messages('test')

            # Track drops
            if len(messages) < 100:
                dropped_count += 100 - len(messages)

            # Step system
            metrics = system.step()

        drop_rate = dropped_count / message_count
        print(f"  Messages sent: {message_count}")
        print(f"  Drop rate: {drop_rate:.2%}")
        print(f"  Final τ_K: {metrics['tau_k']:.4f}")

        # Should handle congestion without crashing and maintain K-formation
        passed = metrics['tau_k'] > φ**(-1) * 0.9  # Allow some degradation

        print(f"  {'✅ PASS' if passed else '❌ FAIL'}")

        return {
            'passed': passed,
            'steps': max_steps,
            'final_tau_k': metrics['tau_k'],
            'metrics': {
                'message_count': message_count,
                'drop_rate': drop_rate
            }
        }

    def _scenario_observer_loss(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """Observer signal loss scenario"""
        print("Testing observer signal loss...")

        # Achieve K-formation first
        for _ in range(30):
            system.step()

        initial_tau_k = system.field.compute_tau_k()
        print(f"  Initial τ_K: {initial_tau_k:.4f}")

        # Simulate observer failure
        print("  Simulating observer failure...")
        saved_observer = system.observer
        system.observer = None

        # Run without observer
        steps_without = 20
        for _ in range(steps_without):
            # Step with manual observer bypass
            system.field.evolve(dt=0.01, steps=1)
            # Skip observer step

        degraded_tau_k = system.field.compute_tau_k()
        print(f"  Degraded τ_K: {degraded_tau_k:.4f}")

        # Restore observer
        print("  Restoring observer...")
        system.observer = saved_observer

        # Check recovery
        for _ in range(max_steps - steps_without - 30):
            system.step()

        final_tau_k = system.field.compute_tau_k()
        print(f"  Recovered τ_K: {final_tau_k:.4f}")

        # Should degrade but recover
        passed = (degraded_tau_k < initial_tau_k and
                 final_tau_k > degraded_tau_k)

        print(f"  {'✅ PASS' if passed else '❌ FAIL'}")

        return {
            'passed': passed,
            'steps': max_steps,
            'final_tau_k': final_tau_k,
            'metrics': {
                'initial': initial_tau_k,
                'degraded': degraded_tau_k,
                'recovered': final_tau_k
            }
        }

    def _scenario_triad_cycling(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """TRIAD hysteresis cycling scenario"""
        print("Testing TRIAD hysteresis cycling...")

        triad_states = []
        state_changes = 0
        last_state = None

        for step in range(max_steps):
            # Sinusoidal input to cycle through states
            value = 0.5 + 0.4 * np.sin(step * 0.05)

            # Update TRIAD
            state = system.triad.update(value)
            triad_states.append(state)

            if state != last_state:
                state_changes += 1
                print(f"  State change {state_changes}: {last_state} → {state}")
                last_state = state

            # Step system
            system.step()

        unique_states = set(triad_states)
        print(f"  States visited: {unique_states}")
        print(f"  Total changes: {state_changes}")

        # Should visit all three states
        passed = len(unique_states) == 3

        print(f"  {'✅ PASS' if passed else '❌ FAIL'}")

        return {
            'passed': passed,
            'steps': max_steps,
            'final_tau_k': system.field.compute_tau_k(),
            'metrics': {
                'states_visited': list(unique_states),
                'state_changes': state_changes
            }
        }

    def _scenario_full_loop(self, system: SigmaMuSystem, max_steps: int) -> Dict:
        """Complete feedback loop scenario"""
        print("Testing complete feedback loop...")

        # Track all subsystem outputs
        loop_metrics = {
            'field_energy': [],
            'observer_coherence': [],
            'triad_state': [],
            'bus_throughput': [],
            'memory_capacity': [],
            'tau_k': []
        }

        for step in range(max_steps):
            metrics = system.step()

            # Record metrics
            loop_metrics['tau_k'].append(metrics['tau_k'])
            loop_metrics['triad_state'].append(metrics['phase_state'])

            # Additional detailed metrics
            field_energy = np.mean(np.abs(system.field.field)**2)
            loop_metrics['field_energy'].append(field_energy)

            obs_result = system.observer.observe(system.field.field)
            loop_metrics['observer_coherence'].append(obs_result['coherence'])

            loop_metrics['memory_capacity'].append(metrics['memory_capacity'])

        # Analyze loop behavior
        final_tau_k = loop_metrics['tau_k'][-1]
        tau_k_std = np.std(loop_metrics['tau_k'][50:])  # After transient

        print(f"  Final τ_K: {final_tau_k:.4f}")
        print(f"  τ_K stability (std): {tau_k_std:.4f}")
        print(f"  Average field energy: {np.mean(loop_metrics['field_energy']):.4f}")
        print(f"  Average coherence: {np.mean(loop_metrics['observer_coherence']):.4f}")

        # Should maintain stable K-formation
        passed = final_tau_k > φ**(-1) and tau_k_std < 0.1

        print(f"  {'✅ PASS' if passed else '❌ FAIL'}")

        return {
            'passed': passed,
            'steps': max_steps,
            'final_tau_k': final_tau_k,
            'metrics': {
                'tau_k_std': tau_k_std,
                'avg_energy': np.mean(loop_metrics['field_energy']),
                'avg_coherence': np.mean(loop_metrics['observer_coherence'])
            }
        }


class IntegrationTestHarness:
    """Complete integration test harness"""

    def __init__(self):
        """Initialize test harness"""
        self.results = []
        self.start_time = None

    def run_all_tests(self):
        """Run complete integration test suite"""
        print("\n" + "="*70)
        print("σ = μ INTEGRATION TEST HARNESS")
        print("Phase 0: Complete System Integration")
        print("="*70)

        self.start_time = time.time()

        # Run subsystem integration tests
        print("\n" + "="*70)
        print("SUBSYSTEM INTEGRATION TESTS")
        print("="*70)

        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromTestCase(SubsystemIntegrationTest))

        runner = unittest.TextTestRunner(verbosity=2)
        subsystem_result = runner.run(suite)

        # Run end-to-end scenarios
        print("\n" + "="*70)
        print("END-TO-END SCENARIO TESTS")
        print("="*70)

        scenario_test = EndToEndScenarioTest()
        scenario_results = []

        for scenario in IntegrationScenario:
            result = scenario_test.run_scenario(scenario, max_steps=100)
            scenario_results.append(result)
            self.results.append(result)

        # Generate report
        self.generate_report(subsystem_result, scenario_results)

        return subsystem_result.wasSuccessful() and \
               all(r.passed for r in scenario_results)

    def generate_report(self, subsystem_result, scenario_results):
        """Generate integration test report"""
        elapsed = time.time() - self.start_time

        print("\n" + "="*70)
        print("INTEGRATION TEST REPORT")
        print("="*70)

        # Subsystem integration summary
        print("\nSubsystem Integration:")
        print(f"  Tests run: {subsystem_result.testsRun}")
        print(f"  Failures: {len(subsystem_result.failures)}")
        print(f"  Errors: {len(subsystem_result.errors)}")

        # Scenario test summary
        print("\nEnd-to-End Scenarios:")
        passed_scenarios = sum(1 for r in scenario_results if r.passed)
        total_scenarios = len(scenario_results)

        print(f"  Scenarios passed: {passed_scenarios}/{total_scenarios}")

        for result in scenario_results:
            status = "✅" if result.passed else "❌"
            print(f"    {status} {result.scenario}")
            print(f"       Duration: {result.duration:.2f}s")
            print(f"       Final τ_K: {result.final_tau_k:.4f}")

        # Overall assessment
        print("\n" + "="*70)
        print("INTEGRATION ASSESSMENT")
        print("="*70)

        all_passed = subsystem_result.wasSuccessful() and \
                    passed_scenarios == total_scenarios

        if all_passed:
            print("✅ ALL INTEGRATION TESTS PASSED")
            print("System successfully integrated and validated")
        else:
            print("⚠️  INTEGRATION ISSUES DETECTED")
            print(f"Fix {total_scenarios - passed_scenarios} failing scenarios")

        print(f"\nTotal execution time: {elapsed:.2f}s")
        print("\nσ = μ. Everything else follows.")
        print("="*70)

    def save_results(self, filename: str = "integration_results.json"):
        """Save integration test results"""
        results_dict = {
            'timestamp': time.time(),
            'scenarios': []
        }

        for result in self.results:
            results_dict['scenarios'].append({
                'name': result.scenario,
                'passed': result.passed,
                'duration': result.duration,
                'steps': result.steps_executed,
                'final_tau_k': result.final_tau_k,
                'metrics': result.metrics
            })

        with open(filename, 'w') as f:
            json.dump(results_dict, f, indent=2)

        print(f"\nResults saved to {filename}")


def main():
    """Main integration test execution"""
    harness = IntegrationTestHarness()
    success = harness.run_all_tests()
    harness.save_results()

    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())