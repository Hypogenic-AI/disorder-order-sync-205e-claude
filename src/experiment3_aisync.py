"""
Experiment 3: AISync verification — Asymmetry-Induced Synchronization.

Tests H3: For a significant fraction of symmetric network topologies,
parameter heterogeneity is required for stable synchronization.

We verify the Zhang et al. (2017) result computationally using the MSF framework,
and extend it by testing with the barycentric condition.
"""

import sys
import json
import time
import numpy as np
import networkx as nx
from pathlib import Path
from itertools import combinations

sys.path.insert(0, str(Path(__file__).parent))
from kuramoto import simulate_kuramoto, order_parameter
from networks import laplacian_spectrum, spectral_gap_ratio

SEED = 42
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def generate_symmetric_graphs(N, max_graphs=200):
    """Generate vertex-transitive (symmetric) graphs on N nodes.

    For small N, these are circulant graphs. We enumerate circulant graphs
    as they are the main class of vertex-transitive graphs tractable to enumerate.
    """
    graphs = []
    # Circulant graphs: C_N(S) where S ⊂ {1, ..., N//2}
    possible_offsets = list(range(1, N // 2 + 1))
    # Enumerate non-empty subsets of offsets
    for r in range(1, len(possible_offsets) + 1):
        for subset in combinations(possible_offsets, r):
            G = nx.circulant_graph(N, list(subset))
            adj = nx.to_numpy_array(G)
            # Check it's connected
            if nx.is_connected(G):
                # Avoid duplicates (complete graph is reached multiple ways)
                is_dup = False
                for existing_adj, _, _ in graphs:
                    if np.array_equal(adj, existing_adj):
                        is_dup = True
                        break
                if not is_dup:
                    name = f"C_{N}({','.join(map(str, subset))})"
                    graphs.append((adj, name, list(subset)))
            if len(graphs) >= max_graphs:
                return graphs
    return graphs


def test_sync_with_msf_proxy(adj_matrix, N, is_heterogeneous=False,
                              delta=0.5, K=5.0, n_trials=20, seed=42):
    """Test synchronization using Kuramoto simulation as MSF proxy.

    For identical oscillators (homogeneous), complete sync is possible
    if K * λ₂(L) / N > some threshold related to dynamics.

    For heterogeneous, we test whether sync improves.

    Returns:
        mean_r: Mean order parameter achieved.
    """
    if is_heterogeneous:
        rng = np.random.default_rng(seed)
        omega = rng.uniform(-delta, delta, N)
        omega -= np.mean(omega)  # barycentric condition
    else:
        omega = np.zeros(N)

    trial_rs = []
    for trial in range(n_trials):
        r_mean, _, _ = simulate_kuramoto(
            omega, K, adj_matrix,
            T=50.0, t_transient=25.0,
            seed=seed + trial
        )
        trial_rs.append(r_mean)

    return np.mean(trial_rs), np.std(trial_rs)


def test_aisync_condition(adj_matrix, N, name, K_values=None, delta=0.5,
                           n_trials=15, seed=42):
    """Test whether a graph exhibits AISync-like behavior.

    AISync condition (adapted):
    - Homogeneous system does NOT synchronize well (r_homo < threshold)
    - Heterogeneous system DOES synchronize well (r_hetero > threshold)

    We test across a range of K values.
    """
    if K_values is None:
        K_values = np.linspace(1.0, 15.0, 20)

    r_homo = np.zeros(len(K_values))
    r_hetero = np.zeros(len(K_values))

    for i, K in enumerate(K_values):
        r_h, _ = test_sync_with_msf_proxy(
            adj_matrix, N, is_heterogeneous=False, K=K,
            n_trials=n_trials, seed=seed + i * 100
        )
        r_het, _ = test_sync_with_msf_proxy(
            adj_matrix, N, is_heterogeneous=True, delta=delta, K=K,
            n_trials=n_trials, seed=seed + i * 100 + 50
        )
        r_homo[i] = r_h
        r_hetero[i] = r_het

    return K_values, r_homo, r_hetero


def main():
    start_time = time.time()
    print("=" * 60)
    print("EXPERIMENT 3: AISync Verification")
    print("=" * 60)

    all_results = {}

    # Test for N = 6, 8, 10 (small enough for enumeration)
    for N in [6, 8, 10]:
        print(f"\n{'='*50}")
        print(f"N = {N}: Enumerating symmetric (circulant) graphs...")
        graphs = generate_symmetric_graphs(N, max_graphs=100)
        print(f"  Found {len(graphs)} connected circulant graphs")

        n_aisync = 0
        n_disorder_helps = 0
        graph_results = []

        K_values = np.linspace(1.0, 15.0, 15)

        for idx, (adj, name, offsets) in enumerate(graphs):
            if idx % 5 == 0:
                print(f"  Testing {name} ({idx+1}/{len(graphs)})...")

            eigs = laplacian_spectrum(adj)
            gap_ratio = spectral_gap_ratio(adj)

            K_arr, r_homo, r_hetero = test_aisync_condition(
                adj, N, name, K_values=K_values,
                delta=0.5, n_trials=10, seed=SEED + idx * 1000
            )

            # Check AISync: hetero syncs better at some K where homo doesn't
            # "Disorder helps" = r_hetero > r_homo + 0.05 at some K
            improvement = r_hetero - r_homo
            max_improvement = np.max(improvement)
            best_K_idx = np.argmax(improvement)

            is_aisync = False
            disorder_helps = max_improvement > 0.05

            # Stricter AISync: homo never reaches r > 0.7, but hetero does
            homo_max = np.max(r_homo)
            hetero_max = np.max(r_hetero)
            if homo_max < 0.7 and hetero_max > 0.7:
                is_aisync = True
                n_aisync += 1

            if disorder_helps:
                n_disorder_helps += 1

            graph_results.append({
                'name': name,
                'offsets': offsets,
                'spectral_gap_ratio': float(gap_ratio),
                'laplacian_eigs': eigs.tolist(),
                'r_homo': r_homo.tolist(),
                'r_hetero': r_hetero.tolist(),
                'max_improvement': float(max_improvement),
                'best_K': float(K_arr[best_K_idx]),
                'is_aisync': bool(is_aisync),
                'disorder_helps': bool(disorder_helps),
            })

        all_results[f'N_{N}'] = {
            'N': N,
            'n_graphs': len(graphs),
            'n_aisync': n_aisync,
            'n_disorder_helps': n_disorder_helps,
            'aisync_fraction': n_aisync / len(graphs) if graphs else 0,
            'disorder_helps_fraction': n_disorder_helps / len(graphs) if graphs else 0,
            'K_values': K_values.tolist(),
            'graphs': graph_results,
        }

        print(f"\n  N={N} Summary:")
        print(f"    Graphs tested: {len(graphs)}")
        print(f"    AISync-like: {n_aisync} ({100*n_aisync/len(graphs):.1f}%)")
        print(f"    Disorder helps: {n_disorder_helps} ({100*n_disorder_helps/len(graphs):.1f}%)")

    outfile = RESULTS_DIR / "experiment3_aisync.json"
    with open(outfile, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {outfile}")

    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
