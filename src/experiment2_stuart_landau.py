"""
Experiment 2: Stuart-Landau feedforward networks — Disorder in excitation parameter.

Tests H2: Inhomogeneity in excitation parameter μ enhances amplification and
broadens the phase-locking region in feedforward networks.

Following Ahmed et al. (2026), we study 2-cell and 3-cell feedforward networks
with Stuart-Landau oscillators, comparing homogeneous vs. heterogeneous excitation.
"""

import sys
import json
import time
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from stuart_landau import simulate_stuart_landau_ff

SEED = 42
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def check_phase_locking_2cell(mu1, mu2, omega1, omega2, lam, n_trials=5, seed=42):
    """Check if 2-cell feedforward system achieves phase locking."""
    mu = np.array([mu1, mu2])
    omega = np.array([omega1, omega2])
    locked_count = 0
    amplitudes = []

    for trial in range(n_trials):
        try:
            t, z, locked = simulate_stuart_landau_ff(
                mu, omega, lam, T=150.0, t_transient=80.0,
                seed=seed + trial
            )
            if locked:
                locked_count += 1
            # Record final amplitude of output node
            amplitudes.append(np.mean(np.abs(z[-100:, -1])))
        except Exception:
            amplitudes.append(0.0)

    return locked_count / n_trials, np.mean(amplitudes) if amplitudes else 0.0


def experiment_2a_phase_locking_boundary():
    """Map the phase-locking boundary in (σ̃, μ̃) space for 2-cell network.

    Compare homogeneous (μ₁=μ₂) vs. heterogeneous (μ₁≠μ₂, mean preserved).
    """
    print("\n" + "=" * 60)
    print("Experiment 2a: Phase-locking boundary (2-cell feedforward)")
    print("=" * 60)

    lam = 1.0  # Coupling strength
    n_sigma = 35
    n_mu = 35
    n_trials = 5

    sigma_vals = np.linspace(-2.0, 2.0, n_sigma)
    mu_vals = np.linspace(0.01, 3.0, n_mu)

    # Case 1: Homogeneous (μ₁ = μ₂ = μ)
    print("\n  Scanning homogeneous case (μ₁ = μ₂)...")
    lock_homo = np.zeros((n_mu, n_sigma))
    amp_homo = np.zeros((n_mu, n_sigma))

    for i, mu_val in enumerate(mu_vals):
        if i % 10 == 0:
            print(f"    μ = {mu_val:.2f} ({i+1}/{n_mu})")
        for j, sig_val in enumerate(sigma_vals):
            frac, amp = check_phase_locking_2cell(
                mu_val, mu_val, sig_val, -sig_val, lam,
                n_trials=n_trials, seed=SEED + i * n_sigma + j
            )
            lock_homo[i, j] = frac
            amp_homo[i, j] = amp

    # Case 2: Heterogeneous excitation (μ₁ = μ + δ, μ₂ = μ - δ, barycentric)
    delta_mu = 0.5  # Excitation mismatch
    print(f"\n  Scanning heterogeneous case (μ₁ = μ+{delta_mu}, μ₂ = μ-{delta_mu})...")
    lock_hetero = np.zeros((n_mu, n_sigma))
    amp_hetero = np.zeros((n_mu, n_sigma))

    for i, mu_val in enumerate(mu_vals):
        if i % 10 == 0:
            print(f"    μ = {mu_val:.2f} ({i+1}/{n_mu})")
        for j, sig_val in enumerate(sigma_vals):
            frac, amp = check_phase_locking_2cell(
                mu_val + delta_mu, mu_val - delta_mu,
                sig_val, -sig_val, lam,
                n_trials=n_trials, seed=SEED + 100000 + i * n_sigma + j
            )
            lock_hetero[i, j] = frac
            amp_hetero[i, j] = amp

    results = {
        'sigma_vals': sigma_vals.tolist(),
        'mu_vals': mu_vals.tolist(),
        'lambda': lam,
        'delta_mu': delta_mu,
        'homogeneous': {
            'lock_fraction': lock_homo.tolist(),
            'amplitude': amp_homo.tolist(),
        },
        'heterogeneous': {
            'lock_fraction': lock_hetero.tolist(),
            'amplitude': amp_hetero.tolist(),
        }
    }

    # Compare areas
    area_homo = np.sum(lock_homo >= 0.5) / (n_mu * n_sigma)
    area_hetero = np.sum(lock_hetero >= 0.5) / (n_mu * n_sigma)
    print(f"\n  Phase-locking area (homo): {area_homo:.3f}")
    print(f"  Phase-locking area (hetero): {area_hetero:.3f}")
    print(f"  Ratio (hetero/homo): {area_hetero/area_homo:.3f}" if area_homo > 0 else "  Homo area = 0")

    results['area_homo'] = float(area_homo)
    results['area_hetero'] = float(area_hetero)

    return results


