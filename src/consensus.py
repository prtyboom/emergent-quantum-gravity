"""
Consensus Field Implementation
Computes ρ_C, decoherence rates, and information mass.
"""

import numpy as np
from scipy.linalg import expm
import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import G, c, hbar, kappa

# ═══════════════════════════════════════════════════════
# QUANTUM NODE
# ═══════════════════════════════════════════════════════

class QuantumNode:
    """
    Represents a quantum system (particle, observer, etc.)
    
    Attributes:
    -----------
    position : ndarray
        3D position [m]
    mass : float
        Mass [kg] (can be information mass, self-consistent)
    state : ndarray
        Quantum state vector |ψ⟩
    H : ndarray
        Hamiltonian matrix
    """
    
    def __init__(self, position, mass, state_dim=2):
        """
        Parameters:
        -----------
        position : array-like
            (x, y, z) in meters
        mass : float
            Initial mass [kg]
        state_dim : int
            Hilbert space dimension (default: 2 for qubit)
        """
        self.position = np.array(position, dtype=np.float64)
        self.mass = mass
        self.state_dim = state_dim
        
        # Initialize in random state
        self.state = np.random.randn(state_dim) + 1j * np.random.randn(state_dim)
        self.state /= np.linalg.norm(self.state)
        
        # Default Hamiltonian (can be overridden)
        self.H = np.zeros((state_dim, state_dim), dtype=complex)
    
    def set_state(self, state):
        """Set quantum state (normalized automatically)."""
        self.state = np.array(state, dtype=complex)
        self.state /= np.linalg.norm(self.state)
    
    def set_hamiltonian(self, H):
        """Set Hamiltonian matrix."""
        self.H = np.array(H, dtype=complex)

# ═══════════════════════════════════════════════════════
# CONSENSUS FIELD
# ═══════════════════════════════════════════════════════

class ConsensusField:
    """
    Computes consensus field ρ_C from collection of nodes.
    """
    
    def __init__(self, nodes, coherence_length=None):
        """
        Parameters:
        -----------
        nodes : list of QuantumNode
            All quantum systems in the universe
        coherence_length : float or None
            Screening length λ [m]. If None, no screening (1/r² only)
        """
        self.nodes = nodes
        self.coherence_length = coherence_length
        
        if len(nodes) > 0:
            self.state_dim = nodes[0].state_dim
        else:
            self.state_dim = 2
    
    def compute_weight(self, x, node):
        """
        Weight of node at position x.
        
        w_i(x) = (G m_i / c²) / r²  ·  screening(r/λ)
        
        Parameters:
        -----------
        x : ndarray
            Evaluation point
        node : QuantumNode
            Node i
            
        Returns:
        --------
        w : float
            Weight (dimensionless after normalization)
        """
        r = np.linalg.norm(x - node.position)
        
        # Regularization at small r
        epsilon = 1e-10  # meters
        r = max(r, epsilon)
        
        # Base weight: Newtonian
        w = (G * node.mass / c**2) / r**2
        
        # Screening function
        if self.coherence_length is not None:
            screening = np.exp(-r / self.coherence_length)
            w *= screening
        
        return w
    
    def compute_at_point(self, x):
        """
        Compute ρ_C(x) as density matrix.
        
        ρ_C(x) = Σᵢ wᵢ(x) |ψᵢ⟩⟨ψᵢ|
        
        Returns:
        --------
        rho_C : ndarray
            Consensus density matrix (state_dim × state_dim)
        W_total : float
            Total weight (for normalization)
        """
        rho_C = np.zeros((self.state_dim, self.state_dim), dtype=complex)
        W_total = 0.0
        
        for node in self.nodes:
            w = self.compute_weight(x, node)
            rho_C += w * np.outer(node.state, node.state.conj())
            W_total += w
        
        return rho_C, W_total
    
    def consensus_strength(self, x):
        """
        Total consensus strength W(x) = Tr[ρ_C].
        
        Returns:
        --------
        W : float
            Consensus strength (analogous to ε field)
        """
        _, W = self.compute_at_point(x)
        return W

# ═══════════════════════════════════════════════════════
# DECOHERENCE
# ═══════════════════════════════════════════════════════

def decoherence_rate(node, rho_C, alpha=1e-43):
    """
    Compute γ(ρ_C) for a node.
    
    γ = α · Tr(ρ_C²) · ⟨ψ|ρ_C|ψ⟩ / ℏ
    
    Parameters:
    -----------
    node : QuantumNode
        The node experiencing decoherence
    rho_C : ndarray
        Consensus density matrix at node's position
    alpha : float
        Coupling constant (dimensionless)
        
    Returns:
    --------
    gamma : float
        Decoherence rate [1/s]
    """
    # Purity of consensus
    purity = np.trace(rho_C @ rho_C).real
    
    # Overlap: how much node agrees with consensus
    overlap = np.abs(node.state.conj() @ rho_C @ node.state)
    
    # Rate
    gamma = alpha * purity * overlap / hbar
    
    return gamma

