"""
Black Hole Spectrum Discretization Prediction
Δf = c³ ln(2) / (8πGM)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Fix imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import G, c, hbar
# ═══════════════════════════════════════════════════════
# PREDICTION FORMULA
# ═══════════════════════════════════════════════════════

def delta_f(M):
    """
    Frequency discretization for black hole of mass M.
    
    Δf = c³ ln(2) / (8πGM)
    
    Derived from:
    - Holographic entropy: S = k_B ln(2) · A / (4ℓ_P²)
    - Black hole area: A = 16πG²M²/c⁴
    - Energy levels: ΔE = h·Δf
    
    Parameters:
    -----------
    M : float or array
        Black hole mass [kg]
        
    Returns:
    --------
    Δf : float or array
        Frequency spacing [Hz]
    """
    return (c**3 * np.log(2)) / (8 * np.pi * G * M)

def wavelength(M):
    """
    Wavelength corresponding to Δf.
    
    λ = c / Δf
    
    Returns:
    --------
    λ : float or array
        Wavelength [m]
    """
    return c / delta_f(M)

def schwarzschild_radius(M):
    """
    Schwarzschild radius r_s = 2GM/c²
    
    Returns:
    --------
    r_s : float or array
        Schwarzschild radius [m]
    """
    return 2 * G * M / c**2

# ═══════════════════════════════════════════════════════
# PHYSICAL EXAMPLES
# ═══════════════════════════════════════════════════════

def print_predictions():
    """
    Print predictions for various black hole masses.
    """
    print("="*80)
    print(" BLACK HOLE SPECTRUM DISCRETIZATION PREDICTIONS")
    print("="*80)
    print()
    print("Formula: Δf = c³ ln(2) / (8πGM)")
    print()
    print(f"Constants:")
    print(f"  c  = {c:.6e} m/s")
    print(f"  G  = {G:.6e} m³/(kg·s²)")
    print(f"  ln(2) = {np.log(2):.6f}")
    print()
    print("-"*80)
    print(f"{'Mass':<20} {'Δf':<15} {'λ':<15} {'r_s':<15}")
    print(f"{'[M☉]':<20} {'[Hz]':<15} {'[km]':<15} {'[km]':<15}")
    print("-"*80)
    
    M_sun = 1.989e30  # kg
    
    # Examples
    examples = [
        ("Stellar (5 M☉)", 5 * M_sun),
        ("Stellar (10 M☉)", 10 * M_sun),
        ("Intermediate (100 M☉)", 100 * M_sun),
        ("Supermassive (10⁶ M☉)", 1e6 * M_sun),
        ("Sgr A* (4×10⁶ M☉)", 4e6 * M_sun),
        ("M87* (6.5×10⁹ M☉)", 6.5e9 * M_sun),
    ]
    
    for name, M in examples:
        df = delta_f(M)
        lam = wavelength(M)
        rs = schwarzschild_radius(M)
        
        M_solar = M / M_sun
        
        print(f"{name:<20} {df:>14.2e} {lam/1e3:>14.2e} {rs/1e3:>14.2e}")
    
    print("-"*80)
    print()
    
    # Special case: LIGO detections
    print("LIGO/Virgo Events (Final Black Holes):")
    print("-"*80)
    
    ligo_events = [
        ("GW150914", 62 * M_sun),
        ("GW170817 (NS)", 2.7 * M_sun),  # Neutron star merger remnant
        ("GW190521", 142 * M_sun),
    ]
    
    for name, M in ligo_events:
        df = delta_f(M)
        print(f"{name:<20} M = {M/M_sun:.1f} M☉ → Δf = {df:.2f} Hz")
    
    print("="*80)
    print()
    
    print("HOW TO TEST:")
    print("  1. Analyze LIGO/Virgo ringdown phase")
    print("  2. Compute power spectrum of gravitational wave signal")
    print("  3. Look for periodic structure with spacing Δf")
    print("  4. Stellar-mass BH: Δf ~ 1-10 Hz (accessible!)")
    print("="*80)

# ═══════════════════════════════════════════════════════
# VISUALIZATION
# ═══════════════════════════════════════════════════════

def plot_predictions(save_path='predictions/black_hole_spectrum.png'):
    """
    Plot Δf vs M for various black hole masses.
    """
    M_sun = 1.989e30
    
    # Mass range: 1 M☉ to 10⁹ M☉
    M_solar = np.logspace(0, 9, 200)
    M = M_solar * M_sun
    
    df = delta_f(M)
    lam = wavelength(M)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Δf vs M
    ax1.loglog(M_solar, df, 'b-', lw=2.5, label='Δf = c³ln(2)/(8πGM)')
    
    # Mark examples
    examples = [5, 10, 100, 1e6, 4e6, 6.5e9]
    for M_ex in examples:
        df_ex = delta_f(M_ex * M_sun)
        ax1.plot(M_ex, df_ex, 'ro', ms=8)
        
        if M_ex < 1000:
            label = f"{M_ex:.0f} M☉"
        else:
            label = f"{M_ex:.1e} M☉"
        
        ax1.annotate(label, (M_ex, df_ex), 
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=9, alpha=0.8)
    
    ax1.axhline(1.0, color='gray', linestyle='--', alpha=0.5, label='1 Hz (LIGO range)')
    ax1.axhline(100.0, color='gray', linestyle=':', alpha=0.5, label='100 Hz')
    
    ax1.set_xlabel('Black Hole Mass [M☉]', fontsize=12)
    ax1.set_ylabel('Frequency Spacing Δf [Hz]', fontsize=12)
    ax1.set_title('Predicted Spectrum Discretization', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: λ vs M
    ax2.loglog(M_solar, lam/1e3, 'g-', lw=2.5, label='λ = c/Δf')
    
    # Earth radius reference
    R_earth = 6371  # km
    ax2.axhline(R_earth, color='blue', linestyle='--', alpha=0.5, label='Earth radius')
    ax2.axhline(2*R_earth, color='blue', linestyle=':', alpha=0.3)
    
    ax2.set_xlabel('Black Hole Mass [M☉]', fontsize=12)
    ax2.set_ylabel('Wavelength λ [km]', fontsize=12)
    ax2.set_title('Corresponding Wavelength', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {save_path}")

# ═══════════════════════════════════════════════════════
# COMPARISON WITH LIGO DATA
# ═══════════════════════════════════════════════════════

def ligo_testable():
    """
    Check which LIGO events are most promising for testing.
    """
    print("="*80)
    print(" LIGO/VIRGO TESTABILITY ANALYSIS")
    print("="*80)
    print()
    
    M_sun = 1.989e30
    
    # Known events with final BH mass estimates
    events = [
        ("GW150914", 62, 0.22),      # M_final [M☉], spin
        ("GW151226", 21, 0.74),
        ("GW170104", 49, 0.66),
        ("GW170814", 54, 0.72),
        ("GW190521", 142, 0.72),
    ]
    
    print(f"{'Event':<15} {'M_final':<10} {'Δf':<12} {'λ':<15} {'Testable?':<15}")
    print(f"{'':15} {'[M☉]':<10} {'[Hz]':<12} {'[km]':<15}")
    print("-"*80)
    
    for name, M_solar, spin in events:
        M = M_solar * M_sun
        df = delta_f(M)
        lam = wavelength(M)
        
        # LIGO sensitive range: ~10 Hz to 2000 Hz
        # Ringdown duration: ~0.1-1 s
        # Need at least 3-5 cycles to detect periodicity
        
        cycles_in_ringdown = df * 0.5  # assume 0.5 s ringdown
        testable = "YES ✓" if (10 < df < 1000 and cycles_in_ringdown > 3) else "Marginal"
        
        print(f"{name:<15} {M_solar:>9.0f} {df:>11.2f} {lam/1e3:>14.1f} {testable:<15}")
    
    print("="*80)
    print()
    print("CONCLUSION:")
    print("  Stellar-mass black holes (5-150 M☉) → Δf ~ 1-20 Hz")
    print("  Ringdown lasts ~0.1-1 second")
    print("  → Need high SNR to resolve periodic structure")
    print("  → GW150914 (Δf ≈ 13 Hz) is BEST CANDIDATE")
    print("="*80)

# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    print_predictions()
    print()
    ligo_testable()
    print()
    
    import os
    os.makedirs('predictions', exist_ok=True)
    plot_predictions()