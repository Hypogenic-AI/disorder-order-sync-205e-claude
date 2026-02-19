"""
Experiment 1: Kuramoto model — Homogeneous vs. Heterogeneous synchronization
across multiple network topologies.

Tests H1: Zero-mean frequency disorder can lower or raise the critical coupling
depending on network topology.

For each topology, compares:
  - Homogeneous: ω_i = 0 for all i
  - Uniform disorder: ω_i ~ Uniform(-Δ, Δ), then centered to zero mean
  - Structured disorder: ω_i proportional to node degree deviation

All heterogeneous distributions satisfy the barycentric condition Σω_i = 0.
"""

import sys
import os
import json
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kuramoto import simulate_kuramoto, order_parameter
from networks import (
    complete_graph, ring_graph, star_graph, path_graph,
    cycle_graph, small_world_graph, get_topology_properties
)

# ─── Configuration ─────────────────────────────────────────────────────────
SEED = 42
N = 20  # Number of oscillators
N_TRIALS = 30  # Trials per configuration
K_VALUES = np.linspace(0.1, 12.0, 40)  # Coupling strength sweep
T_SIM = 60.0  # Simulation time
T_TRANSIENT = 30.0  # Transient to discard
DELTA = 1.0  # Disorder strength for uniform distribution

RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

np.random.seed(SEED)


def make_zero_mean(omega):
    """Enforce barycentric condition: Σω_i = 0."""
    return omega - np.mean(omega)


def generate_frequency_distributions(adj_matrix, N, delta=DELTA, seed=SEED):
    """Generate different zero-mean frequency distributions.

    Returns dict of name -> omega array.
    """
    rng = np.random.default_rng(seed)
    distributions = {}

    # Homogeneous
    distributions['homogeneous'] = np.zeros(N)

    # Uniform disorder (zero mean)
    omega_uniform = rng.uniform(-delta, delta, N)
    distributions['uniform_disorder'] = make_zero_mean(omega_uniform)

    # Gaussian disorder (zero mean)
    omega_gauss = rng.normal(0, delta / 2, N)
    distributions['gaussian_disorder'] = make_zero_mean(omega_gauss)

    # Degree-correlated disorder: ω_i ∝ (d_i - d̄)
    degrees = np.sum(adj_matrix, axis=1)
    omega_deg = degrees - np.mean(degrees)
    if np.max(np.abs(omega_deg)) > 0:
        omega_deg = delta * omega_deg / np.max(np.abs(omega_deg))
    distributions['degree_correlated'] = make_zero_mean(omega_deg)

    # Anti-degree-correlated disorder: ω_i ∝ -(d_i - d̄)
    omega_antideg = -omega_deg
    distributions['anti_degree_correlated'] = make_zero_mean(omega_antideg)

    # Bimodal disorder: half at +δ, half at -δ (zero mean by construction)
    omega_bimodal = np.array([delta if i < N // 2 else -delta for i in range(N)],
                             dtype=float)
    distributions['bimodal'] = make_zero_mean(omega_bimodal)

    return distributions


def run_topology_experiment(adj_matrix, topo_name):
    """Run full coupling sweep for one topology with all disorder types."""
    print(f"\n{'='*60}")
    print(f"Topology: {topo_name} (N={N})")
    print(f"{'='*60}")

    props = get_topology_properties(adj_matrix, topo_name)
    print(f"  Edges: {props['num_edges']}, Mean degree: {props['mean_degree']:.1f}")
    print(f"  Algebraic connectivity: {props['algebraic_connectivity']:.4f}")
    print(f"  Spectral gap ratio: {props['spectral_gap_ratio']:.4f}")

    distributions = generate_frequency_distributions(adj_matrix, N)

    results = {
        'topology': topo_name,
        'properties': {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                       for k, v in props.items()},
        'K_values': K_VALUES.tolist(),
        'distributions': {}
    }

    for dist_name, omega in distributions.items():
        print(f"\n  Distribution: {dist_name}")
        print(f"    ω range: [{omega.min():.3f}, {omega.max():.3f}], "
              f"mean: {omega.mean():.6f}, std: {omega.std():.3f}")

        r_means = np.zeros(len(K_VALUES))
        r_stds = np.zeros(len(K_VALUES))

        for ki, K in enumerate(K_VALUES):
            trial_rs = np.zeros(N_TRIALS)
            for trial in range(N_TRIALS):
                trial_seed = SEED + hash((topo_name, dist_name, ki, trial)) % (2**31)
                r_mean, _, _ = simulate_kuramoto(
                    omega, K, adj_matrix,
                    T=T_SIM, t_transient=T_TRANSIENT,
                    seed=abs(trial_seed)
                )
                trial_rs[trial] = r_mean
            r_means[ki] = np.mean(trial_rs)
            r_stds[ki] = np.std(trial_rs)

        # Estimate critical coupling (r > 0.5 threshold)
        above = r_means >= 0.5
        if np.any(above):
            idx = np.argmax(above)
            if idx > 0:
                K_c = np.interp(0.5, r_means[idx-1:idx+1], K_VALUES[idx-1:idx+1])
            else:
                K_c = K_VALUES[0]
        else:
            K_c = float('inf')

        results['distributions'][dist_name] = {
            'omega': omega.tolist(),
            'r_means': r_means.tolist(),
            'r_stds': r_stds.tolist(),
            'K_c': K_c,
            'omega_std': float(omega.std()),
        }
        print(f"    K_c ≈ {K_c:.3f}")

    return results


def main():
    start_time = time.time()
    print("=" * 60)
    print("EXPERIMENT 1: Kuramoto Disorder vs. Synchronization")
    print(f"N={N}, trials={N_TRIALS}, K range=[{K_VALUES[0]:.1f}, {K_VALUES[-1]:.1f}]")
    print("=" * 60)

    topologies = {
        'complete': complete_graph(N),
        'ring_k1': ring_graph(N, k=1),
        'ring_k2': ring_graph(N, k=2),
        'star': star_graph(N),
        'path': path_graph(N),
        'small_world': small_world_graph(N, k=4, p=0.3, seed=42),
    }

    all_results = {}
    for name, adj in topologies.items():
        all_results[name] = run_topology_experiment(adj, name)

    # Save results
    outfile = RESULTS_DIR / "experiment1_kuramoto.json"
    with open(outfile, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {outfile}")

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY: Critical Coupling K_c by Topology and Disorder Type")
    print("=" * 80)
    header = f"{'Topology':<15} {'Homogeneous':<13} {'Uniform':<13} {'Gaussian':<13} {'Degree-corr':<13} {'Bimodal':<13}"
    print(header)
    print("-" * 80)
    for name, res in all_results.items():
        dists = res['distributions']
        row = f"{name:<15}"
        for d in ['homogeneous', 'uniform_disorder', 'gaussian_disorder',
                  'degree_correlated', 'bimodal']:
            kc = dists[d]['K_c']
            row += f" {kc:<12.3f}"
        print(row)

    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
