"""
Epsilon Field Model - Dimensionless scalar field (0 to 1)
Represents "subtraction from Absolute" in emergent gravity theory.
"""

import numpy as np
import sys
import os

# Fix imports for direct execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import c, kappa

class EpsilonField:
    """
    Dimensionless scalar field ε(x,y,z).
    
    Theory:
    - ε = 0: Absolute (vacuum, no gravity)
    - ε > 0: Presence of mass (gravity well)
    - Equation: ∇²ε = κ·ρ (without minus!)
    - Potential: Φ = -c²·ε (negative for attraction)
    """
    
    def __init__(self, shape=(100, 100, 100), extent=10.0):
        """
        Parameters:
        -----------
        shape : tuple
            Grid dimensions (Nx, Ny, Nz)
        extent : float
            Physical size: domain is [-extent, +extent] in meters
        """
        self.shape = shape
        self.extent = extent
        
        # Grid spacing
        self.Nx, self.Ny, self.Nz = shape
        self.dx = 2 * extent / self.Nx
        self.dy = 2 * extent / self.Ny
        self.dz = 2 * extent / self.Nz
        
        # Coordinate arrays
        x = np.linspace(-extent, extent, self.Nx)
        y = np.linspace(-extent, extent, self.Ny)
        z = np.linspace(-extent, extent, self.Nz)
        self.X, self.Y, self.Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Field array [dimensionless]
        self.epsilon = np.zeros(shape, dtype=np.float64)
        
        # Mass distribution [kg/m³]
        self.rho = np.zeros(shape, dtype=np.float64)
    
    def add_point_mass(self, M, position=(0, 0, 0), smoothing=None):
        """
        Add point mass with Gaussian smoothing.
        
        Parameters:
        -----------
        M : float
            Mass [kg]
        position : tuple
            (x, y, z) coordinates [m]
        smoothing : float
            Gaussian width [m]. Default: 3*dx (to avoid grid artifacts)
        """
        if smoothing is None:
            smoothing = 3 * self.dx
        
        x0, y0, z0 = position
        r_squared = (self.X - x0)**2 + (self.Y - y0)**2 + (self.Z - z0)**2
        
        # Normalized Gaussian distribution
        gauss = np.exp(-r_squared / (2 * smoothing**2))
        normalization = np.sum(gauss) * self.dx * self.dy * self.dz
        
        # Add to density field
        self.rho += M * gauss / normalization
        
        print(f"  Added mass: M={M:.2e} kg at {position}")
        print(f"  Smoothing: σ={smoothing:.2e} m")
        print(f"  Total mass check: {np.sum(self.rho)*self.dx*self.dy*self.dz:.2e} kg")
    
    def compute_potential(self):
        """
        Gravitational potential Φ = -c²·ε
        
        CRITICAL: Minus sign ensures attraction (Φ < 0)
        
        Returns:
        --------
        Phi : ndarray
            Potential field [m²/s²] (same units as GM/r)
        """
        return -c**2 * self.epsilon  # MINUS for attraction!
    
    def compute_force_field(self):
        """
        Gravitational acceleration: a = -∇Φ
        
        Returns:
        --------
        ax, ay, az : ndarray
            Acceleration components [m/s²]
        """
        Phi = self.compute_potential()
        
        ax = -np.gradient(Phi, self.dx, axis=0)
        ay = -np.gradient(Phi, self.dy, axis=1)
        az = -np.gradient(Phi, self.dz, axis=2)
        
        return ax, ay, az
    
    def get_radial_profile(self, center=(0, 0, 0), num_bins=50):
        """
        Spherically averaged profiles ε(r), Φ(r).
        
        Returns:
        --------
        r_bins : ndarray
            Radial distances [m]
        epsilon_avg : ndarray
            Averaged ε(r) [dimensionless]
        phi_avg : ndarray
            Averaged Φ(r) [m²/s²]
        rho_avg : ndarray
            Averaged ρ(r) [kg/m³]
        """
        x0, y0, z0 = center
        r = np.sqrt((self.X - x0)**2 + (self.Y - y0)**2 + (self.Z - z0)**2)
        
        # Avoid outer boundary effects
        r_max = self.extent * 0.85
        r_bins = np.linspace(self.dx, r_max, num_bins)
        
        epsilon_avg = np.zeros(num_bins)
        phi_avg = np.zeros(num_bins)
        rho_avg = np.zeros(num_bins)
        
        Phi = self.compute_potential()
        
        for i, rc in enumerate(r_bins):
            # Shell averaging
            dr = r_bins[1] - r_bins[0] if num_bins > 1 else r_max
            mask = (r >= rc - dr/2) & (r < rc + dr/2)
            
            if np.sum(mask) > 0:
                epsilon_avg[i] = np.mean(self.epsilon[mask])
                phi_avg[i] = np.mean(Phi[mask])
                rho_avg[i] = np.mean(self.rho[mask])
        
        return r_bins, epsilon_avg, phi_avg, rho_avg
    
    def info(self):
        """Print field information."""
        print("="*60)
        print("EPSILON FIELD INFO")
        print("="*60)
        print(f"Grid shape:       {self.shape}")
        print(f"Physical extent:  ±{self.extent:.2e} m")
        print(f"Resolution:       dx={self.dx:.2e} m")
        print(f"Total points:     {np.prod(self.shape):,}")
        print("-"*60)
        print(f"ε range:          [{self.epsilon.min():.2e}, {self.epsilon.max():.2e}]")
        print(f"Total mass:       {np.sum(self.rho)*self.dx**3:.2e} kg")
        print("="*60)

if __name__ == "__main__":
    # Quick test
    print("Testing EpsilonField...")
    field = EpsilonField(shape=(64, 64, 64), extent=1e10)
    field.add_point_mass(1e30, position=(0, 0, 0))
    field.info()
    print("\n✓ Field module works!")