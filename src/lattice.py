"""4D Holographic Lattice with mass placement."""
import numpy as np

class HolographicLattice:
    """4D latent manifold with central mass."""
    
    def __init__(self, N=100, mass_center=10.0, seed=42):
        self.N = N
        np.random.seed(seed)
        
        # 4D latent positions
        self.Z = np.random.randn(N, 4)
        
        # Mass array
        self.masses = np.ones(N)  # base density = 1
        self.masses[0] = mass_center  # central mass
        self.Z[0] = [0, 0, 0, 0]  # center at origin
        
        # Precompute distances (in 3D projection) - CORRECTED
        p3d = self.Z[:, :3]
        self.dists = np.linalg.norm(p3d[:, np.newaxis, :] - p3d[np.newaxis, :, :], axis=2)

        # Characteristic scale
        self.sigma = np.median(self.dists[self.dists > 0])
        
        # Weights for neighbors
        self.weights = np.exp(-self.dists / self.sigma)
        np.fill_diagonal(self.weights, 0)
    
    def compute_local_entropy(self, epsilon):
        """S_local normalized by local area."""
        A_local = np.sum(self.weights, axis=1) + 1.0  # избежать деления на 0
        rho_local = self.masses * epsilon
        S = rho_local * np.sqrt(A_local)
        return S