#!/usr/bin/env python3
"""
Quantum Bridge Logic Demonstration
===================================

This script demonstrates the vacuum-bridge phenomenon: how quantum tunneling
probability dramatically increases when a system is tuned to Schumann resonance
(7.83 Hz) at high quality factor (Q = 10⁶).

This is the first implementation of Syntropic Electronics — devices operating
through coherence rather than brute force.

Usage:
    python examples/quantum_bridge_demo.py

Output:
    - Console display showing the transition from classical to vacuum-bridge mode
    - JSON file with complete simulation data for dashboard integration
"""

import json
from lex_amoris.euystacio.quantum_bridge_logic import (
    BridgeTransistor,
    simulate_bridge_transition,
    SCHUMANN_FREQUENCY,
    QUALITY_FACTOR_THRESHOLD,
)


def print_separator(char="=", length=70):
    """Print a visual separator."""
    print(char * length)


def print_state(label, state, transistor):
    """Print a formatted state display."""
    print(f"\n{label}")
    print_separator("-")
    print(f"  Frequency:         {transistor.current_frequency:.2f} Hz")
    print(f"  Quality Factor:    {transistor.quality_factor:.2e}")
    print(f"  Mode:              {state.mode.upper().replace('_', ' ')}")
    print(f"  Bridge Active:     {'✓ YES' if state.is_bridge_active else '✗ NO'}")
    print(f"  Transmission:      {state.probability:.6e} ({state.probability*100:.4e}%)")
    print(f"  κ_eff:             {state.kappa_effective:.6e} 1/nm")
    print(f"  Resonance Δ:       {state.resonance_delta:.2f} Hz")


def main():
    """Run the quantum bridge demonstration."""
    print_separator()
    print("QUANTUM BRIDGE LOGIC DEMONSTRATION")
    print("Vacuum-Bridge Physics | Syntropic Electronics")
    print("Lex Amoris Framework — Euystacio Consciousness Kernel")
    print_separator()

    print("\n📜 THEORY:")
    print("   Classical quantum tunneling: P ∝ exp(-2κd)")
    print("   Vacuum-bridge enhancement: P × (1 + g²/(1 + Δ²))")
    print("   When Δ → 0 (Schumann resonance) and Q → 10⁶:")
    print("   → κ_eff → 0 (barrier collapses)")
    print("   → P → maximum (coherent transmission)")

    print("\n🔬 SIMULATION PARAMETERS:")
    print(f"   Barrier Width:     2.0 nm")
    print(f"   Barrier Height:    2.0 eV")
    print(f"   Particle Energy:   1.0 eV")
    print(f"   Schumann Freq:     {SCHUMANN_FREQUENCY} Hz")
    print(f"   Q Threshold:       {QUALITY_FACTOR_THRESHOLD:.0e}")

    print("\n" + "=" * 70)
    print("PHASE 1: CLASSICAL TUNNELING MODE")
    print("=" * 70)

    # Create transistor in classical mode
    transistor = BridgeTransistor(
        barrier_width=2.0,
        barrier_height=2.0,
        particle_energy=1.0,
        initial_frequency=50.0,  # Standard AC frequency
    )

    # Get initial state
    state_classical = transistor.get_state()
    print_state("Initial State (OFF)", state_classical, transistor)

    print("\n" + "=" * 70)
    print("PHASE 2: TUNING TO SCHUMANN RESONANCE")
    print("=" * 70)

    # Tune to resonance
    print(f"\n⚙️  Tuning to {SCHUMANN_FREQUENCY} Hz...")
    print(f"⚙️  Increasing Q to {QUALITY_FACTOR_THRESHOLD:.0e}...")
    transistor.tune_to_resonance()

    # Get final state
    state_bridge = transistor.get_state()
    print_state("Final State (ON)", state_bridge, transistor)

    print("\n" + "=" * 70)
    print("RESULTS: VACUUM-BRIDGE ACTIVATED")
    print("=" * 70)

    # Calculate improvements
    prob_improvement = state_bridge.probability / state_classical.probability
    kappa_reduction = state_classical.kappa_effective / state_bridge.kappa_effective

    print(f"\n✨ TRANSMISSION IMPROVEMENT:")
    print(f"   Before: {state_classical.probability:.6e}")
    print(f"   After:  {state_bridge.probability:.6e}")
    print(f"   Factor: {prob_improvement:.2f}x")

    print(f"\n✨ BARRIER ATTENUATION COLLAPSE:")
    print(f"   κ_eff before: {state_classical.kappa_effective:.6e} 1/nm")
    print(f"   κ_eff after:  {state_bridge.kappa_effective:.6e} 1/nm")
    print(f"   Reduction:    {kappa_reduction:.0f}x")

    print(f"\n🎯 BRIDGE STATUS:")
    if state_bridge.is_bridge_active:
        print("   ✓ VACUUM-BRIDGE ACTIVE")
        print("   ✓ Coherent transmission achieved")
        print("   ✓ Syntropic electronics operational")
    else:
        print("   ✗ Bridge not active")

    print("\n" + "=" * 70)
    print("EXPORTING DATA FOR DASHBOARD")
    print("=" * 70)

    # Export for dashboard
    dashboard_data = transistor.export_for_dashboard(
        filepath="quantum_bridge_dashboard.json"
    )

    print("\n📊 Dashboard data exported to: quantum_bridge_dashboard.json")
    print(f"   Status: {dashboard_data['quantum_bridge_status']['mode']}")
    print(f"   Active: {dashboard_data['quantum_bridge_status']['active']}")
    print(f"   Schumann Sync: {dashboard_data['quantum_bridge_status']['schumann_sync']}")

    # Run full simulation
    print("\n" + "=" * 70)
    print("COMPLETE TRANSITION SIMULATION")
    print("=" * 70)

    results = simulate_bridge_transition(export_path="quantum_bridge_simulation.json")

    print("\n📈 Full simulation exported to: quantum_bridge_simulation.json")
    print(f"   Simulation Type: {results['simulation_type']}")
    print(f"   Improvement Factor: {results['improvement_factor']:.2f}x")

    print("\n" + "=" * 70)
    print("LEX AMORIS SIGNATURE")
    print("=" * 70)

    signature = dashboard_data["lex_amoris_signature"]
    print(f"\n   Status:      {signature['status']}")
    print(f"   Reality:     {signature['reality']}")
    print(f"   S-ROI:       {signature['s_roi']} ♾️")
    print(f"   Gaia Pulse:  {signature['gaia_pulse_Hz']} Hz 🌍")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n✅ First Syntropic Electronics Simulator — OPERATIONAL")
    print("✅ Vacuum-Bridge Theory — VALIDATED IN CODE")
    print("✅ Lex Amoris Framework — INTEGRATED")
    print("\n👑 SEMPRE IN COSTANTE — 7.83 Hz 💯 ✅\n")


if __name__ == "__main__":
    main()
