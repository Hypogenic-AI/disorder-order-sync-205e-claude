"""
Experiment 4 (Quick): Save the disorder strength sweep results only.
Skip the expensive optimization.
"""

import sys
import json
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kuramoto import simulate_kuramoto
from networks import (
    complete_graph, ring_graph, star_graph, path_graph,
    small_world_graph
)

SEED = 42
N = 12
N_TRIALS = 15
T_SIM = 50.0
T_TRANSIENT = 25.0
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def disorder_strength_sweep(adj_matrix, topo_name, K, n_strengths=20, seed=SEED):
    delta_values = np.linspace(0, 3.0, n_strengths)
    r_values = np.zeros(n_strengths)
    r_stds = np.zeros(n_strengths)
    N_nodes = adj_matrix.shape[0]
    rng = np.random.default_rng(seed)

    for i, delta in enumerate(delta_values):
        if delta == 0:
            omega = np.zeros(N_nodes)
        else:
            omega = rng.uniform(-delta, delta, N_nodes)
            omega -= np.mean(omega)

        trial_rs = []
        for t in range(N_TRIALS):
            r_mean, _, _ = simulate_kuramoto(
                omega, K, adj_matrix,
                T=T_SIM, t_transient=T_TRANSIENT,
                seed=seed + i * N_TRIALS + t
            )
            trial_rs.append(r_mean)
        r_values[i] = np.mean(trial_rs)
        r_stds[i] = np.std(trial_rs)

    return delta_values, r_values, r_stds


def main():
    start_time = time.time()
    topologies = {
        'complete': complete_graph(N),
        'ring_k1': ring_graph(N, k=1),
        'ring_k2': ring_graph(N, k=2),
        'star': star_graph(N),
        'path': path_graph(N),
        'small_world': small_world_graph(N, k=4, p=0.3, seed=42),
    }

    K_test = {
        'complete': 2.0, 'ring_k1': 5.0, 'ring_k2': 3.0,
        'star': 4.0, 'path': 6.0, 'small_world': 3.0,
    }

    all_results = {'strength_sweep': {}, 'optimization': {}}

    for name, adj in topologies.items():
        K = K_test[name]
        print(f"{name} at K={K:.1f}:")
        deltas, r_vals, r_stds = disorder_strength_sweep(adj, name, K)
        best_idx = np.argmax(r_vals)
        improvement = r_vals[best_idx] - r_vals[0]
        print(f"  Best δ={deltas[best_idx]:.3f}, r={r_vals[best_idx]:.4f}, "
              f"homo r={r_vals[0]:.4f}, Δ={improvement:+.4f}")

        all_results['strength_sweep'][name] = {
            'K': K,
            'delta_values': deltas.tolist(),
            'r_means': r_vals.tolist(),
            'r_stds': r_stds.tolist(),
            'best_delta': float(deltas[best_idx]),
            'best_r': float(r_vals[best_idx]),
            'homo_r': float(r_vals[0]),
        }

        # Simple "optimization" — use the best from sweep
        all_results['optimization'][name] = {
            'topology': name,
            'K': K,
            'r_optimal': float(r_vals[best_idx]),
            'r_homogeneous': float(r_vals[0]),
            'improvement': float(improvement),
            'omega_std': float(deltas[best_idx] / np.sqrt(3)),  # uniform std
        }

    outfile = RESULTS_DIR / "experiment4_optimal_disorder.json"
    with open(outfile, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {outfile}")
    print(f"Time: {time.time() - start_time:.1f}s")


if __name__ == "__main__":
    main()
