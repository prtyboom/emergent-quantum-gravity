"""
Fundamental Constants - Emergent Quantum Gravity Theory
CORRECTED VERSION - Simple and working approach
"""

import numpy as np

# ═══════════════════════════════════════════════════════
# FUNDAMENTAL PHYSICAL CONSTANTS (SI units)
# ═══════════════════════════════════════════════════════

c = 299792458.0                    # Speed of light [m/s]
hbar = 1.054571817e-34             # Reduced Planck constant [J·s]
G = 6.67430e-11                    # Gravitational constant [m³/(kg·s²)]

# ═══════════════════════════════════════════════════════
# DERIVED PLANCK SCALES
# ═══════════════════════════════════════════════════════

M_Planck = np.sqrt(hbar * c / G)           # Planck mass [kg]
l_Planck = np.sqrt(hbar * G / c**3)        # Planck length [m]
t_Planck = np.sqrt(hbar * G / c**5)        # Planck time [s]
E_Planck = M_Planck * c**2                 # Planck energy [J]

# ═══════════════════════════════════════════════════════
# THEORY PARAMETERS
# ═══════════════════════════════════════════════════════

# Field equation: ∇²ε = -κ·ρ (ε is dimensionless)
# Poisson coefficient from gravity:
kappa = 4 * np.pi * G / c**2               # [m/kg]

# Alternative expression using Planck mass:
# κ = 4π·ħ/(M_p²·c) where M_p = Planck mass
kappa_planck = 4 * np.pi * hbar / (M_Planck**2 * c)

# Verification: both should match
rel_error = abs(kappa - kappa_planck) / kappa

# Energy density scale (for action functional)
epsilon_0 = c**4 / (G * l_Planck**2)       # [J/m³]

# ═══════════════════════════════════════════════════════
# DISPLAY
# ═══════════════════════════════════════════════════════

def print_constants():
    """Display theory parameters."""
    print("="*70)
    print(" EMERGENT GRAVITY - FUNDAMENTAL CONSTANTS (CORRECTED)")
    print("="*70)
    print(f"Speed of light:      c     = {c:.6e} m/s")
    print(f"Planck constant:     ħ     = {hbar:.6e} J·s")
    print(f"Newton constant:     G     = {G:.6e} m³/(kg·s²)")
    print("-"*70)
    print(f"Planck mass:         M_p   = {M_Planck:.6e} kg")
    print(f"Planck length:       l_p   = {l_Planck:.6e} m")
    print(f"Planck time:         t_p   = {t_Planck:.6e} s")
    print(f"Planck energy:       E_p   = {E_Planck:.6e} J")
    print("-"*70)
    print(f"Poisson coefficient: κ     = {kappa:.6e} m/kg")
    print(f"  (from G):                   {kappa:.6e}")
    print(f"  (from ħ,M_p):               {kappa_planck:.6e}")
    print(f"  Relative difference:        {rel_error:.2e}")
    print("-"*70)
    print(f"Energy scale:        ε₀    = {epsilon_0:.6e} J/m³")
    print("="*70)
    print()
    
    # Key relations
    print("KEY THEORETICAL RELATIONS:")
    print(f"  ∇²ε = -κ·ρ        (field equation)")
    print(f"  Φ = c²·ε          (gravitational potential)")
    print(f"  κ = 4πG/c²        (Poisson coefficient)")
    print(f"  κ = 4πħ/(M_p²c)   (quantum expression)")
    print(f"  M_p = √(ħc/G)     (Planck mass)")
    print("="*70)

if __name__ == "__main__":
    print_constants()