def experiment_2b_amplitude_enhancement():
    """Test if excitation heterogeneity enhances output amplitude.

    Fix μ̃ = 0.5 (near bifurcation), sweep frequency mismatch σ̃.
    Compare amplitude of output oscillator for homo vs hetero excitation.
    """
    print("\n" + "=" * 60)
    print("Experiment 2b: Amplitude enhancement from excitation disorder")
    print("=" * 60)

    lam = 1.0
    mu_base = 0.5
    delta_mu_values = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
    sigma_vals = np.linspace(0, 1.5, 30)
    n_trials = 10

    results = {
        'lambda': lam,
        'mu_base': mu_base,
        'sigma_vals': sigma_vals.tolist(),
        'delta_mu_values': delta_mu_values,
        'amplitude_curves': {}
    }

    for delta_mu in delta_mu_values:
        print(f"\n  δμ = {delta_mu:.2f}...")
        amps = np.zeros(len(sigma_vals))
        lock_frac = np.zeros(len(sigma_vals))

        for j, sig in enumerate(sigma_vals):
            trial_amps = []
            locked = 0
            for trial in range(n_trials):
                try:
                    t, z, is_locked = simulate_stuart_landau_ff(
                        np.array([mu_base + delta_mu, mu_base - delta_mu]),
                        np.array([sig, -sig]),  # barycentric frequencies
                        lam, T=150.0, t_transient=80.0,
                        seed=SEED + int(delta_mu * 1000) + j * n_trials + trial
                    )
                    trial_amps.append(np.mean(np.abs(z[-100:, -1])))
                    if is_locked:
                        locked += 1
                except Exception:
                    trial_amps.append(0.0)
            amps[j] = np.mean(trial_amps)
            lock_frac[j] = locked / n_trials

        results['amplitude_curves'][f'delta_mu_{delta_mu:.1f}'] = {
            'amplitudes': amps.tolist(),
            'lock_fractions': lock_frac.tolist(),
        }
        print(f"    Peak amplitude: {np.max(amps):.4f}, "
              f"mean lock fraction: {np.mean(lock_frac):.3f}")

    return results


def experiment_2c_three_cell():
    """Extend to 3-cell feedforward: 1→2→3.

    Test if excitation disorder enhances signal propagation through the chain.
    """
    print("\n" + "=" * 60)
    print("Experiment 2c: 3-cell feedforward network")
    print("=" * 60)

    lam = 1.0
    mu_base = 0.5
    sigma_vals = np.linspace(0, 1.2, 25)
    n_trials = 10

    # Configurations: [μ₁, μ₂, μ₃] all with mean = mu_base (barycentric)
    configs = {
        'homogeneous': [0.0, 0.0, 0.0],
        'increasing': [-0.3, 0.0, 0.3],
        'decreasing': [0.3, 0.0, -0.3],
        'V_shape': [0.3, -0.6, 0.3],  # sum = 0, mean-centered
        'peak': [-0.3, 0.6, -0.3],
    }

    results = {
        'lambda': lam,
        'mu_base': mu_base,
        'sigma_vals': sigma_vals.tolist(),
        'configs': {}
    }

    for config_name, deltas in configs.items():
        print(f"\n  Config: {config_name} δμ = {deltas}")
        mu_arr = np.array([mu_base + d for d in deltas])
        print(f"    μ = {mu_arr}, sum(δ) = {sum(deltas):.6f}")

        amps_out = np.zeros(len(sigma_vals))
        lock_frac = np.zeros(len(sigma_vals))

        for j, sig in enumerate(sigma_vals):
            # Barycentric frequencies: ω₁ + ω₂ + ω₃ = 0
            omega_arr = np.array([sig, 0, -sig])

            trial_amps = []
            locked = 0
            for trial in range(n_trials):
                try:
                    t, z, is_locked = simulate_stuart_landau_ff(
                        mu_arr, omega_arr, lam,
                        T=200.0, t_transient=100.0,
                        seed=SEED + hash(config_name) % (2**31) + j * n_trials + trial
                    )
                    trial_amps.append(np.mean(np.abs(z[-100:, -1])))
                    if is_locked:
                        locked += 1
                except Exception:
                    trial_amps.append(0.0)

            amps_out[j] = np.mean(trial_amps)
            lock_frac[j] = locked / n_trials

        results['configs'][config_name] = {
            'deltas': deltas,
            'mu': mu_arr.tolist(),
            'amplitudes': amps_out.tolist(),
            'lock_fractions': lock_frac.tolist(),
        }
        print(f"    Peak amplitude: {np.max(amps_out):.4f}")

    return results


def main():
    start_time = time.time()
    print("=" * 60)
    print("EXPERIMENT 2: Stuart-Landau Feedforward Networks")
    print("=" * 60)

    all_results = {}

    all_results['exp2a'] = experiment_2a_phase_locking_boundary()
    all_results['exp2b'] = experiment_2b_amplitude_enhancement()
    all_results['exp2c'] = experiment_2c_three_cell()

    outfile = RESULTS_DIR / "experiment2_stuart_landau.json"
    with open(outfile, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {outfile}")

    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
