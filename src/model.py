# src/model.py
"""
4D Lattice with holographic constraint.
Mass creates local entropy violation → epsilon suppression.
"""

import numpy as np
from scipy.spatial.distance import cdist

class HolographicLattice:
    """4D lattice with information density and projection metric."""
    
    def __init__(self, N=500, dim=4, seed=42):
        """
        Args:
            N: Number of lattice points
            dim: Latent dimension (default 4)
            seed: Random seed for reproducibility
        """
        self.N = N
        self.dim = dim
        self.seed = seed
        
        np.random.seed(seed)
        self.Z = np.random.randn(N, dim)  # 4D latent space
        
        # Place origin at center
        self.Z[0] = 0.0
        
        # Compute distances and adaptive scale
        self.dists = cdist(self.Z, self.Z, metric='euclidean')
        self.sigma = np.median(self.dists[self.dists > 0])
        
        # Exponential weights for local interactions
        self.weights = np.exp(-self.dists / self.sigma)
        np.fill_diagonal(self.weights, 0)  # No self-interaction
        
        # Information density (uniform initially)
        self.rho_info = np.ones(N)
        
    def add_central_mass(self, M_frac=0.1, m_0=1.0):
        """Add mass at center (index 0)."""
        self.rho_info[0] = 1.0 + M_frac / m_0
        
    def compute_local_entropy(self, epsilon):
        """
        Compute local entropy at each node.
        S_local[i] = rho_info[i] * epsilon[i] * Σ_j weights[i,j]
        """
        weighted_sum = self.weights.sum(axis=1)
        S_local = self.rho_info * epsilon * weighted_sum
        return S_local
    
    def get_radial_profile(self, values):
        """Extract radial profile from center."""
        r = self.dists[0, :]
        sorted_idx = np.argsort(r)
        return r[sorted_idx], values[sorted_idx]