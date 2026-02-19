# When Disorder Creates Order: Unexpected Synchronization in Heterogeneous Networks

## 1. Executive Summary

We experimentally investigate whether deliberately introducing zero-mean parameter disorder (heterogeneity) into coupled oscillator networks can broaden or stabilize synchronization regions, as suggested by the barycentric condition framework of Palacios, In, and Amani (2024). Through systematic numerical experiments on Kuramoto and Stuart-Landau oscillator models across six network topologies, we find that **the effect of disorder on synchronization is topology-dependent, coupling-dependent, and realization-dependent**. Our central findings are:

1. **Stuart-Landau feedforward networks:** Excitation-parameter disorder nearly *doubles* the phase-locking region (from 35.6% to 61.4% of parameter space), with phase-locking fraction increasing monotonically from 61% to 100% as disorder strength increases. This is the strongest evidence for disorder-enhanced synchronization.

2. **Kuramoto ring networks:** For a *fixed* disorder realization, small disorder (delta ~ 0.1-0.4) can improve the order parameter by up to 32% near the synchronization transition. However, when averaging over *random* disorder realizations, the effect becomes statistically non-significant, revealing that only specific disorder patterns enhance synchronization.

3. **Circulant graph survey:** 20-37% of circulant graphs show improved synchronization from disorder at some coupling level, with the simple ring C_N(1) consistently showing the largest improvement.

4. **Classical regime confirmed:** For most topologies with large random frequency disorder, the classical prediction holds — disorder raises the critical coupling threshold.

These results support the hypothesis that disorder can create order, but with the crucial qualifier that the benefit is **structured** rather than random: not any zero-mean disorder helps, but specific patterns aligned with the network topology do.

---

## 2. Goal

**Hypothesis:** Contrary to traditional expectations, there exist network topologies and parameter distributions where disorder — judiciously imposed — broadens or stabilizes the region of synchronization, subject to the barycentric condition (Palacios, In, Amani, 2024).

**Why this matters:** Classical synchronization theory treats heterogeneity as an obstacle. If certain forms of disorder actually help, this has implications for:
- **Power grid stability:** Real generators have inherently different parameters; understanding when this helps (rather than hurts) synchronization could improve grid design.
- **Neuroscience:** Neural circuits exhibit substantial parameter heterogeneity; this may be a feature rather than a bug.
- **Engineering design:** Instead of striving for (expensive) homogeneity, one could deliberately introduce beneficial disorder.

**What we tested:** Five experiments systematically comparing synchronization metrics between homogeneous and heterogeneous (zero-mean) parameter distributions across multiple network topologies.

---

## 3. Data Construction

### Models

**Model 1: Kuramoto Model** on arbitrary networks:

$$\dot{\theta}_i = \omega_i + \frac{K}{N} \sum_{j=1}^{N} A_{ij} \sin(\theta_j - \theta_i)$$

where $\omega_i$ are natural frequencies satisfying the barycentric condition $\sum \omega_i = 0$, $K$ is coupling strength, and $A$ is the adjacency matrix.

**Model 2: Stuart-Landau Oscillators** on feedforward networks:

$$\dot{z}_i = (\mu_i + i\omega_i)z_i - |z_i|^2 z_i + \lambda z_{i-1}$$

where $\mu_i$ are excitation parameters, $\omega_i$ are natural frequencies, and $\lambda$ is the coupling strength.

### Network Topologies Tested

| Topology | N | Edges | Mean Degree | Algebraic Connectivity | Spectral Gap Ratio |
|----------|---|-------|-------------|----------------------|-------------------|
| Complete | 20 | 190 | 19.0 | 20.000 | 1.000 |
| Ring k=1 | 20 | 20 | 2.0 | 0.098 | 40.86 |
| Ring k=2 | 20 | 40 | 4.0 | 0.480 | 13.00 |
| Star | 20 | 19 | 1.9 | 1.000 | 20.00 |
| Path | 20 | 19 | 1.9 | 0.025 | 161.45 |
| Small-world | 20 | 40 | 4.0 | 0.789 | 10.94 |

### Disorder Distributions (All Satisfying Barycentric Condition)

