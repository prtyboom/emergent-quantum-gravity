"""Test emergent gravity mechanism."""
import sys
sys.path.append('.')

from src.lattice import HolographicLattice
from src.optimize import EpsilonOptimizer

print("="*60)
print("EMERGENT GRAVITY TEST v2")
print("="*60)

# ИЗМЕНЕНИЯ: N=200, gamma=0.1
N = 200
mass = 10.0
lattice = HolographicLattice(N=N, mass_center=mass, seed=42)
print(f"Lattice: N={N}, M_center={mass}")

opt = EpsilonOptimizer(lattice, alpha=1.0, lambda_holo=10.0, gamma=0.1)

K_opt = opt.calibrate(target_n=2.0, K_range=(0.1, 10.0), verbose=True)

print("\nFinal optimization...")
eps_final, res = opt.optimize(verbose=True)

n, n_err = opt.measure_n(eps_final)

print("\n" + "="*60)
print(f"RESULT: n = {n:.3f} ± {n_err:.3f}")
if n_err > 0 and abs(n - 2.0) / n_err < 2.5: # Allow 2.5 sigma deviation
    print("✅ COMPATIBLE WITH 1/r²")
else:
    print(f"⚠️  Deviation: {abs(n-2.0)/n_err if n_err > 0 else 999:.1f}σ")
print("="*60)