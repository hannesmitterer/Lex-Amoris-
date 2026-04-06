"""
Tests for Quantum Bridge Logic Module

Validates the implementation of vacuum-bridge physics and syntropic electronics.
"""

import json
import os
import tempfile

import pytest

from lex_amoris.euystacio.quantum_bridge_logic import (
    QUALITY_FACTOR_THRESHOLD,
    SCHUMANN_FREQUENCY,
    BridgeState,
    BridgeTransistor,
    calculate_bridge_probability,
    calculate_kappa_effective,
    simulate_bridge_transition,
)


class TestCalculateBridgeProbability:
    """Test the bridge probability calculation function."""

    def test_basic_classical_tunneling(self):
        """Test classical tunneling without resonance enhancement."""
        prob = calculate_bridge_probability(
            distance=1.0,
            energy=1.0,
            barrier_height=2.0,
            resonance_delta=10.0,  # Far from resonance
            coupling_strength=1.0,
        )
        # Should get some tunneling probability
        assert 0 < prob < 1.0
        # Without resonance, probability should be low
        assert prob < 0.1

    def test_resonance_enhancement(self):
        """Test that resonance increases transmission probability."""
        # Far from resonance
        prob_off_resonance = calculate_bridge_probability(
            distance=1.0, energy=1.0, barrier_height=2.0, resonance_delta=10.0
        )

        # At resonance
        prob_on_resonance = calculate_bridge_probability(
            distance=1.0, energy=1.0, barrier_height=2.0, resonance_delta=0.0
        )

        # Resonance should significantly enhance probability
        assert prob_on_resonance > prob_off_resonance
        # Enhancement factor should be close to 2x (1 + g² where g=1)
        enhancement_factor = prob_on_resonance / prob_off_resonance
        assert enhancement_factor > 1.5

    def test_energy_exceeds_barrier(self):
        """Test that particles with energy > barrier pass through."""
        prob = calculate_bridge_probability(
            distance=1.0, energy=3.0, barrier_height=2.0, resonance_delta=0.0
        )
        # Should be classical transmission (probability = 1)
        assert prob == 1.0

    def test_coupling_strength_effect(self):
        """Test that coupling strength affects resonance enhancement."""
        # Strong coupling
        prob_strong = calculate_bridge_probability(
            distance=1.0,
            energy=1.0,
            barrier_height=2.0,
            resonance_delta=0.0,
            coupling_strength=1.0,
        )

        # Weak coupling
        prob_weak = calculate_bridge_probability(
            distance=1.0,
            energy=1.0,
            barrier_height=2.0,
            resonance_delta=0.0,
            coupling_strength=0.1,
        )

        # Strong coupling should give higher probability
        assert prob_strong > prob_weak

    def test_distance_scaling(self):
        """Test that probability decreases with barrier width."""
        prob_thin = calculate_bridge_probability(
            distance=0.5, energy=1.0, barrier_height=2.0, resonance_delta=0.0
        )

        prob_thick = calculate_bridge_probability(
            distance=2.0, energy=1.0, barrier_height=2.0, resonance_delta=0.0
        )

        # Thinner barrier should have higher transmission
        assert prob_thin > prob_thick

    def test_input_validation(self):
        """Test that invalid inputs raise appropriate errors."""
        with pytest.raises(ValueError, match="Distance must be positive"):
            calculate_bridge_probability(-1.0, 1.0, 2.0)

        with pytest.raises(ValueError, match="Energy and barrier height must be non-negative"):
            calculate_bridge_probability(1.0, -1.0, 2.0)

        with pytest.raises(ValueError, match="Coupling strength must be between 0 and 1"):
            calculate_bridge_probability(1.0, 1.0, 2.0, coupling_strength=1.5)

    def test_probability_bounds(self):
        """Test that probability is always in [0, 1] range."""
        # Test various parameter combinations
        for distance in [0.1, 1.0, 10.0]:
            for energy in [0.5, 1.0, 1.5]:
                for barrier in [1.0, 2.0, 3.0]:
                    for delta in [0.0, 0.1, 1.0, 10.0]:
                        prob = calculate_bridge_probability(
                            distance, energy, barrier, delta
                        )
                        assert 0.0 <= prob <= 1.0