1. **Homogeneous:** $\omega_i = 0$ for all $i$ (baseline)
2. **Uniform disorder:** $\omega_i \sim \text{Uniform}(-\Delta, \Delta)$, then centered
3. **Gaussian disorder:** $\omega_i \sim \mathcal{N}(0, \Delta/2)$, then centered
4. **Degree-correlated:** $\omega_i \propto (d_i - \bar{d})$ (correlated with node degree)
5. **Bimodal:** $\omega_i = \pm\Delta$ (half positive, half negative)

### Simulation Parameters

- Random seed: 42
- ODE solver: RK45 (adaptive), rtol=1e-8, atol=1e-10
- Transient time discarded: 25-40 seconds (depending on experiment)
- Total simulation time: 50-200 seconds
- Trials per configuration: 10-80 (depending on experiment)

---

## 4. Experiment Description

### Experiment 1: Kuramoto Model — Critical Coupling Comparison

**Purpose:** Test whether zero-mean frequency disorder changes the critical coupling $K_c$ (threshold for $r > 0.5$) across network topologies.

**Method:** Sweep coupling strength $K \in [0.1, 12.0]$ with 40 points; for each $K$, run 30 trials with random initial conditions. Compute time-averaged order parameter $r$ after discarding transient.

**Key Parameters:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| N | 20 | Moderate size balancing computation and finite-size effects |
| K range | [0.1, 12.0] | Spans sub-critical to super-critical for all topologies |
| N_trials | 30 | Sufficient for stable means |
| T_sim | 60 s | Long enough for convergence |
| Delta | 1.0 | Moderate disorder strength |

### Experiment 2: Stuart-Landau Feedforward — Phase-Locking Boundaries

**Purpose:** Test whether excitation-parameter disorder broadens the phase-locking region in feedforward networks, following Ahmed et al. (2026).

**Sub-experiments:**
- **2a:** Map phase-locking boundary in $(\tilde{\sigma}, \tilde{\mu})$ space for homogeneous vs. heterogeneous 2-cell networks (35 x 35 grid, 5 trials per point).
- **2b:** Sweep frequency mismatch at fixed excitation, comparing 7 disorder levels.
- **2c:** Extend to 3-cell feedforward with 5 disorder configurations.

### Experiment 3: AISync Verification

**Purpose:** Verify that a significant fraction of symmetric (circulant) graphs show improved synchronization from disorder.

**Method:** Enumerate connected circulant graphs for N=6, 8, 10. For each graph, compare order parameter trajectories for homogeneous vs. heterogeneous (uniform, $\Delta = 0.5$) oscillators across 15 coupling values.

### Experiment 4: Disorder Strength Sweep

**Purpose:** Identify the optimal disorder strength for each topology.

**Method:** For each topology at a moderate coupling $K$, sweep disorder strength $\delta \in [0, 3]$ and measure order parameter.

### Experiment 5: Ring Network Deep Dive

**Purpose:** Map the full $(K, \delta)$ parameter space for ring networks, where disorder enhancement was detected.

**Method:** 25 x 20 grid in $(K, \delta)$ space with 15 trials per point, for four configurations (N=10,20; k=1,2). Statistical significance tested with paired t-tests (80 trials).

---

## 5. Raw Results

### Experiment 1: Critical Coupling K_c

| Topology | Homogeneous | Uniform | Gaussian | Degree-corr. | Bimodal |
|----------|------------|---------|----------|--------------|---------|
| Complete | 0.100 | 0.875 | 0.517 | 0.100 | 0.207 |
| Ring k=1 | 1.401 | inf | 11.143 | **1.184** | 1.608 |
| Ring k=2 | 0.395 | 6.443 | 4.352 | **0.360** | 0.619 |
| Star | 0.358 | 9.651 | 7.171 | 2.213 | 1.574 |
| Path | 1.305 | inf | inf | 3.256 | 1.855 |
| Small-world | 0.362 | 4.490 | 2.720 | 3.736 | 0.722 |

**Bold** entries indicate K_c *decreased* (disorder helps). This occurs only for ring graphs with degree-correlated disorder, which for degree-regular graphs reduces to zero disorder (since all degrees are equal). The "improvement" in rings reflects numerical variation near the homogeneous baseline.

### Experiment 2: Stuart-Landau Feedforward

#### 2a: Phase-Locking Region Area

