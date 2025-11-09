# src/optimize.py
"""
Variational optimization of projection metric epsilon(x).
Minimizes: F[ε] = projection_cost + holographic_penalty + smoothness
"""

import numpy as np
from scipy.optimize import minimize

class EpsilonOptimizer:
    """Optimize epsilon field under holographic constraint."""
    
    def __init__(self, lattice, alpha=1.0, lambda_=10.0, gamma=0.5, eps_min=1e-6):
        """
        Args:
            lattice: HolographicLattice instance
            alpha: Projection cost weight
            lambda_: Holographic penalty weight
            gamma: Smoothness penalty weight
            eps_min: Minimum epsilon (regularization)
        """
        self.lattice = lattice
        self.alpha = alpha
        self.lambda_ = lambda_
        self.gamma = gamma
        self.eps_min = eps_min
        
        # Holographic bound (global)
        self.S_max = lattice.N ** (2/3) / 4
        
    def free_energy(self, epsilon):
        """
        Total free energy functional.
        F[ε] = α·Σ(1/ε) + λ·Σ max(0, S_local - S_max)² + γ·Σ(∇ε)²
        """
        epsilon = np.abs(epsilon) + self.eps_min  # Ensure positivity
        
        # Term 1: Projection cost (suppressing epsilon is expensive)
        projection_cost = self.alpha * np.sum(1.0 / (epsilon + self.eps_min))
        
        # Term 2: Holographic penalty (entropy exceeding bound)
        S_local = self.lattice.compute_local_entropy(epsilon)
        violation = np.maximum(0, S_local - self.S_max)
        holographic_penalty = self.lambda_ * np.sum(violation ** 2)
        
        # Term 3: Smoothness (gradient penalty via finite differences)
        eps_diff = epsilon[:, None] - epsilon[None, :]
        smoothness_penalty = self.gamma * np.sum(
            self.lattice.weights * eps_diff ** 2
        ) / 2
        
        return projection_cost + holographic_penalty + smoothness_penalty
    
    def optimize(self, eps_init=None, maxiter=1000, verbose=True):
        """
        Run optimization.
        Returns: optimized epsilon array, result object
        """
        if eps_init is None:
            eps_init = np.ones(self.lattice.N) * 0.01
        
        if verbose:
            print(f"Starting optimization (N={self.lattice.N}, maxiter={maxiter})...")
        
        result = minimize(
            self.free_energy,
            eps_init,
            method='L-BFGS-B',
            bounds=[(self.eps_min, 1.0)] * self.lattice.N,
            options={'maxiter': maxiter, 'disp': verbose}
        )
        
        if verbose:
            print(f"Converged: {result.success}")
            print(f"Final F = {result.fun:.6f}")
            print(f"ε range: [{result.x.min():.6f}, {result.x.max():.6f}]")
        
        return result.x, result