"""
Kuramoto model simulation on arbitrary network topologies.

Implements the generalized Kuramoto model:
    dθ_i/dt = ω_i + (K/N) Σ_j A_ij sin(θ_j - θ_i)

where A is the adjacency matrix of the network.
"""

import numpy as np
from scipy.integrate import solve_ivp


def kuramoto_rhs(t, theta, omega, K, adj_matrix):
    """Right-hand side of the Kuramoto model on a network.

    Args:
        t: Time (unused, system is autonomous).
        theta: Phase angles, shape (N,).
        omega: Natural frequencies, shape (N,).
        K: Coupling strength (scalar).
        adj_matrix: Adjacency matrix, shape (N, N).

    Returns:
        dtheta/dt, shape (N,).
    """
    N = len(theta)
    # Compute pairwise phase differences: diff[i,j] = theta[j] - theta[i]
    diff = theta[np.newaxis, :] - theta[:, np.newaxis]
    # Coupling term: sum over neighbors
    coupling = (K / N) * np.sum(adj_matrix * np.sin(diff), axis=1)
    return omega + coupling


def order_parameter(theta):
    """Compute the Kuramoto order parameter r.

    Args:
        theta: Phase angles, shape (N,) or (T, N).

    Returns:
        r: Order parameter magnitude(s).
    """
    if theta.ndim == 1:
        z = np.mean(np.exp(1j * theta))
        return np.abs(z)
    else:
        z = np.mean(np.exp(1j * theta), axis=1)
        return np.abs(z)


def simulate_kuramoto(omega, K, adj_matrix, T=100.0, dt=0.01, theta0=None,
                      seed=None, t_transient=50.0):
    """Simulate Kuramoto model and return time-averaged order parameter.

    Args:
        omega: Natural frequencies, shape (N,). Should satisfy Σω_i = 0 (barycentric).
        K: Coupling strength.
        adj_matrix: Adjacency matrix, shape (N, N).
        T: Total simulation time.
        dt: Output time step.
        theta0: Initial phases. If None, drawn uniformly from [0, 2π).
        seed: Random seed for initial conditions.
        t_transient: Transient time to discard.

    Returns:
        r_mean: Time-averaged order parameter after transient.
        r_std: Standard deviation of order parameter after transient.
        r_final: Final order parameter value.
    """
    N = len(omega)
    if theta0 is None:
        rng = np.random.default_rng(seed)
        theta0 = rng.uniform(0, 2 * np.pi, N)

    t_span = (0, T)
    t_eval = np.arange(0, T, dt)

    sol = solve_ivp(
        kuramoto_rhs, t_span, theta0,
        args=(omega, K, adj_matrix),
        t_eval=t_eval, method='RK45',
        rtol=1e-8, atol=1e-10
    )

    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")

    # Compute order parameter over time
    r_t = order_parameter(sol.y.T)  # sol.y is (N, T), need (T, N)

    # Discard transient
    mask = sol.t >= t_transient
    r_steady = r_t[mask]

    return np.mean(r_steady), np.std(r_steady), r_steady[-1]


def sweep_coupling(omega, adj_matrix, K_values, n_trials=50, T=80.0,
                   t_transient=40.0, seed=42):
    """Sweep coupling strength K and measure order parameter.

    Args:
        omega: Natural frequencies, shape (N,).
        adj_matrix: Adjacency matrix.
        K_values: Array of coupling strengths to test.
        n_trials: Number of random initial conditions per K.
        T: Simulation time per trial.
        t_transient: Transient to discard.
        seed: Base random seed.

    Returns:
        r_means: Mean order parameter for each K, shape (len(K_values),).
        r_stds: Std of order parameter for each K, shape (len(K_values),).
    """
    r_means = np.zeros(len(K_values))
    r_stds = np.zeros(len(K_values))

    for i, K in enumerate(K_values):
        trial_r = np.zeros(n_trials)
        for t in range(n_trials):
            trial_seed = seed + i * n_trials + t
            r_mean, _, _ = simulate_kuramoto(
                omega, K, adj_matrix, T=T, t_transient=t_transient,
                seed=trial_seed
            )
            trial_r[t] = r_mean
        r_means[i] = np.mean(trial_r)
        r_stds[i] = np.std(trial_r)

    return r_means, r_stds


def estimate_critical_coupling(omega, adj_matrix, K_range=(0, 10), n_K=50,
                                n_trials=20, r_threshold=0.5, seed=42):
    """Estimate critical coupling K_c where order parameter crosses threshold.

    Uses bisection-like approach with sweep.

    Returns:
        K_c: Estimated critical coupling.
        K_values: Array of K values tested.
        r_means: Corresponding mean order parameters.
    """
    K_values = np.linspace(K_range[0], K_range[1], n_K)
    r_means, r_stds = sweep_coupling(
        omega, adj_matrix, K_values, n_trials=n_trials, seed=seed
    )

    # Find crossing point
    above = r_means >= r_threshold
    if not np.any(above):
        K_c = K_range[1]  # Never synchronized
    elif np.all(above):
        K_c = K_range[0]  # Always synchronized
    else:
        idx = np.argmax(above)
        if idx > 0:
            # Linear interpolation
            K_c = np.interp(r_threshold, r_means[idx-1:idx+1], K_values[idx-1:idx+1])
        else:
            K_c = K_values[0]

    return K_c, K_values, r_means, r_stds
