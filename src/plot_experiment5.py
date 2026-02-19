"""Plot Experiment 5 results: Ring network deep dive."""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

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


def main():
    with open(RESULTS_DIR / "experiment5_ring_deep_dive.json") as f:
        data = json.load(f)

    # Figure 10: (K, δ) heatmaps
    configs = ['ring_k1_N10', 'ring_k1_N20', 'ring_k2_N10', 'ring_k2_N20']
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, key in enumerate(configs):
        if key not in data:
            continue
        d = data[key]
        K_vals = np.array(d['K_vals'])
        delta_vals = np.array(d['delta_vals'])
        r_grid = np.array(d['r_grid'])

        # Compute improvement over homogeneous (δ=0)
        homo_col = r_grid[:, 0:1]
        improvement = r_grid - homo_col

        ax = axes[idx]
        D, K = np.meshgrid(delta_vals, K_vals)
        im = ax.contourf(D, K, improvement, levels=np.linspace(-0.3, 0.35, 14),
                         cmap='RdBu_r', extend='both')
        ax.contour(D, K, improvement, levels=[0], colors='black', linewidths=2)
        plt.colorbar(im, ax=ax, label=r'$\Delta r$ (vs. homogeneous)')

        # Mark maximum improvement
        best_flat = np.argmax(improvement)
        bi, bj = np.unravel_index(best_flat, improvement.shape)
        ax.plot(delta_vals[bj], K_vals[bi], 'r*', markersize=15, markeredgecolor='black')

        N_val = d['N']
        k_val = d['k_ring']
        ax.set_xlabel(r'Disorder strength $\delta$')
        ax.set_ylabel('Coupling K')
        ax.set_title(f'Ring $k={k_val}$, $N={N_val}$\n'
                     f'Max $\\Delta r = {d["max_improvement"]:.3f}$')

    plt.suptitle('Synchronization Improvement from Disorder in Ring Networks',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig10_ring_disorder_heatmap.png", bbox_inches='tight')
    plt.close()
    print("Saved fig10_ring_disorder_heatmap.png")

    # Figure 11: Optimal δ as function of K
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for idx, (key, color, label) in enumerate([
        ('ring_k1_N10', 'blue', 'Ring k=1, N=10'),
        ('ring_k1_N20', 'red', 'Ring k=1, N=20'),
        ('ring_k2_N10', 'green', 'Ring k=2, N=10'),
        ('ring_k2_N20', 'purple', 'Ring k=2, N=20'),
    ]):
        if key not in data:
            continue
        d = data[key]
        K_vals = np.array(d['K_vals'])
        opt_delta = np.array(d['opt_delta'])
        opt_r = np.array(d['opt_r'])
        homo_r = np.array(d['homo_r'])

        axes[0].plot(K_vals, opt_delta, color=color, linewidth=2, label=label)
        axes[1].plot(K_vals, opt_r - homo_r, color=color, linewidth=2, label=label)

    axes[0].set_xlabel('Coupling K')
    axes[0].set_ylabel(r'Optimal disorder strength $\delta^*$')
    axes[0].set_title('Optimal Disorder Strength vs. Coupling')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel('Coupling K')
    axes[1].set_ylabel(r'Improvement $\Delta r$')
    axes[1].set_title('Synchronization Improvement from Optimal Disorder')
    axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig11_optimal_disorder_vs_K.png", bbox_inches='tight')
    plt.close()
    print("Saved fig11_optimal_disorder_vs_K.png")

    # Figure 12: Statistical test results
    if 'statistical_tests' in data:
        stats = data['statistical_tests']
        fig, ax = plt.subplots(figsize=(10, 6))

        names = list(stats.keys())
        means = [stats[n]['mean_diff'] for n in names]
        stds = [stats[n]['std_diff'] for n in names]
        pvals = [stats[n]['p_value'] for n in names]

        x = np.arange(len(names))
        colors = ['green' if m > 0 else 'red' for m in means]
        bars = ax.bar(x, means, yerr=stds, capsize=5, color=colors, alpha=0.7)

        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.set_xlabel('Configuration')
        ax.set_ylabel(r'Mean $\Delta r$ (hetero - homo)')
        ax.set_title('Statistical Tests: Disorder Enhancement')
        ax.set_xticks(x)
        ax.set_xticklabels([n.replace('ring_', '').replace('_', '\n') for n in names],
                           fontsize=8)

        for i, (m, p) in enumerate(zip(means, pvals)):
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
            ax.annotate(f'p={p:.4f}\n{sig}', xy=(i, m + stds[i] + 0.01),
                       ha='center', fontsize=8)

        plt.tight_layout()
        plt.savefig(FIGURES_DIR / "fig12_statistical_tests.png", bbox_inches='tight')
        plt.close()
        print("Saved fig12_statistical_tests.png")


if __name__ == "__main__":
    main()
