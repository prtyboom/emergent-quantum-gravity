"""
calculate_N.py
Manual calculation of N = (R_H/l_P)^2
Result: N ≈ 7 × 10^121
"""

import numpy as np

# Constants (Planck 2018)
c = 299792458  # m/s
H0_km_s_Mpc = 67.4  # km/s/Mpc
Mpc_to_m = 3.085677581e22  # meters
l_P = 1.616255e-35  # Planck length, meters

# Convert H0 to SI
H0 = H0_km_s_Mpc * 1000 / Mpc_to_m  # 1/s

# Hubble radius
R_H = c / H0  # meters

# Calculate N
N = (R_H / l_P)**2

print(f"R_H = {R_H:.3e} m")
print(f"l_P = {l_P:.3e} m")
print(f"R_H/l_P = {R_H/l_P:.3e}")
print(f"N = {N:.3e}")
print(f"N ≈ 10^{np.log10(N):.1f}")