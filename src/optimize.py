"""Variational epsilon optimization with auto-calibration."""
import numpy as np
from scipy.optimize import minimize, minimize_scalar, curve_fit

class EpsilonOptimizer:
    
    def __init__(self, lattice, alpha=1.0, lambda_holo=10.0, gamma=0.5, eps_min=1e-6):
        self.lattice = lattice
        self.alpha = alpha
        self.lambda_holo = lambda_holo
        self.gamma = gamma
        self.eps_min = eps_min
        self.K_holo = 1.0
        self._update_S_max()
    
    def _update_S_max(self):
        r = self.lattice.dists[0, :]
        self.S_max = self.K_holo * (r**2 + 0.01)
        self.S_max[0] = self.K_holo * 0.01
    
    def set_K(self, K):
        self.K_holo = K
        self._update_S_max()
    
    def free_energy(self, epsilon):
        epsilon = np.clip(np.abs(epsilon), self.eps_min, 1.0)
        
        U_proj = -self.alpha * np.sum(np.log(epsilon))
        
        S_local = self.lattice.compute_local_entropy(epsilon)
        violation = np.maximum(0, S_local - self.S_max)
        U_holo = self.lambda_holo * np.sum(violation**2)
        
        eps_diff = epsilon[:, None] - epsilon[None, :]
        U_smooth = 0.5 * self.gamma * np.sum(self.lattice.weights * eps_diff**2)
        
        return U_proj + U_holo + U_smooth
    
    def optimize(self, eps_init=None, maxiter=500, verbose=False):
        if eps_init is None:
            eps_init = np.full(self.lattice.N, 0.5)
        
        result = minimize(
            self.free_energy,
            eps_init,
            method='L-BFGS-B',
            bounds=[(self.eps_min, 1.0)] * self.lattice.N,
            options={'maxiter': maxiter, 'disp': False}
        )
        
        if verbose:
            print(f"  K={self.K_holo:.3f}: F={result.fun:.2f}, ε∈[{result.x.min():.6f},{result.x.max():.6f}]")
        
        return result.x, result
    
    def measure_n(self, epsilon, r_range=(0.3, 3.0)):
        """Measure F ~ 1/r^n."""
        Phi = -np.log(np.clip(epsilon, 1e-10, 1.0))
        r = self.lattice.dists[0, :]
        
        valid = (r > r_range[0]) & (r < r_range[1])
        r_v = r[valid]
        Phi_v = Phi[valid]
        
        if len(r_v) < 10:
            return np.nan, np.nan
        
        idx = np.argsort(r_v)
        r_s = r_v[idx]
        Phi_s = Phi_v[idx]
        
        F = -np.gradient(Phi_s, r_s)
        
        mask = F > 0
        if np.sum(mask) < 10:
            return np.nan, np.nan
        
        r_fit = r_s[mask]
        F_fit = F[mask]
        
        try:
            popt, pcov = curve_fit(lambda r, A, n: A/r**n, r_fit, F_fit, p0=[1,2], maxfev=5000)
            return popt[1], np.sqrt(pcov[1,1])
        except:
            return np.nan, np.nan
    
    def calibrate(self, target_n=2.0, K_range=(0.1, 10.0), verbose=True):
        """Find K giving n ≈ target_n."""
        if verbose:
            print(f"Calibrating K for n={target_n}...")
        
        def objective(K):
            self.set_K(K)
            eps, _ = self.optimize(verbose=verbose)
            n, _ = self.measure_n(eps)
            if np.isnan(n):
                return 999
            if verbose:
                print(f"  K={K:.3f} → n={n:.3f}")
            return abs(n - target_n)
        
        res = minimize_scalar(objective, bounds=K_range, method='bounded')
        K_opt = res.x
        self.set_K(K_opt)
        
        if verbose:
            print(f"✓ K_optimal = {K_opt:.4f}")
        
        return K_opt