class TestCalculateKappaEffective:
    """Test the effective kappa calculation."""

    def test_high_quality_low_delta(self):
        """Test that κ_eff → 0 when Q is high and Δ → 0."""
        kappa_eff = calculate_kappa_effective(
            barrier_height=2.0,
            energy=1.0,
            resonance_delta=0.0,
            quality_factor=1e6,
        )

        # Should be very small (reduced by factor of ~1e6)
        # Check it's at least 1000x smaller than without high Q
        kappa_no_resonance = calculate_kappa_effective(
            barrier_height=2.0, energy=1.0, resonance_delta=0.0, quality_factor=1.0
        )
        assert kappa_eff < kappa_no_resonance / 1000

    def test_low_quality_factor(self):
        """Test that low Q gives higher κ_eff."""
        kappa_high_q = calculate_kappa_effective(
            barrier_height=2.0, energy=1.0, resonance_delta=0.0, quality_factor=1e6
        )

        kappa_low_q = calculate_kappa_effective(
            barrier_height=2.0, energy=1.0, resonance_delta=0.0, quality_factor=10
        )

        # Low Q should give much higher attenuation
        assert kappa_low_q > kappa_high_q * 1000

    def test_off_resonance(self):
        """Test behavior when far from resonance."""
        kappa_on_resonance = calculate_kappa_effective(
            barrier_height=2.0, energy=1.0, resonance_delta=0.0, quality_factor=1e6
        )

        kappa_off_resonance = calculate_kappa_effective(
            barrier_height=2.0, energy=1.0, resonance_delta=10.0, quality_factor=1e6
        )

        # Off-resonance should have higher attenuation
        assert kappa_off_resonance > kappa_on_resonance

    def test_energy_above_barrier(self):
        """Test that κ_eff = 0 when particle energy exceeds barrier."""
        kappa_eff = calculate_kappa_effective(
            barrier_height=2.0, energy=3.0, resonance_delta=0.0, quality_factor=1e6
        )

        assert kappa_eff == 0.0