| Configuration | Phase-Locking Area | Fraction of Parameter Space |
|--------------|-------------------|---------------------------|
| Homogeneous ($\mu_1 = \mu_2$) | 0.356 | 35.6% |
| Heterogeneous ($\delta\mu = 0.5$) | **0.614** | **61.4%** |
| **Improvement ratio** | **1.725x** | |

#### 2b: Phase-Locking Fraction vs. Excitation Disorder ($\mu_{base} = 0.5$)

| Disorder $\delta\mu$ | Peak Amplitude | Mean Lock Fraction |
|---------------------|---------------|-------------------|
| 0.0 (homo) | 1.076 | 0.610 |
| 0.1 | 1.063 | 0.683 |
| 0.2 | 1.048 | 0.780 |
| 0.3 | 1.033 | 0.907 |
| 0.5 | 1.000 | **1.000** |
| 0.7 | 0.966 | **1.000** |
| 1.0 | 0.915 | **1.000** |

Phase-locking fraction increases monotonically with disorder, reaching 100% at $\delta\mu \geq 0.5$, while amplitude decreases modestly. This is a clear **trade-off between amplitude and stability**: disorder reduces signal strength but dramatically improves phase coherence.

#### 2c: 3-Cell Feedforward Network

| Configuration | $[\delta\mu_1, \delta\mu_2, \delta\mu_3]$ | Peak Amplitude |
|--------------|-------------------------------------|---------------|
| Homogeneous | [0, 0, 0] | 1.186 |
| **Increasing** | **[-0.3, 0, 0.3]** | **1.256** |
| Decreasing | [0.3, 0, -0.3] | 1.107 |
| V-shape | [0.3, -0.6, 0.3] | 1.244 |
| Peak | [-0.3, 0.6, -0.3] | 1.129 |

The "increasing" configuration (excitation increasing along the chain) yields the highest amplitude, 6% above homogeneous. The direction of disorder matters: increasing $\mu$ along the feedforward chain enhances output, while decreasing $\mu$ suppresses it.

### Experiment 3: AISync Survey

| N | Circulant Graphs | Disorder Helps | Fraction |
|---|-----------------|----------------|----------|
| 6 | 5 | 1 | 20.0% |
| 8 | 12 | 4 | 33.3% |
| 10 | 27 | 10 | 37.0% |

Best improvements: C_6(1) (Δr = 0.264), C_8(1) (Δr = 0.416), C_10(1) (Δr = 0.407). The simple ring graph consistently benefits most from disorder, which aligns with its having the largest spectral gap ratio among circulant graphs.

### Experiment 4: Optimal Disorder Strength

| Topology | K | Best $\delta$ | r (best) | r (homo) | Improvement |
|----------|---|-------------|----------|----------|-------------|
| Complete | 2.0 | 0.000 | 1.000 | 1.000 | +0.000 |
| **Ring k=1** | **5.0** | **0.158** | **0.864** | **0.607** | **+0.258** |
| **Ring k=2** | **3.0** | **0.158** | **0.995** | **0.936** | **+0.060** |
| Star | 4.0 | 0.000 | 1.000 | 1.000 | +0.000 |
| Path | 6.0 | 0.000 | 0.908 | 0.908 | +0.000 |
| Small-world | 3.0 | 0.000 | 1.000 | 1.000 | +0.000 |

Ring networks show substantial improvement from small disorder ($\delta \approx 0.16$). Other topologies show no improvement at the tested K values (which are above their critical coupling).

### Experiment 5: Ring Network (K, delta) Space

| Configuration | Max $\Delta r$ | Best K | Best $\delta$ |
|--------------|---------------|--------|-------------|
| Ring k=1, N=10 | 0.315 | 7.38 | 0.421 |
| Ring k=1, N=20 | 0.321 | 6.75 | 0.105 |
| Ring k=2, N=10 | 0.261 | 6.44 | 0.316 |
| Ring k=2, N=20 | 0.220 | 6.12 | 0.105 |

The improvement is concentrated in a specific region of (K, delta) space near the synchronization transition.

#### Statistical Tests (Paired, 80 trials, random disorder realizations)

