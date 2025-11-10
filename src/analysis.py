"""
Analysis Tools - Power law fitting and validation
"""

import numpy as np
import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import G

def measure_power_law(r, values, r_range=None):
    """
    Fit values(r) = A/r^n and measure exponent n.
    
    Parameters:
    -----------
    r : array
        Radial distances [m]
    values : array
        Φ(r) or F(r)
    r_range : tuple, optional
        (r_min, r_max) for fitting region
    
    Returns:
    --------
    n : float
        Power law exponent
    n_err : float
        Uncertainty in n
    A : float
        Amplitude
    """
    # Auto-select fitting region (avoid boundaries and center)
    if r_range is None:
        r_min = r[5] if len(r) > 10 else r[1]
        r_max = r[-5] if len(r) > 10 else r[-1]
    else:
        r_min, r_max = r_range
    
    mask = (r >= r_min) & (r <= r_max) & (values != 0) & np.isfinite(values)
    r_fit = r[mask]
    y_fit = np.abs(values[mask])
    
    if len(r_fit) < 5:
        return np.nan, np.nan, np.nan
    
    # Log-log linear fit: log(y) = log(A) - n*log(r)
    log_r = np.log(r_fit)
    log_y = np.log(y_fit)
    
    # Robust fitting
    try:
        coeffs = np.polyfit(log_r, log_y, deg=1)
        n = -coeffs[0]  # Slope = -n
        log_A = coeffs[1]
        A = np.exp(log_A)
        
        # Estimate uncertainty
        y_pred = A * r_fit**(-n)
        residuals = np.log(y_fit) - np.log(y_pred)
        sigma = np.std(residuals)
        
        # Uncertainty in n
        n_err = sigma / np.sqrt(len(r_fit))
        
    except:
        return np.nan, np.nan, np.nan
    
    return n, n_err, A

def validate_newtonian(r, phi, mass, tolerance=0.05):
    """
    Compare Φ(r) with -GM/r.
    
    Returns:
    --------
    max_error : float
        Maximum relative error
    """
    phi_theory = -G * mass / r
    
    mask = (r > 0) & np.isfinite(phi) & np.isfinite(phi_theory)
    
    if np.sum(mask) == 0:
        return np.nan
    
    rel_error = np.abs((phi[mask] - phi_theory[mask]) / phi_theory[mask])
    max_error = np.max(rel_error)
    
    return max_error

if __name__ == "__main__":
    print("Testing analysis module...")
    
    # Test power law fitting
    r_test = np.logspace(8, 11, 50)
    phi_test = -1e20 / r_test  # Should give n=1
    
    n, n_err, A = measure_power_law(r_test, phi_test)
    print(f"  Power law fit: n = {n:.4f} ± {n_err:.4f}")
    print(f"  Expected: n = 1.0000")
    
    if abs(n - 1.0) < 0.01:
        print("  ✓ Analysis works!")
    else:
        print("  ⚠ Check fitting routine")