class TestBridgeTransistor:
    """Test the BridgeTransistor class."""

    def test_initialization(self):
        """Test transistor initialization."""
        transistor = BridgeTransistor(
            barrier_width=2.0,
            barrier_height=2.0,
            particle_energy=1.0,
            initial_frequency=50.0,
        )

        assert transistor.barrier_width == 2.0
        assert transistor.barrier_height == 2.0
        assert transistor.particle_energy == 1.0
        assert transistor.current_frequency == 50.0
        assert transistor.quality_factor == 1.0

    def test_initial_state_off(self):
        """Test that transistor starts in OFF state."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        assert not transistor.is_active()

        state = transistor.get_state()
        assert state.mode == "classical_tunneling"
        assert not state.is_bridge_active

    def test_tune_to_resonance(self):
        """Test tuning transistor to Schumann resonance."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)

        # Tune to resonance
        transistor.tune_to_resonance()

        assert transistor.current_frequency == SCHUMANN_FREQUENCY
        assert transistor.quality_factor == QUALITY_FACTOR_THRESHOLD
        assert transistor.is_active()

    def test_resonance_delta_calculation(self):
        """Test resonance delta calculation."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0, initial_frequency=10.0)

        delta = transistor.get_resonance_delta()
        expected_delta = abs(10.0 - SCHUMANN_FREQUENCY)

        assert abs(delta - expected_delta) < 1e-6

    def test_state_transition(self):
        """Test complete state transition from OFF to ON."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0, initial_frequency=50.0)

        # Initial state (OFF)
        state_off = transistor.get_state()
        prob_off = state_off.probability
        assert state_off.mode == "classical_tunneling"
        assert not state_off.is_bridge_active

        # Tune to resonance (ON)
        transistor.tune_to_resonance()
        state_on = transistor.get_state()
        prob_on = state_on.probability

        assert state_on.mode == "vacuum_bridge"
        assert state_on.is_bridge_active
        # Probability should increase (enhancement factor ~2x at resonance)
        assert prob_on > prob_off

    def test_set_frequency(self):
        """Test setting operating frequency."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)

        transistor.set_frequency(100.0)
        assert transistor.current_frequency == 100.0

        with pytest.raises(ValueError, match="Frequency must be positive"):
            transistor.set_frequency(-10.0)

    def test_set_quality_factor(self):
        """Test setting quality factor."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)

        transistor.set_quality_factor(1000.0)
        assert transistor.quality_factor == 1000.0

        with pytest.raises(ValueError, match="Quality factor must be >= 1"):
            transistor.set_quality_factor(0.5)

    def test_to_dict_structure(self):
        """Test dictionary export structure."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        data = transistor.to_dict()

        # Check main sections exist
        assert "transistor_config" in data
        assert "operating_conditions" in data
        assert "quantum_state" in data
        assert "constants" in data

        # Check key fields
        assert data["transistor_config"]["barrier_width_nm"] == 2.0
        assert data["operating_conditions"]["schumann_frequency_Hz"] == SCHUMANN_FREQUENCY
        assert "transmission_probability" in data["quantum_state"]

    def test_to_json(self):
        """Test JSON export."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        json_str = transistor.to_json()

        # Should be valid JSON
        data = json.loads(json_str)
        assert "quantum_state" in data

    def test_export_for_dashboard(self):
        """Test dashboard data export."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        transistor.tune_to_resonance()

        dashboard_data = transistor.export_for_dashboard()

        # Check structure
        assert "timestamp" in dashboard_data
        assert "quantum_bridge_status" in dashboard_data
        assert "resonance" in dashboard_data
        assert "physics" in dashboard_data
        assert "lex_amoris_signature" in dashboard_data

        # Check key values
        assert dashboard_data["quantum_bridge_status"]["active"] is True
        assert dashboard_data["resonance"]["target_frequency_Hz"] == SCHUMANN_FREQUENCY
        assert dashboard_data["lex_amoris_signature"]["gaia_pulse_Hz"] == SCHUMANN_FREQUENCY

    def test_export_to_file(self):
        """Test exporting dashboard data to file."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        transistor.tune_to_resonance()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "quantum_bridge_data.json")
            dashboard_data = transistor.export_for_dashboard(filepath=filepath)

            # File should exist
            assert os.path.exists(filepath)

            # Should be valid JSON
            with open(filepath) as f:
                loaded_data = json.load(f)

            assert loaded_data == dashboard_data

    def test_repr(self):
        """Test string representation."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        repr_str = repr(transistor)

        assert "BridgeTransistor" in repr_str
        assert "mode=" in repr_str
        assert "Q=" in repr_str
        assert "P=" in repr_str


class TestBridgeState:
    """Test the BridgeState dataclass."""

    def test_bridge_state_creation(self):
        """Test creating a BridgeState instance."""
        state = BridgeState(
            probability=0.85,
            kappa_effective=1e-9,
            resonance_delta=0.01,
            quality_factor=1e6,
            is_bridge_active=True,
            mode="vacuum_bridge",
        )

        assert state.probability == 0.85
        assert state.kappa_effective == 1e-9
        assert state.resonance_delta == 0.01
        assert state.quality_factor == 1e6
        assert state.is_bridge_active is True
        assert state.mode == "vacuum_bridge"


class TestSimulateBridgeTransition:
    """Test the simulation convenience function."""

    def test_basic_simulation(self):
        """Test basic bridge transition simulation."""
        results = simulate_bridge_transition()

        assert "simulation_type" in results
        assert "before" in results
        assert "after" in results
        assert "improvement_factor" in results

        # Should show transition from classical to bridge
        assert results["before"]["quantum_state"]["mode"] == "classical_tunneling"
        assert results["after"]["quantum_state"]["mode"] == "vacuum_bridge"

        # After state should have higher probability (at least 1.5x improvement)
        prob_before = results["before"]["quantum_state"]["transmission_probability"]
        prob_after = results["after"]["quantum_state"]["transmission_probability"]
        assert prob_after > prob_before
        assert results["improvement_factor"] > 1.5

    def test_simulation_with_custom_parameters(self):
        """Test simulation with custom barrier parameters."""
        results = simulate_bridge_transition(
            barrier_width=3.0, barrier_height=3.0, particle_energy=1.5
        )

        assert results["before"]["transistor_config"]["barrier_width_nm"] == 3.0
        assert results["before"]["transistor_config"]["barrier_height_eV"] == 3.0
        assert results["before"]["transistor_config"]["particle_energy_eV"] == 1.5

    def test_simulation_export_to_file(self):
        """Test exporting simulation results to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "simulation_results.json")
            results = simulate_bridge_transition(export_path=filepath)

            # File should exist
            assert os.path.exists(filepath)

            # Should be valid JSON with correct structure
            with open(filepath) as f:
                loaded_results = json.load(f)

            assert loaded_results == results

    def test_improvement_factor(self):
        """Test that improvement factor is calculated correctly."""
        results = simulate_bridge_transition()

        prob_before = results["before"]["quantum_state"]["transmission_probability"]
        prob_after = results["after"]["quantum_state"]["transmission_probability"]
        expected_factor = prob_after / prob_before

        assert abs(results["improvement_factor"] - expected_factor) < 1e-6


