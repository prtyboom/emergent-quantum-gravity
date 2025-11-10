"""
Full Yukawa parameter scan for UCN experiment.
Determines detectability range for graviphoton mass.
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from ucn_constants import *
from ucn_numerical import UCNYukawaSolver

print("="*70)
print("YUKAWA PARAMETER SCAN FOR UCN EXPERIMENT")
print("="*70)

# ═══════════════════════════════════════════════════════════
# COMPUTE REFERENCE (NEWTONIAN)
# ═══════════════════════════════════════════════════════════

print("\nComputing reference energies (Newtonian)...")
solver_ref = UCNYukawaSolver(lambda_g=np.inf, z_max=40e-6, N=4000)
E_ref, psi_ref = solver_ref.solve(n_levels=3)

print(f"  E₁ = {E_ref[0]/peV:.4f} peV")
print(f"  E₂ = {E_ref[1]/peV:.4f} peV")
print(f"  E₃ = {E_ref[2]/peV:.4f} peV")

# ═══════════════════════════════════════════════════════════
# SCAN YUKAWA LENGTH
# ═══════════════════════════════════════════════════════════

# Scan from 0.1 μm to 1 cm
n_scan = 60
lambda_g_array = np.logspace(-7, -2, n_scan)  # 0.1 μm to 1 cm

# Storage
dE1 = np.zeros(n_scan)
dE2 = np.zeros(n_scan)
dE3 = np.zeros(n_scan)

print(f"\nScanning {n_scan} values of λ_g (0.1 μm to 1 cm)...")
print("This will take ~10 seconds...")

for i, lambda_g in enumerate(tqdm(lambda_g_array, desc="Progress")):
    solver = UCNYukawaSolver(lambda_g=lambda_g, z_max=40e-6, N=4000)
    E_mod, _ = solver.solve(n_levels=3)
    
    dE1[i] = E_mod[0] - E_ref[0]
    dE2[i] = E_mod[1] - E_ref[1]
    dE3[i] = E_mod[2] - E_ref[2]

# Convert to graviphoton mass
m_grav_kg = hbar / (lambda_g_array * c)
m_grav_eV = m_grav_kg * c**2 / 1.60218e-19

# ═══════════════════════════════════════════════════════════
# DETECTABILITY ANALYSIS
# ═══════════════════════════════════════════════════════════

threshold_3sigma = 3 * dE1_exp
threshold_5sigma = 5 * dE1_exp

detectable_3sigma = np.abs(dE1) > threshold_3sigma
detectable_5sigma = np.abs(dE1) > threshold_5sigma

print("\n" + "="*70)
print("DETECTABILITY RESULTS")
print("="*70)

if np.any(detectable_3sigma):
    idx_min = np.where(detectable_3sigma)[0][0]
    lambda_min = lambda_g_array[idx_min]
    m_max = m_grav_eV[idx_min]
    
    print(f"\n✅ 3σ DETECTION POSSIBLE for:")
    print(f"   λ_g > {lambda_min*1e6:.2f} μm")
    print(f"   m_ε < {m_max:.2e} eV/c²")
    
    if np.any(detectable_5sigma):
        idx_5sig = np.where(detectable_5sigma)[0][0]
        lambda_5sig = lambda_g_array[idx_5sig]
        m_5sig = m_grav_eV[idx_5sig]
        
        print(f"\n✅ 5σ DISCOVERY POSSIBLE for:")
        print(f"   λ_g > {lambda_5sig*1e6:.2f} μm")
        print(f"   m_ε < {m_5sig:.2e} eV/c²")
else:
    print("\n❌ NOT DETECTABLE in scanned range")

# Maximum shift
idx_max = np.argmax(np.abs(dE1))
print(f"\nMaximum shift:")
print(f"  |ΔE₁|_max = {np.abs(dE1[idx_max])/peV:.3f} peV")
print(f"  at λ_g = {lambda_g_array[idx_max]*1e6:.2f} μm")
print(f"  Significance: {np.abs(dE1[idx_max])/dE1_exp:.1f}σ")

# ═══════════════════════════════════════════════════════════
# VISUALIZATION
# ═══════════════════════════════════════════════════════════

fig = plt.figure(figsize=(16, 10))

# Layout: 2x3 grid
from matplotlib.gridspec import GridSpec
gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)

# Plot 1: Energy shift vs λ_g
ax1 = fig.add_subplot(gs[0, 0])
ax1.semilogx(lambda_g_array*1e6, dE1/peV, 'o-', label='ΔE₁', lw=2, ms=4)
ax1.semilogx(lambda_g_array*1e6, dE2/peV, 's-', label='ΔE₂', lw=2, ms=4, alpha=0.7)
ax1.axhline(threshold_3sigma/peV, color='red', ls='--', lw=1.5, label='3σ threshold')
ax1.axhline(-threshold_3sigma/peV, color='red', ls='--', lw=1.5)
ax1.axhline(threshold_5sigma/peV, color='orange', ls='--', lw=1.5, label='5σ threshold')
ax1.axhline(-threshold_5sigma/peV, color='orange', ls='--', lw=1.5)
ax1.set_xlabel('Yukawa length λ_g [μm]', fontsize=11)
ax1.set_ylabel('Energy shift ΔE [peV]', fontsize=11)
ax1.set_title('(a) Energy Level Shifts', fontsize=12, fontweight='bold')
ax1.legend(fontsize=9, loc='best')
ax1.grid(True, alpha=0.3)

# Plot 2: Shift vs graviphoton mass
ax2 = fig.add_subplot(gs[0, 1])
ax2.loglog(m_grav_eV, np.abs(dE1)/peV, 'o-', label='|ΔE₁|', lw=2, ms=4)
ax2.loglog(m_grav_eV, np.abs(dE2)/peV, 's-', label='|ΔE₂|', lw=2, ms=4, alpha=0.7)
ax2.axhline(threshold_3sigma/peV, color='red', ls='--', lw=1.5, label='3σ')
ax2.axhline(threshold_5sigma/peV, color='orange', ls='--', lw=1.5, label='5σ')
ax2.set_xlabel('Graviphoton mass m_ε [eV/c²]', fontsize=11)
ax2.set_ylabel('|Energy shift| [peV]', fontsize=11)
ax2.set_title('(b) Shift vs Graviphoton Mass', fontsize=12, fontweight='bold')
ax2.legend(fontsize=9, loc='best')
ax2.grid(True, alpha=0.3)
ax2.invert_xaxis()

# Plot 3: Statistical significance
ax3 = fig.add_subplot(gs[0, 2])
significance = np.abs(dE1) / dE1_exp
ax3.loglog(lambda_g_array*1e6, significance, 'o-', lw=2, ms=4, color='purple')
ax3.axhline(3, color='red', ls='--', lw=2, label='3σ (evidence)')
ax3.axhline(5, color='orange', ls='--', lw=2, label='5σ (discovery)')
ax3.fill_between(lambda_g_array*1e6, 0.1, 100, where=(significance >= 3), 
                 alpha=0.2, color='green', label='Detectable')
ax3.set_xlabel('Yukawa length λ_g [μm]', fontsize=11)
ax3.set_ylabel('Detection significance [σ]', fontsize=11)
ax3.set_title('(c) Statistical Significance', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9, loc='best')
ax3.grid(True, alpha=0.3)
ax3.set_ylim(0.1, 100)

# Plot 4: Detectability map
ax4 = fig.add_subplot(gs[1, 0])
ax4.fill_between(lambda_g_array*1e6, 0, 1, where=detectable_5sigma, 
                 alpha=0.4, color='orange', label='5σ discovery')
ax4.fill_between(lambda_g_array*1e6, 0, 1, where=detectable_3sigma & ~detectable_5sigma, 
                 alpha=0.4, color='green', label='3σ evidence')
ax4.fill_between(lambda_g_array*1e6, 0, 1, where=~detectable_3sigma, 
                 alpha=0.2, color='gray', label='Not detectable')
ax4.set_xscale('log')
ax4.set_xlabel('Yukawa length λ_g [μm]', fontsize=11)
ax4.set_ylabel('Detection status', fontsize=11)
ax4.set_title('(d) Detectability Map', fontsize=12, fontweight='bold')
ax4.legend(fontsize=9, loc='upper left')
ax4.set_ylim(0, 1)
ax4.set_yticks([0, 0.5, 1])
ax4.set_yticklabels(['No', '', 'Yes'])
ax4.grid(True, alpha=0.3, axis='x')

# Plot 5: Comparison with Planck scale
ax5 = fig.add_subplot(gs[1, 1])
m_planck_eV = M_Planck * c**2 / 1.60218e-19
ax5.loglog(m_grav_eV, np.abs(dE1)/peV, 'o-', lw=2, ms=4, label='|ΔE₁(m_ε)|')
ax5.axvline(m_planck_eV, color='black', ls=':', lw=2, label=f'Planck mass')
ax5.axhline(threshold_3sigma/peV, color='red', ls='--', lw=1.5)
ax5.fill_betweenx([1e-6, 1], m_grav_eV[0], m_planck_eV, 
                  alpha=0.15, color='blue', label='Testable range')
ax5.set_xlabel('Graviphoton mass m_ε [eV/c²]', fontsize=11)
ax5.set_ylabel('|ΔE₁| [peV]', fontsize=11)
ax5.set_title('(e) Comparison with Planck Scale', fontsize=12, fontweight='bold')
ax5.legend(fontsize=9, loc='best')
ax5.grid(True, alpha=0.3)
ax5.invert_xaxis()

# Plot 6: Constraint plot
ax6 = fig.add_subplot(gs[1, 2])
# Show excluded vs allowed regions
constraint_line = threshold_3sigma / np.abs(dE1)
ax6.loglog(lambda_g_array*1e6, constraint_line, 'b-', lw=2.5)
ax6.fill_between(lambda_g_array*1e6, 0.01, constraint_line, 
                 alpha=0.3, color='red', label='Excluded (>3σ)')
ax6.fill_between(lambda_g_array*1e6, constraint_line, 100, 
                 alpha=0.3, color='green', label='Allowed')
ax6.set_xlabel('Yukawa length λ_g [μm]', fontsize=11)
ax6.set_ylabel('Required precision δE/|ΔE|', fontsize=11)
ax6.set_title('(f) Experimental Constraints', fontsize=12, fontweight='bold')
ax6.legend(fontsize=9, loc='best')
ax6.grid(True, alpha=0.3)
ax6.set_ylim(0.01, 100)

plt.suptitle('UCN Quantum Bouncer: Yukawa Modification Detectability Analysis', 
            fontsize=14, fontweight='bold', y=0.995)

plt.savefig('yukawa_ucn_full_analysis.png', dpi=200, bbox_inches='tight')
print("\n✓ Figure saved: yukawa_ucn_full_analysis.png")

# ═══════════════════════════════════════════════════════════
# SAVE DATA
# ═══════════════════════════════════════════════════════════

np.savez('yukawa_scan_data.npz',
         lambda_g=lambda_g_array,
         m_grav_eV=m_grav_eV,
         dE1=dE1,
         dE2=dE2,
         dE3=dE3,
         E_ref=E_ref)

print("✓ Data saved: yukawa_scan_data.npz")

print("\n" + "="*70)
print("SCAN COMPLETE!")
print("="*70)

plt.show()