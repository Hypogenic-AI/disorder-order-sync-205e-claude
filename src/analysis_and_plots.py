"""
Analysis and visualization for all experiments.

Generates publication-quality figures and computes statistical tests.
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

RESULTS_DIR = Path(__file__).parent.parent / "results"
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 9,
    'figure.dpi': 150,
})


def plot_experiment1():
    """Plot Kuramoto disorder results."""
    with open(RESULTS_DIR / "experiment1_kuramoto.json") as f:
        data = json.load(f)

    # Figure 1: Order parameter vs coupling for each topology
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()

    topo_names = list(data.keys())
    colors = {
        'homogeneous': '#2196F3',
        'uniform_disorder': '#FF5722',
        'gaussian_disorder': '#4CAF50',
        'degree_correlated': '#9C27B0',
        'anti_degree_correlated': '#FF9800',
        'bimodal': '#795548',
    }
    labels = {
        'homogeneous': 'Homogeneous',
        'uniform_disorder': 'Uniform disorder',
        'gaussian_disorder': 'Gaussian disorder',
        'degree_correlated': 'Degree-correlated',
        'anti_degree_correlated': 'Anti-degree-corr.',
        'bimodal': 'Bimodal',
    }

    for idx, topo_name in enumerate(topo_names):
        ax = axes[idx]
        topo_data = data[topo_name]
        K_values = np.array(topo_data['K_values'])

        for dist_name, dist_data in topo_data['distributions'].items():
            r_means = np.array(dist_data['r_means'])
            r_stds = np.array(dist_data['r_stds'])
            color = colors.get(dist_name, 'gray')
            lw = 2.5 if dist_name == 'homogeneous' else 1.5
            ls = '-' if dist_name == 'homogeneous' else '--'

            ax.plot(K_values, r_means, color=color, linewidth=lw, linestyle=ls,
                    label=labels.get(dist_name, dist_name))
            ax.fill_between(K_values, r_means - r_stds, r_means + r_stds,
                           alpha=0.1, color=color)

        ax.set_xlabel('Coupling K')
        ax.set_ylabel('Order parameter r')
        ax.set_title(topo_name.replace('_', ' ').title())
        ax.set_ylim(-0.05, 1.05)
        ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
        ax.grid(True, alpha=0.3)

    axes[0].legend(loc='lower right', fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig1_kuramoto_sync_curves.png", bbox_inches='tight')
    plt.close()
    print("Saved fig1_kuramoto_sync_curves.png")

    # Figure 2: Critical coupling comparison (bar chart)
    fig, ax = plt.subplots(figsize=(12, 6))

    dist_names = ['homogeneous', 'uniform_disorder', 'gaussian_disorder',
                  'degree_correlated', 'bimodal']
    x = np.arange(len(topo_names))
    width = 0.15

    for di, dist_name in enumerate(dist_names):
        kc_vals = []
        for topo_name in topo_names:
            kc = data[topo_name]['distributions'][dist_name]['K_c']
            kc_vals.append(min(kc, 15))  # cap for display
        ax.bar(x + di * width, kc_vals, width, label=labels[dist_name],
               color=colors[dist_name], alpha=0.8)

    ax.set_xlabel('Network Topology')
    ax.set_ylabel('Critical Coupling K_c')
    ax.set_title('Critical Coupling: Homogeneous vs. Disordered')
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels([n.replace('_', '\n') for n in topo_names])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig2_critical_coupling_comparison.png", bbox_inches='tight')
    plt.close()
    print("Saved fig2_critical_coupling_comparison.png")

    return data


def plot_experiment2():
    """Plot Stuart-Landau feedforward results."""
    with open(RESULTS_DIR / "experiment2_stuart_landau.json") as f:
        data = json.load(f)

    # Figure 3: Phase-locking boundary comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    exp2a = data['exp2a']
    sigma = np.array(exp2a['sigma_vals'])
    mu = np.array(exp2a['mu_vals'])
    S, M = np.meshgrid(sigma, mu)

    lock_homo = np.array(exp2a['homogeneous']['lock_fraction'])
    lock_hetero = np.array(exp2a['heterogeneous']['lock_fraction'])

    im1 = axes[0].contourf(S, M, lock_homo, levels=np.linspace(0, 1, 11), cmap='RdYlGn')
    axes[0].contour(S, M, lock_homo, levels=[0.5], colors='black', linewidths=2)
    axes[0].set_xlabel(r'Frequency mismatch $\tilde{\sigma}$')
    axes[0].set_ylabel(r'Excitation $\tilde{\mu}$')
    axes[0].set_title('Homogeneous ($\\mu_1 = \\mu_2$)')
    plt.colorbar(im1, ax=axes[0], label='Phase-lock fraction')

    im2 = axes[1].contourf(S, M, lock_hetero, levels=np.linspace(0, 1, 11), cmap='RdYlGn')
    axes[1].contour(S, M, lock_hetero, levels=[0.5], colors='black', linewidths=2)
    axes[1].set_xlabel(r'Frequency mismatch $\tilde{\sigma}$')
    axes[1].set_ylabel(r'Excitation $\tilde{\mu}$')
    delta_mu = exp2a['delta_mu']
    axes[1].set_title(f'Heterogeneous ($\\delta\\mu = {delta_mu}$)')
    plt.colorbar(im2, ax=axes[1], label='Phase-lock fraction')

    plt.suptitle('Phase-Locking Region: 2-Cell Feedforward Stuart-Landau')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig3_phase_locking_boundary.png", bbox_inches='tight')
    plt.close()
    print("Saved fig3_phase_locking_boundary.png")

    # Figure 4: Amplitude enhancement curves
    fig, ax = plt.subplots(figsize=(8, 5))
    exp2b = data['exp2b']
    sigma_vals = np.array(exp2b['sigma_vals'])

    cmap = plt.cm.viridis
    delta_mu_list = exp2b['delta_mu_values']
    for i, delta_mu in enumerate(delta_mu_list):
        key = f'delta_mu_{delta_mu:.1f}'
        amps = np.array(exp2b['amplitude_curves'][key]['amplitudes'])
        color = cmap(i / max(len(delta_mu_list) - 1, 1))
        lw = 2.5 if delta_mu == 0.0 else 1.5
        ax.plot(sigma_vals, amps, color=color, linewidth=lw,
                label=f'$\\delta\\mu = {delta_mu}$')

    ax.set_xlabel(r'Frequency mismatch $\sigma$')
    ax.set_ylabel('Output amplitude $|z_2|$')
    ax.set_title('Amplitude Enhancement from Excitation Disorder')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig4_amplitude_enhancement.png", bbox_inches='tight')
    plt.close()
    print("Saved fig4_amplitude_enhancement.png")

    # Figure 5: 3-cell comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    exp2c = data['exp2c']
    sigma_vals = np.array(exp2c['sigma_vals'])

    colors_3c = plt.cm.Set1(np.linspace(0, 1, len(exp2c['configs'])))
    for i, (config_name, config_data) in enumerate(exp2c['configs'].items()):
        amps = np.array(config_data['amplitudes'])
        lock_frac = np.array(config_data['lock_fractions'])
        deltas = config_data['deltas']
        label = f"{config_name} ({deltas})"

        axes[0].plot(sigma_vals, amps, color=colors_3c[i], linewidth=2, label=label)
        axes[1].plot(sigma_vals, lock_frac, color=colors_3c[i], linewidth=2, label=label)

    axes[0].set_xlabel(r'Frequency mismatch $\sigma$')
    axes[0].set_ylabel('Output amplitude $|z_3|$')
    axes[0].set_title('3-Cell Feedforward: Output Amplitude')
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel(r'Frequency mismatch $\sigma$')
    axes[1].set_ylabel('Phase-lock fraction')
    axes[1].set_title('3-Cell Feedforward: Phase Locking')
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5_three_cell_feedforward.png", bbox_inches='tight')
    plt.close()
    print("Saved fig5_three_cell_feedforward.png")

    return data


def plot_experiment3():
    """Plot AISync results."""
    with open(RESULTS_DIR / "experiment3_aisync.json") as f:
        data = json.load(f)

    # Figure 6: AISync prevalence
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    for idx, N_key in enumerate(sorted(data.keys())):
        ax = axes[idx]
        N_data = data[N_key]
        N_val = N_data['N']
        K_values = np.array(N_data['K_values'])

        # Plot r_homo vs r_hetero for each graph
        for graph in N_data['graphs']:
            r_homo = np.array(graph['r_homo'])
            r_hetero = np.array(graph['r_hetero'])
            color = 'red' if graph['is_aisync'] else ('orange' if graph['disorder_helps'] else 'blue')
            alpha = 0.7 if graph['is_aisync'] else 0.3
            ax.plot(K_values, r_hetero - r_homo, color=color, alpha=alpha, linewidth=0.8)

        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.axhline(y=0.05, color='gray', linestyle=':', linewidth=0.8)
        ax.set_xlabel('Coupling K')
        ax.set_ylabel(r'$r_{hetero} - r_{homo}$')
        n_g = N_data['n_graphs']
        n_a = N_data['n_aisync']
        n_h = N_data['n_disorder_helps']
        ax.set_title(f'N={N_val}: {n_a}/{n_g} AISync, {n_h}/{n_g} disorder helps')
        ax.grid(True, alpha=0.3)

    plt.suptitle('Synchronization Improvement from Disorder (Circulant Graphs)')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6_aisync_prevalence.png", bbox_inches='tight')
    plt.close()
    print("Saved fig6_aisync_prevalence.png")

    # Figure 7: Spectral gap ratio vs improvement
    fig, ax = plt.subplots(figsize=(8, 6))

    for N_key in sorted(data.keys()):
        N_data = data[N_key]
        N_val = N_data['N']
        gap_ratios = []
        improvements = []
        for graph in N_data['graphs']:
            gap_ratios.append(graph['spectral_gap_ratio'])
            improvements.append(graph['max_improvement'])

        ax.scatter(gap_ratios, improvements, alpha=0.6, s=30, label=f'N={N_val}')

    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.axhline(y=0.05, color='gray', linestyle=':', linewidth=0.8, label='Threshold')
    ax.set_xlabel('Spectral gap ratio $\\lambda_N / \\lambda_2$')
    ax.set_ylabel('Max improvement $\\Delta r$')
    ax.set_title('Synchronization Improvement vs. Network Spectral Properties')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig7_spectral_vs_improvement.png", bbox_inches='tight')
    plt.close()
    print("Saved fig7_spectral_vs_improvement.png")

    return data


def plot_experiment4():
    """Plot optimal disorder results."""
    with open(RESULTS_DIR / "experiment4_optimal_disorder.json") as f:
        data = json.load(f)

    # Figure 8: Disorder strength sweep
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()

    sweep_data = data['strength_sweep']
    topo_names = list(sweep_data.keys())

    for idx, name in enumerate(topo_names):
        ax = axes[idx]
        sd = sweep_data[name]
        deltas = np.array(sd['delta_values'])
        r_means = np.array(sd['r_means'])
        r_stds = np.array(sd['r_stds'])

        ax.plot(deltas, r_means, 'b-', linewidth=2)
        ax.fill_between(deltas, r_means - r_stds, r_means + r_stds, alpha=0.2)
        ax.axhline(y=r_means[0], color='red', linestyle='--', linewidth=1.5,
                   label=f'Homo r = {r_means[0]:.3f}')

        best_idx = np.argmax(r_means)
        ax.axvline(x=deltas[best_idx], color='green', linestyle=':', linewidth=1.5,
                   label=f'Best $\\delta$ = {deltas[best_idx]:.2f}')

        ax.set_xlabel('Disorder strength $\\delta$')
        ax.set_ylabel('Order parameter r')
        ax.set_title(f'{name.replace("_", " ").title()} (K={sd["K"]:.1f})')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.suptitle('Effect of Disorder Strength on Synchronization')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig8_disorder_strength_sweep.png", bbox_inches='tight')
    plt.close()
    print("Saved fig8_disorder_strength_sweep.png")

    # Figure 9: Optimal vs. Homogeneous comparison bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    opt_data = data['optimization']
    names = list(opt_data.keys())
    x = np.arange(len(names))
    width = 0.35

    r_homo = [opt_data[n]['r_homogeneous'] for n in names]
    r_opt = [opt_data[n]['r_optimal'] for n in names]

    bars1 = ax.bar(x - width/2, r_homo, width, label='Homogeneous', color='#2196F3', alpha=0.8)
    bars2 = ax.bar(x + width/2, r_opt, width, label='Optimal disorder', color='#FF5722', alpha=0.8)

    ax.set_xlabel('Network Topology')
    ax.set_ylabel('Order parameter r')
    ax.set_title('Optimal Disorder vs. Homogeneous Synchronization')
    ax.set_xticks(x)
    ax.set_xticklabels([n.replace('_', '\n') for n in names])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    # Add improvement annotations
    for i, (rh, ro) in enumerate(zip(r_homo, r_opt)):
        improvement = ro - rh
        color = 'green' if improvement > 0 else 'red'
        ax.annotate(f'{improvement:+.3f}', xy=(i + width/2, ro),
                   xytext=(0, 5), textcoords='offset points',
                   ha='center', fontsize=9, color=color, weight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig9_optimal_vs_homogeneous.png", bbox_inches='tight')
    plt.close()
    print("Saved fig9_optimal_vs_homogeneous.png")

    return data


def compute_statistics():
    """Compute statistical tests for all experiments."""
    stats_results = {}

    # Experiment 1: Paired comparisons at each K
    try:
        with open(RESULTS_DIR / "experiment1_kuramoto.json") as f:
            data = json.load(f)

        exp1_stats = {}
        for topo_name, topo_data in data.items():
            dists = topo_data['distributions']
            homo_r = np.array(dists['homogeneous']['r_means'])

            for dist_name in ['uniform_disorder', 'gaussian_disorder', 'bimodal']:
                hetero_r = np.array(dists[dist_name]['r_means'])
                # Paired t-test across K values
                t_stat, p_value = stats.ttest_rel(hetero_r, homo_r)
                diff = hetero_r - homo_r
                cohen_d = np.mean(diff) / np.std(diff) if np.std(diff) > 0 else 0

                key = f"{topo_name}_{dist_name}"
                exp1_stats[key] = {
                    'mean_diff': float(np.mean(diff)),
                    't_stat': float(t_stat),
                    'p_value': float(p_value),
                    'cohen_d': float(cohen_d),
                    'significant': bool(p_value < 0.01),
                }

        stats_results['experiment1'] = exp1_stats
    except FileNotFoundError:
        print("Experiment 1 results not found, skipping")

    # Experiment 4: Paired test of optimal vs homogeneous
    try:
        with open(RESULTS_DIR / "experiment4_optimal_disorder.json") as f:
            data = json.load(f)

        opt = data['optimization']
        r_homo_list = [opt[n]['r_homogeneous'] for n in opt]
        r_opt_list = [opt[n]['r_optimal'] for n in opt]

        t_stat, p_value = stats.ttest_rel(r_opt_list, r_homo_list)
        diff = np.array(r_opt_list) - np.array(r_homo_list)
        cohen_d = np.mean(diff) / np.std(diff) if np.std(diff) > 0 else 0

        stats_results['experiment4_overall'] = {
            'mean_improvement': float(np.mean(diff)),
            't_stat': float(t_stat),
            'p_value': float(p_value),
            'cohen_d': float(cohen_d),
            'significant': bool(p_value < 0.01),
            'n_improved': int(np.sum(diff > 0)),
            'n_total': len(diff),
        }
    except FileNotFoundError:
        print("Experiment 4 results not found, skipping")

    # Save statistics
    with open(RESULTS_DIR / "statistical_tests.json", 'w') as f:
        json.dump(stats_results, f, indent=2)
    print(f"Statistics saved to {RESULTS_DIR / 'statistical_tests.json'}")

    return stats_results


def main():
    print("=" * 60)
    print("ANALYSIS AND VISUALIZATION")
    print("=" * 60)

    results_files = list(RESULTS_DIR.glob("experiment*.json"))
    print(f"Found {len(results_files)} result files: {[f.name for f in results_files]}")

    data = {}
    for f in sorted(results_files):
        with open(f) as fh:
            data[f.stem] = json.load(fh)

    if 'experiment1_kuramoto' in data:
        print("\nPlotting Experiment 1...")
        plot_experiment1()

    if 'experiment2_stuart_landau' in data:
        print("\nPlotting Experiment 2...")
        plot_experiment2()

    if 'experiment3_aisync' in data:
        print("\nPlotting Experiment 3...")
        plot_experiment3()

    if 'experiment4_optimal_disorder' in data:
        print("\nPlotting Experiment 4...")
        plot_experiment4()

    print("\nComputing statistics...")
    stats_results = compute_statistics()

    # Print summary
    print("\n" + "=" * 60)
    print("STATISTICAL SUMMARY")
    print("=" * 60)
    if 'experiment1' in stats_results:
        sig_count = sum(1 for v in stats_results['experiment1'].values() if v['significant'])
        total = len(stats_results['experiment1'])
        print(f"  Experiment 1: {sig_count}/{total} comparisons significant (p<0.01)")
        # Show top improvements
        sorted_comps = sorted(stats_results['experiment1'].items(),
                             key=lambda x: x[1]['mean_diff'], reverse=True)
        print("  Top 5 improvements:")
        for name, s in sorted_comps[:5]:
            print(f"    {name}: Δr = {s['mean_diff']:+.4f}, d = {s['cohen_d']:.2f}, p = {s['p_value']:.4f}")

    if 'experiment4_overall' in stats_results:
        s = stats_results['experiment4_overall']
        print(f"\n  Experiment 4 (Overall):")
        print(f"    Mean improvement: {s['mean_improvement']:+.4f}")
        print(f"    Topologies improved: {s['n_improved']}/{s['n_total']}")
        print(f"    t = {s['t_stat']:.3f}, p = {s['p_value']:.4f}, d = {s['cohen_d']:.2f}")

    print("\nAll figures saved to figures/")


if __name__ == "__main__":
    main()
