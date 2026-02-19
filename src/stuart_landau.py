"""
Stuart-Landau oscillator model for feedforward networks.

Implements the coupled Stuart-Landau system:
    dz_i/dt = (μ_i + iω_i)z_i - |z_i|^2 z_i + λ * z_{i-1}  (feedforward coupling)

Based on Ahmed, Cameron, Palacios et al. (2026).
"""

import numpy as np
from scipy.integrate import solve_ivp


def stuart_landau_feedforward_rhs(t, z_flat, mu, omega, lam):
    """RHS for feedforward Stuart-Landau network.

    Args:
        t: Time.
        z_flat: Flattened complex state [Re(z_1), Im(z_1), Re(z_2), Im(z_2), ...].
        mu: Excitation parameters, shape (N,).
        omega: Natural frequencies, shape (N,).
        lam: Coupling strength (scalar, real and positive).

    Returns:
        dz/dt as flattened real array.
    """
    N = len(mu)
    z = z_flat[0::2] + 1j * z_flat[1::2]

    dz = np.zeros(N, dtype=complex)
    for i in range(N):
        dz[i] = (mu[i] + 1j * omega[i]) * z[i] - np.abs(z[i])**2 * z[i]
        if i > 0:
            dz[i] += lam * z[i-1]
        elif i == 0:
            # Self-feedback for first oscillator (optional external drive)
            pass

    dz_flat = np.zeros(2 * N)
    dz_flat[0::2] = np.real(dz)
    dz_flat[1::2] = np.imag(dz)
    return dz_flat


def simulate_stuart_landau_ff(mu, omega, lam, T=200.0, dt=0.01,
                               z0=None, seed=None, t_transient=100.0):
    """Simulate feedforward Stuart-Landau network.

    Args:
        mu: Excitation parameters, shape (N,).
        omega: Natural frequencies, shape (N,).
        lam: Coupling strength.
        T: Total time.
        dt: Output step.
        z0: Initial complex states. If None, small random perturbations.
        seed: Random seed.
        t_transient: Transient to discard.

    Returns:
        t_out: Time array (after transient).
        z_out: Complex states, shape (T_out, N).
        is_phase_locked: Boolean, whether system reached phase-locked state.
    """
    N = len(mu)
    rng = np.random.default_rng(seed)

    if z0 is None:
        z0 = 0.1 * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    z0_flat = np.zeros(2 * N)
    z0_flat[0::2] = np.real(z0)
    z0_flat[1::2] = np.imag(z0)

    t_span = (0, T)
    t_eval = np.arange(0, T, dt)

    sol = solve_ivp(
        stuart_landau_feedforward_rhs, t_span, z0_flat,
        args=(mu, omega, lam),
        t_eval=t_eval, method='RK45',
        rtol=1e-8, atol=1e-10
    )

    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")

    # Reconstruct complex states
    z = sol.y[0::2] + 1j * sol.y[1::2]  # shape (N, T)
    z = z.T  # shape (T, N)

    # Discard transient
    mask = sol.t >= t_transient
    t_out = sol.t[mask]
    z_out = z[mask]

    # Check phase locking: frequency differences should vanish
    if len(z_out) > 100:
        phases = np.angle(z_out)
        # Compute instantaneous frequencies (finite differences)
        dphase = np.diff(np.unwrap(phases, axis=0), axis=0) / dt
        # Phase locked if frequency variance across oscillators is small
        freq_var = np.var(dphase[-100:], axis=0)
        is_phase_locked = np.all(freq_var < 0.01)
    else:
        is_phase_locked = False

    return t_out, z_out, is_phase_locked


def scan_phase_locking_region(lam, sigma_range, mu_tilde_range, n_sigma=40,
                               n_mu=40, n_trials=5, seed=42):
    """Scan parameter space for phase-locking in 2-cell feedforward network.

    Uses the reduced parameters: σ̃ = σ/λ (frequency mismatch), μ̃ = μ/λ (excitation).

    Args:
        lam: Coupling strength.
        sigma_range: (σ̃_min, σ̃_max) range of frequency mismatch.
        mu_tilde_range: (μ̃_min, μ̃_max) range of excitation.
        n_sigma, n_mu: Grid resolution.
        n_trials: Trials per point.
        seed: Random seed.

    Returns:
        sigma_grid: 1D array of σ̃ values.
        mu_grid: 1D array of μ̃ values.
        lock_fraction: 2D array of fraction locked, shape (n_mu, n_sigma).
    """
    sigma_grid = np.linspace(sigma_range[0], sigma_range[1], n_sigma)
    mu_grid = np.linspace(mu_tilde_range[0], mu_tilde_range[1], n_mu)
    lock_fraction = np.zeros((n_mu, n_sigma))

    for i, mu_t in enumerate(mu_grid):
        for j, sig_t in enumerate(sigma_grid):
            # Two-cell feedforward: node 1 has (μ₁, ω₁), node 2 has (μ₂, ω₂)
            # With barycentric condition: μ₁ + μ₂ = 2μ_nom, ω₁ + ω₂ = 2ω_nom
            # Reduced: μ = μ_nom (common), σ = (ω₁ - ω₂)/2
            mu_val = mu_t * lam
            sigma_val = sig_t * lam

            mu_arr = np.array([mu_val, mu_val])  # Same excitation
            omega_arr = np.array([sigma_val, -sigma_val])  # Frequency mismatch (zero mean)

            n_locked = 0
            for trial in range(n_trials):
                try:
                    _, _, locked = simulate_stuart_landau_ff(
                        mu_arr, omega_arr, lam, T=150.0, t_transient=80.0,
                        seed=seed + i * n_sigma * n_trials + j * n_trials + trial
                    )
                    if locked:
                        n_locked += 1
                except Exception:
                    pass
            lock_fraction[i, j] = n_locked / n_trials

    return sigma_grid, mu_grid, lock_fraction
