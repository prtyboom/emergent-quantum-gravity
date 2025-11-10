"""
Fast matrix solver for UCN with Yukawa modification.
Uses finite differences - simple and accurate.
"""

import numpy as np
from scipy.linalg import eigh_tridiagonal
from ucn_constants import *

class UCNYukawaSolver:
    """
    Solve: -ℏ²/(2m) ψ'' + V(z)ψ = E ψ
    V(z) = m g z [1 - exp(-z/λ_g)]
    
    Uses tridiagonal matrix solver (ultra-fast).
    """
    
    def __init__(self, lambda_g=np.inf, z_max=40e-6, N=4000):
        """
        Parameters:
        -----------
        lambda_g : float
            Yukawa screening length [m]
        z_max : float  
            Maximum height [m] (40 μm sufficient)
        N : int
            Number of grid points (4000 for high accuracy)
        """
        self.lambda_g = lambda_g
        self.z_max = z_max
        self.N = N
        
        # Grid (excluding z=0 to enforce ψ(0)=0)
        self.z = np.linspace(z_max/N, z_max, N)
        self.dz = self.z[1] - self.z[0]
        
        # Energy scale
        self.E0 = (hbar**2 * m_n * g**2 / 2)**(1/3)
        
    def potential(self, z):
        """Yukawa-modified potential."""
        if self.lambda_g == np.inf:
            return m_n * g * z
        else:
            return m_n * g * z * (1 - np.exp(-z / self.lambda_g))
    
    def solve(self, n_levels=10):
        """
        Solve for lowest n_levels eigenvalues and eigenvectors.
        
        Returns:
        --------
        E : array
            Eigenvalues [J]
        psi : array  
            Eigenvectors (normalized)
        """
        N = self.N
        dz = self.dz
        
        # Kinetic energy coefficient
        t = hbar**2 / (2 * m_n * dz**2)
        
        # Hamiltonian in tridiagonal form:
        # H[i,i] = 2t + V[i]
        # H[i,i±1] = -t
        
        V = self.potential(self.z)
        
        diagonal = 2*t + V
        off_diagonal = -t * np.ones(N-1)
        
        # Solve tridiagonal eigenvalue problem (super fast!)
        E, psi = eigh_tridiagonal(diagonal, off_diagonal, 
                                  select='i', select_range=(0, n_levels-1))
        
        # Normalize
        for i in range(n_levels):
            norm = np.sqrt(np.sum(psi[:, i]**2) * dz)
            psi[:, i] /= norm
        
        return E, psi
    
    def expectation_z(self, psi):
        """Compute <z> for wavefunction."""
        return np.sum(self.z * psi**2) * self.dz


if __name__ == "__main__":
    print("="*70)
    print("UCN YUKAWA SOLVER - FAST MATRIX METHOD")
    print("="*70)
    
    # Test 1: Standard gravity
    print("\n[1] Standard Newtonian gravity (λ_g = ∞)")
    print("    Grid: N=4000, z_max=40 μm")
    
    solver_newton = UCNYukawaSolver(lambda_g=np.inf, z_max=40e-6, N=4000)
    
    print("    Solving... ", end='', flush=True)
    E_newton, psi_newton = solver_newton.solve(n_levels=5)
    print("Done!")
    
    E_analytical = np.array([1.407, 2.460, 3.321, 4.083, 4.780]) * peV
    
    print("\n    Energy levels:")
    for i in range(5):
        z_avg = solver_newton.expectation_z(psi_newton[:, i])
        error = (E_newton[i] - E_analytical[i]) / E_analytical[i] * 100
        print(f"      E_{i+1} = {E_newton[i]/peV:.4f} peV  (theory: {E_analytical[i]/peV:.3f}, error: {error:+.2f}%, <z>={z_avg*1e6:.2f} μm)")
    
    # Test 2: Yukawa modification
    print("\n" + "="*70)
    print("[2] Yukawa modification (λ_g = 10 μm)")
    
    solver_yukawa = UCNYukawaSolver(lambda_g=10e-6, z_max=40e-6, N=4000)
    
    print("    Solving... ", end='', flush=True)
    E_yukawa, psi_yukawa = solver_yukawa.solve(n_levels=5)
    print("Done!")
    
    print("\n    Energy level shifts:")
    for i in range(5):
        dE = E_yukawa[i] - E_newton[i]
        z_avg = solver_yukawa.expectation_z(psi_yukawa[:, i])
        print(f"      E_{i+1} = {E_yukawa[i]/peV:.4f} peV  (ΔE = {dE/peV:+.5f} peV, <z>={z_avg*1e6:.2f} μm)")
    
    # Detectability
    print("\n" + "="*70)
    print("DETECTABILITY ANALYSIS")
    print("="*70)
    
    threshold_3sigma = 3 * dE1_exp
    
    print(f"\n    Experimental precision: δE₁ = {dE1_exp/peV:.3f} peV")
    print(f"    3σ threshold: {threshold_3sigma/peV:.3f} peV")
    print(f"    Shift for λ_g=10μm: |ΔE₁| = {abs(E_yukawa[0]-E_newton[0])/peV:.5f} peV")
    
    if abs(E_yukawa[0] - E_newton[0]) > threshold_3sigma:
        print(f"\n    ✅ DETECTABLE! ({abs(E_yukawa[0]-E_newton[0])/dE1_exp:.1f}σ)")
    else:
        print(f"\n    ❌ Below threshold ({abs(E_yukawa[0]-E_newton[0])/dE1_exp:.2f}σ)")
    
    print("\n" + "="*70)
    print("✓ Fast solver ready! (~0.1 sec per calculation)")
    print("="*70)