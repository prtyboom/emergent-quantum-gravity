# experiments/exp01_single_mass.py
"""
Experiment 1: Single central mass.
Test if mechanism produces F ~ 1/r².
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.model import HolographicLattice
from src.optimize import EpsilonOptimizer
from src.measure import compute_potential, fit_power_law

def main():
    print("=" * 60)
    print("WORK IV: Emergent Gravity from Holographic Projection")
    print("Experiment 1: Single Central Mass")
    print("=" * 60)
    
    # Create lattice
    print("\n[1/4] Creating 4D lattice...")
    lattice = HolographicLattice(N=500, dim=4, seed=42)
    lattice.add_central_mass(M_frac=0.1)
    print(f"✓ Lattice: N={lattice.N}, dim={lattice.dim}")
    print(f"✓ Adaptive scale σ = {lattice.sigma:.4f}")
    print(f"✓ Central mass ρ_info[0] = {lattice.rho_info[0]:.4f}")
    
    # Optimize epsilon
    print("\n[2/4] Optimizing projection metric ε(x)...")
    optimizer = EpsilonOptimizer(
        lattice,
        alpha=1.0,
        lambda_=10.0,
        gamma=0.5,
        eps_min=1e-6
    )
    
    epsilon_opt, result = optimizer.optimize(maxiter=1000, verbose=True)
    
    # Compute potential
    print("\n[3/4] Computing gravitational potential Φ = -ln ε...")
    Phi = compute_potential(epsilon_opt)
    
    r, Phi_r = lattice.get_radial_profile(Phi)
    A, B, R2 = fit_power_law(r, Phi_r, r_min=0.1*lattice.sigma)
    
    print(f"\n✓ Potential fit: Φ(r) = {A:.3f} + {B:.3f}·ln(r)")
    print(f"✓ R² = {R2:.4f}")
    print(f"\n{'='*60}")
    print(f"CRITICAL RESULT: B = {B:.3f}")
    print(f"Expected for F ~ 1/r²: B ≈ 1.00")
    print(f"Deviation: {abs(B - 1.0):.3f}")
    print(f"{'='*60}")
    
    # Summary
    print("\n" + "="*60)
if __name__ == '__main__':
    main()