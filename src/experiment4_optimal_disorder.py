"""
Experiment 4: Optimal disorder distributions.

Tests H4: The benefit of disorder depends on network topology, and we can
find optimal zero-mean distributions that maximize synchronization.

For each topology where disorder helps, we search for the distribution
that maximizes the order parameter at a fixed coupling strength.
"""

import sys
import json
import time
import numpy as np
from scipy.optimize import minimize, differential_evolution
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kuramoto import simulate_kuramoto
from networks import (
    complete_graph, ring_graph, star_graph, path_graph,
    small_world_graph, laplacian_spectrum, get_topology_properties
)

SEED = 42
N = 12  # Moderate size for optimization
N_TRIALS = 15
T_SIM = 50.0
T_TRANSIENT = 25.0
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def evaluate_disorder(omega_free, adj_matrix, K, n_trials=N_TRIALS, seed=SEED):
    """Evaluate synchronization for a given frequency distribution.

    omega_free has N-1 free parameters; the Nth frequency is set to enforce
    the barycentric condition (zero mean).

    Returns negative order parameter (for minimization).
    """
    N = adj_matrix.shape[0]
    omega = np.zeros(N)
    omega[:N-1] = omega_free
    omega[N-1] = -np.sum(omega_free)  # barycentric condition

    trial_rs = []
    for t in range(n_trials):
        r_mean, _, _ = simulate_kuramoto(
            omega, K, adj_matrix,
            T=T_SIM, t_transient=T_TRANSIENT,
            seed=seed + t
        )
        trial_rs.append(r_mean)

    return -np.mean(trial_rs)  # negative because we minimize


def optimize_disorder_for_topology(adj_matrix, topo_name, K, delta_max=2.0):
    """Find the zero-mean frequency distribution that maximizes synchronization.

    Uses differential evolution (global optimizer) with bounds [-delta_max, delta_max].
    """
    N_nodes = adj_matrix.shape[0]
    bounds = [(-delta_max, delta_max)] * (N_nodes - 1)

    print(f"  Optimizing disorder for {topo_name} at K={K:.2f}...")

    result = differential_evolution(
        evaluate_disorder,
        bounds,
        args=(adj_matrix, K),
        seed=SEED,
        maxiter=80,
        popsize=15,
        tol=1e-4,
        disp=False
    )

    # Reconstruct full omega
    omega_opt = np.zeros(N_nodes)
    omega_opt[:N_nodes-1] = result.x
    omega_opt[N_nodes-1] = -np.sum(result.x)
    r_opt = -result.fun

    # Compare with homogeneous
    omega_homo = np.zeros(N_nodes)
    r_homo = -evaluate_disorder(omega_homo[:N_nodes-1], adj_matrix, K)

    print(f"    Homogeneous r = {r_homo:.4f}")
    print(f"    Optimal disorder r = {r_opt:.4f}")
    print(f"    Improvement: {r_opt - r_homo:+.4f}")
    print(f"    ω_opt: [{', '.join(f'{w:.3f}' for w in omega_opt)}]")
    print(f"    ω_opt std: {np.std(omega_opt):.4f}")

    return {
        'topology': topo_name,
        'K': K,
        'omega_optimal': omega_opt.tolist(),
        'omega_std': float(np.std(omega_opt)),
        'r_optimal': float(r_opt),
        'r_homogeneous': float(r_homo),
        'improvement': float(r_opt - r_homo),
        'optimizer_success': result.success,
        'optimizer_message': result.message,
    }


def disorder_strength_sweep(adj_matrix, topo_name, K, n_strengths=20, seed=SEED):
    """Sweep disorder strength and measure synchronization.

    For a given topology and coupling, vary the standard deviation of a
    uniform zero-mean distribution and measure the order parameter.
    """
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
            omega -= np.mean(omega)  # barycentric

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
    print("=" * 60)
    print("EXPERIMENT 4: Optimal Disorder Distributions")
    print(f"N={N}, trials={N_TRIALS}")
    print("=" * 60)

    topologies = {
        'complete': complete_graph(N),
        'ring_k1': ring_graph(N, k=1),
        'ring_k2': ring_graph(N, k=2),
        'star': star_graph(N),
        'path': path_graph(N),
        'small_world': small_world_graph(N, k=4, p=0.3, seed=42),
    }

    all_results = {
        'optimization': {},
        'strength_sweep': {},
    }

    # Part A: Disorder strength sweep
    print("\n" + "="*50)
    print("Part A: Disorder Strength Sweep")
    print("="*50)

    # Test at moderate coupling (K where homogeneous r ≈ 0.3-0.7)
    K_test = {
        'complete': 2.0,
        'ring_k1': 5.0,
        'ring_k2': 3.0,
        'star': 4.0,
        'path': 6.0,
        'small_world': 3.0,
    }

    for name, adj in topologies.items():
        K = K_test[name]
        print(f"\n  {name} at K={K:.1f}:")
        deltas, r_vals, r_stds = disorder_strength_sweep(adj, name, K)

        # Find optimal disorder strength
        best_idx = np.argmax(r_vals)
        print(f"    Best δ = {deltas[best_idx]:.3f}, r = {r_vals[best_idx]:.4f}")
        print(f"    Homogeneous r = {r_vals[0]:.4f}")
        print(f"    Improvement: {r_vals[best_idx] - r_vals[0]:+.4f}")

        all_results['strength_sweep'][name] = {
            'K': K,
            'delta_values': deltas.tolist(),
            'r_means': r_vals.tolist(),
            'r_stds': r_stds.tolist(),
            'best_delta': float(deltas[best_idx]),
            'best_r': float(r_vals[best_idx]),
            'homo_r': float(r_vals[0]),
        }

    # Part B: Full optimization for topologies where disorder helps
    print("\n" + "="*50)
    print("Part B: Optimal Distribution Search")
    print("="*50)

    for name, adj in topologies.items():
        K = K_test[name]
        result = optimize_disorder_for_topology(adj, name, K, delta_max=2.0)
        all_results['optimization'][name] = result

    # Save results
    outfile = RESULTS_DIR / "experiment4_optimal_disorder.json"
    with open(outfile, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {outfile}")

    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