def evolve_with_decoherence(node, rho_C, dt, alpha=1e-43):
    """
    Evolve node state for time dt with decoherence.
    
    dψ/dt = -iH|ψ⟩/ℏ - γ(ρ_C)[|ψ⟩ - P_C|ψ⟩]
    
    Parameters:
    -----------
    node : QuantumNode
        Node to evolve
    rho_C : ndarray
        Consensus at node's position
    dt : float
        Time step [s]
    alpha : float
        Coupling constant
    """
    # Unitary evolution
    U = expm(-1j * node.H * dt / hbar)
    psi_new = U @ node.state
    
    # Decoherence term
    gamma = decoherence_rate(node, rho_C, alpha)
    
    # Projection onto consensus
    W = np.trace(rho_C).real
    if W > 1e-30:
        P_C = rho_C / W
        projection = P_C @ node.state
    else:
        projection = node.state  # No consensus → no decoherence
    
    # Decoherence correction
    psi_new += -gamma * dt * (node.state - projection)
    
    # Renormalize
    norm = np.linalg.norm(psi_new)
    if norm > 1e-15:
        psi_new /= norm
    
    node.state = psi_new

# ═══════════════════════════════════════════════════════
# INFORMATION MASS
# ═══════════════════════════════════════════════════════

def compute_information_mass(node, rho_C):
    """
    Self-consistent information mass.
    
    m = κ · Tr(|ψ⟩⟨ψ| · ρ_C) = κ · ⟨ψ|ρ_C|ψ⟩
    
    Parameters:
    -----------
    node : QuantumNode
    rho_C : ndarray
        Consensus density matrix
        
    Returns:
    --------
    m : float
        Information mass [kg]
    """
    overlap = np.abs(node.state.conj() @ rho_C @ node.state)
    m = kappa * overlap
    
    return m

def update_masses_selfconsistent(consensus_field, max_iterations=10, tolerance=1e-6):
    """
    Iterate to find self-consistent masses.
    
    Algorithm:
    1. Compute ρ_C with current masses
    2. Update masses: m_i = κ·Tr(ψ_i · ρ_C)
    3. Repeat until convergence
    
    Parameters:
    -----------
    consensus_field : ConsensusField
    max_iterations : int
    tolerance : float
        Relative change threshold
        
    Returns:
    --------
    converged : bool
    iterations : int
    """
    for iteration in range(max_iterations):
        max_relative_change = 0.0
        
        for node in consensus_field.nodes:
            # Compute consensus at node position
            rho_C, _ = consensus_field.compute_at_point(node.position)
            
            # New mass
            m_new = compute_information_mass(node, rho_C)
            
            # Relative change
            if node.mass > 1e-30:
                relative_change = abs(m_new - node.mass) / node.mass
                max_relative_change = max(max_relative_change, relative_change)
            
            # Update
            node.mass = m_new
        
        # Check convergence
        if max_relative_change < tolerance:
            return True, iteration + 1
    
    return False, max_iterations

# ═══════════════════════════════════════════════════════
# EXAMPLE: TWO-BODY SYSTEM
# ═══════════════════════════════════════════════════════

def example_two_bodies():
    """
    Example: Two particles with self-consistent masses.
    """
    print("="*70)
    print("CONSENSUS FIELD - TWO BODY EXAMPLE")
    print("="*70)
    
    # Create two nodes
    m0 = 1e20  # kg (initial guess)
    separation = 1e6  # meters
    
    node1 = QuantumNode(position=[-separation/2, 0, 0], mass=m0, state_dim=2)
    node2 = QuantumNode(position=[+separation/2, 0, 0], mass=m0, state_dim=2)
    
    # Both in "localized" state (classical)
    node1.set_state([1.0, 0.0])
    node2.set_state([1.0, 0.0])
    
    # Consensus field
    consensus = ConsensusField([node1, node2])
    
    print(f"\nInitial setup:")
    print(f"  Separation: {separation:.2e} m")
    print(f"  Initial mass: {m0:.2e} kg")
    print()
    
    # Self-consistent iteration
    print("Finding self-consistent masses...")
    converged, iterations = update_masses_selfconsistent(consensus, max_iterations=20)
    
    print(f"  Converged: {converged}")
    print(f"  Iterations: {iterations}")
    print(f"  Final m1: {node1.mass:.2e} kg")
    print(f"  Final m2: {node2.mass:.2e} kg")
    print()
    
    # Compute consensus at midpoint
    midpoint = np.array([0.0, 0.0, 0.0])
    rho_C, W = consensus.compute_at_point(midpoint)
    
    print(f"Consensus at midpoint:")
    print(f"  W (total weight): {W:.2e}")
    print(f"  ρ_C matrix:")
    print(f"    {rho_C}")
    print()
    
    # Decoherence rate
    gamma1 = decoherence_rate(node1, rho_C)
    print(f"Decoherence rate at midpoint: γ = {gamma1:.2e} s⁻¹")
    print(f"Coherence time: τ = {1/gamma1:.2e} s")
    print("="*70)

# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    example_two_bodies()