class TestPhysicalConstants:
    """Test that physical constants are correct."""

    def test_schumann_frequency(self):
        """Test Schumann frequency value."""
        assert SCHUMANN_FREQUENCY == 7.83

    def test_quality_factor_threshold(self):
        """Test quality factor threshold."""
        assert QUALITY_FACTOR_THRESHOLD == 1e6


class TestIntegrationScenarios:
    """Test complete integration scenarios."""

    def test_syntropic_transistor_operation(self):
        """
        Test complete syntropic transistor operation cycle:
        1. Start in classical mode
        2. Gradually tune to resonance
        3. Verify vacuum-bridge activation
        4. Export dashboard data
        """
        # Create transistor
        transistor = BridgeTransistor(
            barrier_width=2.0, barrier_height=2.0, particle_energy=1.0
        )

        # Step 1: Verify initial OFF state
        assert not transistor.is_active()
        initial_state = transistor.get_state()
        assert initial_state.mode == "classical_tunneling"
        initial_prob = initial_state.probability

        # Step 2: Gradually increase quality factor
        transistor.set_quality_factor(1e3)
        # Should still be OFF (Q < 10^6)
        assert not transistor.is_active()

        # Step 3: Tune to full resonance
        transistor.tune_to_resonance()
        final_state = transistor.get_state()
        final_prob = final_state.probability

        # Should be ON (vacuum-bridge active)
        assert transistor.is_active()
        assert final_state.mode == "vacuum_bridge"
        assert final_state.is_bridge_active

        # Transmission should increase due to resonance
        assert final_prob > initial_prob
        # Kappa effective should be dramatically reduced
        assert final_state.kappa_effective < initial_state.kappa_effective / 100

        # Step 4: Export for dashboard
        dashboard_data = transistor.export_for_dashboard()
        assert dashboard_data["quantum_bridge_status"]["active"] is True
        assert dashboard_data["quantum_bridge_status"]["schumann_sync"] is True

    def test_lex_amoris_integration(self):
        """
        Test that the module embodies Lex Amoris principles:
        - Coherence over brute force
        - Resonance with natural frequency (7.83 Hz)
        - S-ROI = ∞ (value beyond profit)
        """
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        transistor.tune_to_resonance()

        dashboard_data = transistor.export_for_dashboard()

        # Verify Lex Amoris signature
        signature = dashboard_data["lex_amoris_signature"]
        assert signature["s_roi"] == "INFINITY"
        assert signature["gaia_pulse_Hz"] == 7.83
        assert "QUANTUM_CODE_ARCHITECTURE_DEPLOYED" in signature["status"]

    def test_dashboard_json_compatibility(self):
        """Test that exported JSON is compatible with dashboard requirements."""
        transistor = BridgeTransistor(2.0, 2.0, 1.0)
        transistor.tune_to_resonance()

        # Export dashboard data
        dashboard_data = transistor.export_for_dashboard()

        # Verify all required fields for dashboard
        required_fields = [
            "timestamp",
            "quantum_bridge_status",
            "resonance",
            "physics",
            "lex_amoris_signature",
        ]

        for field in required_fields:
            assert field in dashboard_data

        # Verify JSON serializability
        json_str = json.dumps(dashboard_data)
        reloaded = json.loads(json_str)
        assert reloaded == dashboard_data