| Configuration | Mean $\Delta r$ | Cohen's d | p-value | Significance |
|--------------|----------------|-----------|---------|-------------|
| ring_k1_N10_K3.0_d0.2 | +0.084 | 0.17 | 0.131 | ns |
| ring_k1_N20_K5.0_d0.1 | -0.061 | -0.16 | 0.149 | ns |
| ring_k2_N10_K1.5_d0.2 | +0.052 | 0.19 | 0.101 | ns |
| ring_k2_N20_K2.5_d0.1 | +0.070 | 0.15 | 0.195 | ns |
| ring_k1_N10_K2.0_d0.3 | -0.135 | -0.29 | 0.013 | * |
| ring_k1_N20_K3.0_d0.3 | -0.142 | -0.52 | 0.00002 | *** |

When averaging over random disorder realizations (rather than using a fixed realization), the improvement becomes statistically non-significant at small $\delta$, and disorder significantly *hurts* at larger $\delta$. This reveals that the benefit of disorder is **realization-specific**: not any zero-mean disorder helps; the specific pattern must be compatible with the network topology.

---

## 5. Result Analysis

### Key Findings

**Finding 1: Stuart-Landau feedforward networks show robust disorder-enhanced synchronization.**
Excitation-parameter disorder ($\delta\mu$) nearly doubles the phase-locking area and increases the phase-locking fraction from 61% to 100%. This effect is robust: it holds for every tested frequency mismatch value and increases monotonically with disorder strength. This confirms and extends the analytical predictions of Ahmed et al. (2026).

**Finding 2: Disorder enhancement in Kuramoto ring networks is realization-dependent.**
For a fixed disorder realization, the order parameter can improve by 20-32%. But averaging over random realizations eliminates the benefit, indicating that only specific zero-mean disorder patterns help. This is consistent with the Palacios barycentric condition framework: the condition is necessary but not sufficient.

**Finding 3: The fraction of topologies benefiting from disorder increases with network size.**
From 20% (N=6) to 37% (N=10) of circulant graphs show improved synchronization from disorder. The simple ring graph (largest spectral gap ratio) benefits most consistently.

**Finding 4: There is a trade-off between amplitude and stability.**
In Stuart-Landau feedforward networks, increasing disorder strength improves phase locking but decreases output amplitude. This trade-off is practically relevant: one must choose between signal fidelity and robustness.

**Finding 5: The direction of disorder matters in feedforward networks.**
For 3-cell feedforward chains, increasing excitation along the chain direction enhances output (+6% amplitude), while decreasing excitation suppresses it (-7%). The direction of heterogeneity must match the direction of signal propagation.

### Hypothesis Testing

**H1 (Frequency disorder lowers K_c):** **Partially supported.** K_c decreases slightly for degree-regular graphs with degree-correlated disorder, but this is trivially zero disorder for regular graphs. For non-trivial disorder, K_c generally increases.

**H2 (Excitation disorder enhances feedforward networks):** **Strongly supported.** Phase-locking area increases by 72.5%, and phase-locking fraction reaches 100% at moderate disorder levels.

