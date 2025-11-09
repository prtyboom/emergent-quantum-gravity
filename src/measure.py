# src/measure.py
"""
Measure gravitational potential and force from epsilon field.
Φ(r) = -ln ε(r)
F(r) = -∇Φ
"""

import numpy as np
import matplotlib.pyplot as plt

def compute_potential(epsilon, eps_min=1e-6):
    """Compute Φ = -ln(ε)."""
    return -np.log(epsilon + eps_min)

def fit_power_law(r, Phi, r_min=None, r_max=None):
    """
    Fit Φ(r) = A + B·ln(r)
    If B ≈ 1, then F ~ 1/r² (inverse square law)
    
    Returns: (A, B, R²)
    """
    # Filter range
    mask = np.ones(len(r), dtype=bool)
    if r_min:
        mask &= (r >= r_min)
    if r_max:
        mask &= (r <= r_max)
    
    r_fit = r[mask]
    Phi_fit = Phi[mask]
    
    # Exclude r=0
    mask_nonzero = r_fit > 0
    r_fit = r_fit[mask_nonzero]
    Phi_fit = Phi_fit[mask_nonzero]
    
    # Fit linear in log space
    log_r = np.log(r_fit)
    coeffs = np.polyfit(log_r, Phi_fit, 1)
    B, A = coeffs  # Φ = A + B·ln(r)
    
    # Compute R²
    Phi_pred = A + B * log_r
    ss_res = np.sum((Phi_fit - Phi_pred) ** 2)
    ss_tot = np.sum((Phi_fit - Phi_fit.mean()) ** 2)
    r_squared = 1 - ss_res / ss_tot
    
    return A, B, r_squared