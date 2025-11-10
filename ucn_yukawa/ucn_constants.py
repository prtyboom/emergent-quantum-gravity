"""
Physical constants for UCN quantum bouncer experiment.
All values in SI units.
"""

import numpy as np

# ═══════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════

c = 2.99792458e8          # Speed of light [m/s]
hbar = 1.054571817e-34    # Reduced Planck constant [J·s]
G = 6.67430e-11           # Gravitational constant [m³/(kg·s²)]

# Neutron properties
m_n = 1.67492749804e-27   # Neutron mass [kg]
g = 9.80665               # Earth's gravity [m/s²]

# Planck scales
M_Planck = np.sqrt(hbar * c / G)  # 2.176e-8 kg
l_Planck = np.sqrt(hbar * G / c**3)  # 1.616e-35 m
E_Planck = M_Planck * c**2  # 1.956e9 J

# ═══════════════════════════════════════════════════════════
# UCN EXPERIMENT PARAMETERS (GRANIT)
# ═══════════════════════════════════════════════════════════

# Energy levels (measured, in peV = 10^-12 eV)
peV = 1e-12 * 1.60218e-19  # Convert peV to Joules

E1_exp = 1.41 * peV  # Ground state
E2_exp = 2.46 * peV  # First excited
E3_exp = 3.32 * peV  # Second excited

# Experimental uncertainties
dE1_exp = 0.014 * peV  # ~1% precision
dE2_exp = 0.025 * peV
dE3_exp = 0.033 * peV

# Spatial scales
z_char = (hbar**2 / (2 * m_n**2 * g))**(1/3)  # Characteristic height [m]
# z_char ≈ 5.87 μm

# ═══════════════════════════════════════════════════════════
# YUKAWA MODIFICATION PARAMETERS
# ═══════════════════════════════════════════════════════════

# We will scan over these values
lambda_g_min = 0.1e-6   # 0.1 μm
lambda_g_max = 10e-3    # 1 cm
n_lambda = 100

lambda_g_array = np.logspace(np.log10(lambda_g_min), 
                             np.log10(lambda_g_max), 
                             n_lambda)

# Corresponding graviphoton masses
def lambda_to_mass(lambda_g):
    """Convert Compton wavelength to mass [kg]."""
    return hbar / (lambda_g * c)

def mass_to_lambda(m_eps):
    """Convert mass to Compton wavelength [m]."""
    return hbar / (m_eps * c)

# ═══════════════════════════════════════════════════════════
# DISPLAY
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*70)
    print("UCN QUANTUM BOUNCER - CONSTANTS")
    print("="*70)
    print(f"Neutron mass:        m_n = {m_n:.3e} kg")
    print(f"Earth gravity:       g   = {g:.3f} m/s²")
    print(f"Planck mass:         M_p = {M_Planck:.3e} kg")
    print(f"Planck length:       l_p = {l_Planck:.3e} m")
    print()
    print(f"Characteristic height: z₀ = {z_char*1e6:.2f} μm")
    print()
    print("Experimental energies:")
    print(f"  E₁ = {E1_exp/peV:.2f} ± {dE1_exp/peV:.3f} peV")
    print(f"  E₂ = {E2_exp/peV:.2f} ± {dE2_exp/peV:.3f} peV")
    print(f"  E₃ = {E3_exp/peV:.2f} ± {dE3_exp/peV:.3f} peV")
    print()
    print(f"Yukawa length range: {lambda_g_min*1e6:.1f} μm to {lambda_g_max*1e3:.1f} mm")
    print(f"Graviphoton mass range: {lambda_to_mass(lambda_g_max)/1.60218e-19*c**2:.2e} eV/c²")
    print(f"                     to {lambda_to_mass(lambda_g_min)/1.60218e-19*c**2:.2e} eV/c²")
    print("="*70)