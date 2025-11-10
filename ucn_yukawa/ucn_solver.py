"""
Analytical solver for UCN quantum bouncer using Airy function.
CORRECTED energy scale formula.
"""

import numpy as np
from scipy.special import airy
from scipy.optimize import brentq
from ucn_constants import *

# ═══════════════════════════════════════════════════════════
# ANALYTICAL SOLUTION
# ═══════════════════════════════════════════════════════════

def analytical_energies(n_levels=10):
    """
    Compute exact energy levels using Airy function zeros.
    
    For V(z) = m g z with ψ(0) = 0:
    E_n = α_n * (ℏ² m g² / 2)^(1/3)
    
    where α_n are zeros of Airy function Ai(-α_n) = 0
    
    CRITICAL: Only ONE power of m, not m²!
    """
    # CORRECT energy scale
    E0 = (hbar**2 * m_n * g**2 / 2)**(1/3)
    
    # Known zeros of Ai(x) (tabulated values)
    # These are x where Ai(x) = 0 for x < 0
    # We need -x (positive values)
    
    airy_zeros_known = [
        2.33810741,  # α_1
        4.08794944,  # α_2
        5.52055983,  # α_3
        6.78670809,  # α_4
        7.94413359,  # α_5
        9.02265085,  # α_6
        10.04017434, # α_7
        11.00852430, # α_8
        11.93601556, # α_9
        12.82877675  # α_10
    ]
    
    zeros = np.array(airy_zeros_known[:n_levels])
    
    # Energy levels
    E = zeros * E0
    
    return E, zeros

# Test
if __name__ == "__main__":
    print("="*70)
    print("ANALYTICAL UCN ENERGIES (CORRECTED)")
    print("="*70)
    
    # Calculate E0 explicitly
    E0_value = (hbar**2 * m_n * g**2 / 2)**(1/3)
    peV_conversion = 1e-12 * 1.60218e-19  # 1 peV in Joules
    
    print(f"\nEnergy scale calculation:")
    print(f"  ℏ = {hbar:.6e} J·s")
    print(f"  m_n = {m_n:.6e} kg")
    print(f"  g = {g:.5f} m/s²")
    print(f"  ℏ² m g² = {hbar**2 * m_n * g**2:.6e}")
    print(f"  E₀ = (ℏ² m g² / 2)^(1/3) = {E0_value:.6e} J")
    print(f"  E₀ = {E0_value/peV_conversion:.4f} peV")
    
    E_exact, alphas = analytical_energies(n_levels=5)
    
    print("\nAiry function zeros (α_n):")
    for i, a in enumerate(alphas[:5]):
        print(f"  α_{i+1} = {a:.5f}")
    
    print("\nEnergy levels:")
    for i, E in enumerate(E_exact[:5]):
        print(f"  E_{i+1} = {E/peV:.3f} peV = α_{i+1} × {E0_value/peV:.4f} peV")
    
    print("\nComparison with GRANIT experiment:")
    print(f"  E₁: theory={E_exact[0]/peV:.3f} peV, exp={E1_exp/peV:.2f} peV, error={(E_exact[0]-E1_exp)/E1_exp*100:+.1f}%")
    print(f"  E₂: theory={E_exact[1]/peV:.3f} peV, exp={E2_exp/peV:.2f} peV, error={(E_exact[1]-E2_exp)/E2_exp*100:+.1f}%")
    print(f"  E₃: theory={E_exact[2]/peV:.3f} peV, exp={E3_exp/peV:.2f} peV, error={(E_exact[2]-E3_exp)/E3_exp*100:+.1f}%")
    
    print("\n" + "="*70)
    if abs(E_exact[0]/peV - E1_exp/peV) < 0.1:
        print("✅ EXCELLENT AGREEMENT WITH EXPERIMENT!")
    else:
        print(f"⚠️  Deviation: {abs(E_exact[0]-E1_exp)/E1_exp*100:.1f}%")
    print("="*70)