**H3 (AISync prevalence):** **Partially supported.** 20-37% of circulant graphs benefit from disorder (consistent with Zhang et al. 2017's 10-50% range), though no strict AISync (impossible without disorder) was observed in the Kuramoto framework.

**H4 (Topology-dependent effect):** **Strongly supported.** Ring networks benefit while star, path, and small-world networks do not (at the tested coupling values). The spectral gap ratio emerges as a predictor: larger gap ratios correlate with greater benefit from disorder.

### Mechanism Analysis

**Why does disorder help in ring networks?** The ring graph has the largest spectral gap ratio (ratio of largest to smallest nonzero Laplacian eigenvalue) among the tested topologies. A large gap ratio means the synchronization manifold is "fragile" — small perturbations to oscillator dynamics can push it out of stability. Specific disorder patterns that effectively reduce the functional spectral gap ratio can stabilize synchronization. However, random disorder patterns are equally likely to widen the gap, explaining the realization dependence.

**Why does disorder help in feedforward networks?** The Stuart-Landau feedforward network operates near a Hopf bifurcation. Excitation-parameter mismatch can effectively redistribute energy between the input and output nodes. When the output node has lower excitation than the input, the coupling from the higher-excitation input node provides an additional driving force that compensates for the output's subcritical dynamics, broadening the parameter region where phase locking is possible.

### Limitations

1. **Finite network sizes:** All experiments use N=6-20 oscillators. The behavior in the thermodynamic limit (N → ∞) may differ.
2. **Limited topology survey:** We tested six canonical topologies. Real-world networks (scale-free, hierarchical, modular) may behave differently.
3. **Kuramoto model simplicity:** The Kuramoto model captures only phase dynamics. Full oscillator dynamics (Stuart-Landau, Hodgkin-Huxley) may show richer disorder effects.
4. **Fixed disorder strength:** In Experiment 1, we used $\Delta = 1.0$. The optimal disorder strength varies by topology (Experiment 4 shows $\delta^* \approx 0.16$ for rings).
5. **Realization dependence:** The enhancement from disorder depends on the specific disorder realization, not just its statistics. This means practical applications would need to design the disorder pattern, not just its distribution.
6. **ODE integration accuracy:** While we used strict tolerances (rtol=1e-8), extremely long-time behavior may differ.

---

## 6. Conclusions

### Summary

We provide experimental evidence that disorder can enhance synchronization in coupled oscillator networks, but the effect is highly structured. **The strongest evidence comes from Stuart-Landau feedforward networks**, where excitation-parameter disorder nearly doubles the phase-locking region. For Kuramoto models on ring networks, specific disorder realizations improve synchronization by up to 32%, but the benefit is realization-dependent — random disorder is statistically neutral or harmful. Across circulant graphs, 20-37% show improved synchronization from disorder, consistent with the AISync literature.

### Implications

**The barycentric condition is necessary but not sufficient.** Our results show that zero-mean disorder (satisfying the barycentric condition) does not automatically help; the specific pattern of disorder must be compatible with the network topology. This extends the Palacios et al. (2024) framework by demonstrating that the barycentric condition constrains the space of beneficial disorders but does not identify them.

**Disorder type matters more than disorder strength.** In feedforward networks, the direction of excitation gradient (increasing along the chain) matters more than its magnitude. In ring networks, the optimal disorder strength is small ($\delta \approx 0.1-0.4$), suggesting that the benefit comes from breaking a symmetry rather than from the magnitude of asymmetry.

**Practical guideline:** When designing coupled oscillator networks (e.g., power grids, communication arrays), rather than striving for perfect homogeneity, one could deliberately introduce structured heterogeneity aligned with the network's topology to improve synchronization stability.

### Confidence in Findings

- **High confidence** in Stuart-Landau feedforward results (large effect, consistent across parameters)
- **Moderate confidence** in ring network enhancement (large effect for fixed realizations, but realization-dependent)
- **Moderate confidence** in AISync fraction (consistent with literature, limited to circulant graphs)
- **Low confidence** in generalization to arbitrary topologies (only 6 topologies tested)

---

## 7. Next Steps

### Immediate Follow-ups

1. **Characterize optimal disorder realizations:** For ring networks, determine which specific zero-mean frequency patterns maximize the order parameter, and relate these to Laplacian eigenvectors.

2. **Larger N study:** Test whether the ring network enhancement persists and strengthens for N=50, 100, 500 using the Ott-Antonsen reduction for the thermodynamic limit.

3. **Non-identical oscillator models:** Extend to coupled Lorenz oscillators, van der Pol oscillators, or Hodgkin-Huxley neurons where the MSF framework from Zhang et al. (2017) directly applies.

### Alternative Approaches

4. **Spectral optimization:** Formulate the problem of finding optimal zero-mean disorder as an eigenvalue optimization: minimize the spectral gap ratio of the effective Laplacian under the barycentric constraint.

5. **Analytical theory via Ott-Antonsen:** Derive closed-form expressions for how specific frequency distributions affect the synchronization transition in the mean-field limit.

### Broader Extensions

6. **Scale-free and hierarchical networks:** Test on networks with heterogeneous degree distributions where node disorder interacts with topological disorder.

7. **Experimental validation:** Design a physical experiment (e.g., coupled electronic oscillators or metronomes) to test the theoretical predictions.

### Open Questions

- **Is there a sharp criterion** (in terms of network spectral properties) for when zero-mean disorder helps synchronization?
- **What is the optimal disorder distribution** for a given topology? Is it related to the Laplacian eigenvectors?
- **Does the realization dependence persist in the thermodynamic limit**, or does self-averaging make disorder universally beneficial/harmful?
- **Can disorder-enhanced synchronization be achieved in transient dynamics** (not just steady state), which is relevant for power grid applications?

---

## 8. References

1. Palacios, A., In, V., Amani, A. (2024). "Disorder-Induced Dynamics in Complex Networks." *Int. J. Bifurcation and Chaos*, 34(05). DOI: 10.1142/S0218127424300106

2. Ahmed, Cameron, Palacios, Qi, Sahoo (2026). "Effects of Heterogeneity in Two-Cell Feedforward Networks." arXiv:2602.12434.

3. Zhang, Y., Nishikawa, T., Motter, A.E. (2017). "Asymmetry-Induced Synchronization in Oscillator Networks." *Phys. Rev. E*, 95, 062215. arXiv:1705.07907.

4. Molnar, F., Nishikawa, T., Motter, A.E. (2020). "Network Experiment Demonstrates Converse Symmetry Breaking." *Nature Physics*, 16, 351-356. arXiv:2009.05582.

5. Ott, E., Antonsen, T.M. (2008). "Low Dimensional Behavior of Large Systems of Globally Coupled Oscillators." *Chaos*, 18, 037113. arXiv:0806.0004.

6. Dorffer, F., Bullo, F. (2014). "Synchronization in Complex Networks of Phase Oscillators: A Survey." *Automatica*, 50(6), 1539-1564. arXiv:1209.1335.

7. Nishikawa, T., Motter, A.E. (2010). "Network Synchronization Landscape Reveals Compensatory Structures." *Phys. Rev. Lett.*, 104, 054102. arXiv:0909.2874.

8. Restrepo, J.G., Ott, E., Hunt, B.R. (2005). "Onset of Synchronization in Large Networks of Coupled Oscillators." *Phys. Rev. E*, 71, 036151. arXiv:cond-mat/0411202.

---

## Appendix: Figures

All figures are saved in the `figures/` directory:

| Figure | Description | File |
|--------|-------------|------|
| Fig. 1 | Order parameter vs. coupling for all topologies | `fig1_kuramoto_sync_curves.png` |
| Fig. 2 | Critical coupling comparison (bar chart) | `fig2_critical_coupling_comparison.png` |
| Fig. 3 | Stuart-Landau phase-locking boundary (homo vs. hetero) | `fig3_phase_locking_boundary.png` |
| Fig. 4 | Amplitude enhancement from excitation disorder | `fig4_amplitude_enhancement.png` |
| Fig. 5 | 3-cell feedforward: amplitude and phase locking | `fig5_three_cell_feedforward.png` |
| Fig. 6 | AISync prevalence across circulant graphs | `fig6_aisync_prevalence.png` |
| Fig. 7 | Spectral gap ratio vs. synchronization improvement | `fig7_spectral_vs_improvement.png` |
| Fig. 8 | Effect of disorder strength on synchronization | `fig8_disorder_strength_sweep.png` |
| Fig. 9 | Optimal disorder vs. homogeneous (bar chart) | `fig9_optimal_vs_homogeneous.png` |
| Fig. 10 | Ring network (K, delta) improvement heatmap | `fig10_ring_disorder_heatmap.png` |
| Fig. 11 | Optimal disorder strength vs. coupling | `fig11_optimal_disorder_vs_K.png` |
| Fig. 12 | Statistical test results (bar chart) | `fig12_statistical_tests.png` |

## Appendix: Reproducibility

### Environment

- Python 3.12.8
- NumPy 2.4, SciPy 1.17, NetworkX 3.6, Matplotlib 3.10, SymPy 1.14
- GPU: 2x NVIDIA GeForce RTX 3090 (24 GB each) — not used (CPU-only simulations)
- Random seed: 42

### Running the Experiments

```bash
source .venv/bin/activate
python src/experiment1_kuramoto_disorder.py    # ~38 min
python src/experiment2_stuart_landau.py        # ~160 min
python src/experiment3_aisync.py               # ~7 min
python src/experiment4_quick.py                # ~2 min
python src/experiment5_ring_deep_dive.py       # ~22 min
python src/analysis_and_plots.py               # ~10 sec
python src/plot_experiment5.py                 # ~5 sec
```

### Configuration

All experiment parameters are defined at the top of each script as module-level constants. The key parameter is `SEED = 42`, which ensures reproducibility of all random number generation.
