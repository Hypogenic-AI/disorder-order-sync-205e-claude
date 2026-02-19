"""
Experiment 5: Deep dive into disorder-enhanced synchronization in ring networks.

Experiment 4 revealed that small disorder (δ ≈ 0.16) dramatically improves
synchronization in ring networks near the transition. This experiment:

1. Maps the full (K, δ) parameter space for ring networks
2. Tests multiple N values to check if the effect persists at different scales
3. Provides statistical significance tests
4. Investigates the mechanism via phase portrait analysis
"""

import sys
import json
import time
import numpy as np
from scipy import stats
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kuramoto import simulate_kuramoto, order_parameter, kuramoto_rhs
from networks import ring_graph, laplacian_spectrum

SEED = 42
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def scan_K_delta_space(N, k_ring=1, n_K=30, n_delta=25, n_trials=20,
                        K_range=(0.5, 8.0), delta_range=(0, 2.0)):
    """Scan (K, δ) parameter space for ring graph.

    For each (K, δ), generate zero-mean disorder with strength δ and
    measure the order parameter.
    """
    adj = ring_graph(N, k=k_ring)
    K_vals = np.linspace(K_range[0], K_range[1], n_K)
    delta_vals = np.linspace(delta_range[0], delta_range[1], n_delta)

    r_grid = np.zeros((n_K, n_delta))
    r_std_grid = np.zeros((n_K, n_delta))

    for i, K in enumerate(K_vals):
        if i % 5 == 0:
            print(f"  K = {K:.2f} ({i+1}/{n_K})")
        for j, delta in enumerate(delta_vals):
            trial_rs = []
            for trial in range(n_trials):
                rng = np.random.default_rng(SEED + i * n_delta * n_trials + j * n_trials + trial)
                if delta == 0:
                    omega = np.zeros(N)
                else:
                    omega = rng.uniform(-delta, delta, N)
                    omega -= np.mean(omega)  # barycentric condition

                r_mean, _, _ = simulate_kuramoto(
                    omega, K, adj,
                    T=50.0, t_transient=25.0,
                    seed=SEED + i * 10000 + j * 100 + trial
                )
                trial_rs.append(r_mean)

            r_grid[i, j] = np.mean(trial_rs)
            r_std_grid[i, j] = np.std(trial_rs)

    return K_vals, delta_vals, r_grid, r_std_grid


def statistical_test_disorder_enhancement(N, k_ring, K, delta, n_trials=100):
    """Rigorous statistical test: does disorder at strength δ improve r at coupling K?

    Performs two-sample t-test and computes effect size.
    """
    adj = ring_graph(N, k=k_ring)

    r_homo = np.zeros(n_trials)
    r_hetero = np.zeros(n_trials)

    omega_homo = np.zeros(N)

    for trial in range(n_trials):
        rng = np.random.default_rng(SEED + trial * 2)
        omega_hetero = rng.uniform(-delta, delta, N)
        omega_hetero -= np.mean(omega_hetero)

        r_h, _, _ = simulate_kuramoto(omega_homo, K, adj, T=60.0, t_transient=30.0,
                                       seed=SEED + trial)
        r_het, _, _ = simulate_kuramoto(omega_hetero, K, adj, T=60.0, t_transient=30.0,
                                         seed=SEED + trial)  # same IC
        r_homo[trial] = r_h
        r_hetero[trial] = r_het

    # Paired t-test (same initial conditions)
    t_stat, p_value = stats.ttest_rel(r_hetero, r_homo)
    diff = r_hetero - r_homo
    cohen_d = np.mean(diff) / np.std(diff) if np.std(diff) > 0 else 0

    return {
        'r_homo_mean': float(np.mean(r_homo)),
        'r_homo_std': float(np.std(r_homo)),
        'r_hetero_mean': float(np.mean(r_hetero)),
        'r_hetero_std': float(np.std(r_hetero)),
        'mean_diff': float(np.mean(diff)),
        'std_diff': float(np.std(diff)),
        't_stat': float(t_stat),
        'p_value': float(p_value),
        'cohen_d': float(cohen_d),
        'n_trials': n_trials,
        'n_improved': int(np.sum(diff > 0)),
    }


def main():
    start_time = time.time()
    print("=" * 60)
    print("EXPERIMENT 5: Ring Network Disorder Deep Dive")
    print("=" * 60)

    all_results = {}

    # Part A: Scan (K, δ) space for different ring sizes
    print("\n--- Part A: (K, δ) Parameter Space ---")
    for N, k_ring in [(10, 1), (20, 1), (10, 2), (20, 2)]:
        key = f"ring_k{k_ring}_N{N}"
        print(f"\n{key}:")
        K_vals, delta_vals, r_grid, r_std_grid = scan_K_delta_space(
            N, k_ring, n_K=25, n_delta=20, n_trials=15,
            K_range=(0.5, 8.0), delta_range=(0, 2.0)
        )

        # Find the optimal δ for each K
        opt_delta_idx = np.argmax(r_grid, axis=1)
        opt_delta = delta_vals[opt_delta_idx]
        opt_r = np.array([r_grid[i, opt_delta_idx[i]] for i in range(len(K_vals))])
        homo_r = r_grid[:, 0]
        improvement = opt_r - homo_r

        print(f"  Max improvement: {np.max(improvement):.4f} at K={K_vals[np.argmax(improvement)]:.2f}, "
              f"δ={opt_delta[np.argmax(improvement)]:.3f}")

        all_results[key] = {
            'N': N,
            'k_ring': k_ring,
            'K_vals': K_vals.tolist(),
            'delta_vals': delta_vals.tolist(),
            'r_grid': r_grid.tolist(),
            'r_std_grid': r_std_grid.tolist(),
            'homo_r': homo_r.tolist(),
            'opt_delta': opt_delta.tolist(),
            'opt_r': opt_r.tolist(),
            'max_improvement': float(np.max(improvement)),
            'best_K': float(K_vals[np.argmax(improvement)]),
            'best_delta': float(opt_delta[np.argmax(improvement)]),
        }

    # Part B: Statistical tests for the most promising cases
    print("\n--- Part B: Statistical Tests ---")
    test_configs = [
        (10, 1, 3.0, 0.2),  # ring_k1, N=10
        (20, 1, 5.0, 0.15),  # ring_k1, N=20
        (10, 2, 1.5, 0.2),  # ring_k2, N=10
        (20, 2, 2.5, 0.15),  # ring_k2, N=20
        (10, 1, 2.0, 0.3),  # ring_k1, N=10, different K
        (20, 1, 3.0, 0.3),  # ring_k1, N=20, different K
    ]

    stat_results = {}
    for N, k, K, delta in test_configs:
        key = f"ring_k{k}_N{N}_K{K:.1f}_d{delta:.1f}"
        print(f"\n  Testing {key}...")
        result = statistical_test_disorder_enhancement(N, k, K, delta, n_trials=80)
        stat_results[key] = result
        sig = "***" if result['p_value'] < 0.001 else "**" if result['p_value'] < 0.01 else "*" if result['p_value'] < 0.05 else "ns"
        print(f"    r_homo={result['r_homo_mean']:.4f}±{result['r_homo_std']:.4f}, "
              f"r_hetero={result['r_hetero_mean']:.4f}±{result['r_hetero_std']:.4f}")
        print(f"    Δr={result['mean_diff']:+.4f}, d={result['cohen_d']:.2f}, "
              f"p={result['p_value']:.6f} {sig}")

    all_results['statistical_tests'] = stat_results

    # Save
    outfile = RESULTS_DIR / "experiment5_ring_deep_dive.json"
    with open(outfile, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {outfile}")

    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
