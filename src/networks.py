"""
Network topology generation for synchronization experiments.

Provides adjacency matrices for various canonical network topologies,
along with their Laplacian spectra.
"""

import numpy as np
import networkx as nx


def complete_graph(N):
    """Complete graph K_N (all-to-all coupling)."""
    G = nx.complete_graph(N)
    return nx.to_numpy_array(G)


def ring_graph(N, k=1):
    """Ring graph with k nearest-neighbor connections on each side.

    k=1: simple ring (each node connected to 2 neighbors)
    k=2: each node connected to 4 neighbors, etc.
    """
    G = nx.circulant_graph(N, list(range(1, k + 1)))
    return nx.to_numpy_array(G)


def star_graph(N):
    """Star graph: one hub connected to N-1 leaves.

    Node 0 is the hub.
    """
    G = nx.star_graph(N - 1)
    return nx.to_numpy_array(G)


def circulant_graph(N, offsets):
    """Circulant graph C_N(offsets).

    Args:
        N: Number of nodes.
        offsets: List of connection offsets (positive integers).
    """
    G = nx.circulant_graph(N, offsets)
    return nx.to_numpy_array(G)


def path_graph(N):
    """Path graph (chain): 1-2-3-...-N."""
    G = nx.path_graph(N)
    return nx.to_numpy_array(G)


def cycle_graph(N):
    """Cycle graph (ring with k=1)."""
    G = nx.cycle_graph(N)
    return nx.to_numpy_array(G)


def small_world_graph(N, k=4, p=0.3, seed=42):
    """Watts-Strogatz small-world graph."""
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    return nx.to_numpy_array(G)


def barbell_graph(m1, m2=0):
    """Barbell graph: two complete graphs of size m1 connected by a path of length m2."""
    G = nx.barbell_graph(m1, m2)
    return nx.to_numpy_array(G)


def feedforward_graph(N):
    """Feedforward (directed chain): 1→2→3→...→N with self-loop on node 1.

    Returns a directed adjacency matrix where A[i,j]=1 means j influences i.
    """
    A = np.zeros((N, N))
    A[0, 0] = 1  # self-loop on first node
    for i in range(1, N):
        A[i, i-1] = 1  # node i-1 drives node i
    return A


def laplacian_spectrum(adj_matrix):
    """Compute the Laplacian eigenvalues of a graph.

    Returns sorted eigenvalues (ascending).
    """
    D = np.diag(np.sum(adj_matrix, axis=1))
    L = D - adj_matrix
    eigenvalues = np.sort(np.real(np.linalg.eigvalsh(L)))
    return eigenvalues


def algebraic_connectivity(adj_matrix):
    """Compute algebraic connectivity (second smallest Laplacian eigenvalue)."""
    eigs = laplacian_spectrum(adj_matrix)
    return eigs[1]


def spectral_gap_ratio(adj_matrix):
    """Compute ratio of largest to smallest nonzero Laplacian eigenvalue.

    A smaller ratio means better synchronizability (tighter eigenvalue spread).
    """
    eigs = laplacian_spectrum(adj_matrix)
    nonzero = eigs[eigs > 1e-10]
    if len(nonzero) < 2:
        return np.inf
    return nonzero[-1] / nonzero[0]


def get_topology_suite(N=10):
    """Return a suite of network topologies for experiments.

    Args:
        N: Number of nodes (default 10).

    Returns:
        Dictionary mapping topology name to adjacency matrix.
    """
    topologies = {
        'complete': complete_graph(N),
        'ring_k1': ring_graph(N, k=1),
        'ring_k2': ring_graph(N, k=2),
        'star': star_graph(N),
        'path': path_graph(N),
        'small_world': small_world_graph(N, k=4, p=0.3, seed=42),
    }
    return topologies


def get_topology_properties(adj_matrix, name=""):
    """Compute key properties of a network topology."""
    eigs = laplacian_spectrum(adj_matrix)
    nonzero = eigs[eigs > 1e-10]
    N = adj_matrix.shape[0]
    return {
        'name': name,
        'N': N,
        'num_edges': int(np.sum(adj_matrix) / 2),
        'algebraic_connectivity': nonzero[0] if len(nonzero) > 0 else 0,
        'spectral_gap_ratio': nonzero[-1] / nonzero[0] if len(nonzero) >= 2 else np.inf,
        'laplacian_eigenvalues': eigs,
        'mean_degree': np.mean(np.sum(adj_matrix, axis=1)),
    }
