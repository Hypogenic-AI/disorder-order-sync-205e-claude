# Research Plan: When Disorder Creates Order

## Motivation & Novelty Assessment

### Why This Research Matters
Classical synchronization theory (Kuramoto, Pecora-Carroll) generally treats parameter heterogeneity as an obstacle to synchronization: the more diverse the oscillator frequencies, the stronger the coupling needed to synchronize. Yet recent theoretical work (Zhang et al. 2017, Molnar et al. 2020) and normal-form analysis (Palacios et al. 2024, Ahmed et al. 2026) show that disorder can *help*. Understanding when and why is critical for engineering applications (power grids, communication networks) and biological systems (neural circuits, circadian rhythms) where perfect homogeneity is impossible.

### Gap in Existing Work
Based on the literature review, three key gaps exist:
1. The Palacios group's barycentric condition has not been systematically tested across network topologies with numerical experiments.
2. No systematic computational study exists comparing synchronization regions for homogeneous vs. heterogeneous (barycentric-constrained) parameter distributions across multiple canonical network topologies.
3. The connection between AISync/CSB (Motter group, general oscillators) and normal-form disorder effects (Palacios group, specific bifurcations) has not been bridged experimentally.

### Our Novel Contribution
We conduct systematic numerical experiments testing whether disorder—subject to the barycentric condition—broadens synchronization regions across multiple network topologies and coupling schemes. We:
1. Implement Kuramoto and Stuart-Landau oscillator models on various network topologies.
2. Systematically compare homogeneous vs. zero-mean heterogeneous parameter distributions.
3. Quantify the synchronization region (critical coupling, order parameter) for each configuration.
4. Identify specific topology-disorder combinations where disorder provably enhances synchronization.
5. Provide a mathematical characterization (via Laplacian spectral analysis) of when enhancement occurs.

### Experiment Justification
- **Experiment 1 (Kuramoto on ring/star/complete/circulant graphs):** Tests the hypothesis across canonical topologies where Laplacian spectra are analytically known. Directly tests whether frequency heterogeneity with zero mean can lower the critical coupling.
- **Experiment 2 (Stuart-Landau feedforward networks):** Replicates and extends Ahmed et al. (2026) results, testing excitation-parameter disorder on phase-locking regions.
- **Experiment 3 (AISync numerical verification):** Tests the Zhang et al. (2017) multilayer construction to verify that parameter asymmetry enables synchronization that homogeneity cannot.
- **Experiment 4 (Optimal disorder distributions):** For topologies where disorder helps, searches for the optimal zero-mean distribution maximizing synchronization.

---

## Research Question
Does deliberately introducing zero-mean parameter heterogeneity (disorder) into coupled oscillator networks broaden or stabilize synchronization regions, and if so, for which network topologies and parameter distributions?

## Hypothesis Decomposition

### H1: Frequency disorder can lower critical coupling in Kuramoto networks
For certain network topologies, a zero-mean frequency distribution with nonzero variance yields a lower effective critical coupling than the homogeneous case (all frequencies equal).

### H2: Excitation-parameter disorder enhances amplification in feedforward networks
In Stuart-Landau feedforward networks, inhomogeneity in the excitation parameter μ with zero mean expands the phase-locking region compared to the homogeneous case.

### H3: AISync exists for a significant fraction of symmetric network topologies
Following Zhang et al. (2017), parameter heterogeneity is *required* for stable synchronization in a measurable fraction of symmetric networks.

### H4: The benefit of disorder depends on network topology
The degree to which disorder helps (or hurts) synchronization varies systematically with topological properties (algebraic connectivity, spectral gap, symmetry group).

## Proposed Methodology

### Approach
We use numerical simulation of coupled oscillator systems (Kuramoto and Stuart-Landau models) on various network topologies, comparing synchronization metrics between homogeneous and heterogeneous configurations. All heterogeneous configurations satisfy the barycentric condition (zero-mean disorder).

### Experimental Steps

1. **Implement Kuramoto model simulation** on configurable network topologies with:
   - Adjustable natural frequencies ω_i (with barycentric constraint Σω_i = 0)
   - Adjustable coupling strength K
   - Order parameter r computation
   - Multiple network topologies via NetworkX

2. **Implement Stuart-Landau oscillator simulation** for feedforward networks:
   - Complex-valued dynamics with adjustable μ_i and ω_i
   - Phase-locking detection
   - Amplitude growth measurement

3. **Sweep experiments:**
   - For each topology: sweep coupling K, measure r(K) for homogeneous vs. heterogeneous
   - For feedforward: sweep (σ̃, μ̃) parameter space, map phase-locking boundaries
   - Multiple random seeds for statistical robustness

4. **AISync verification:**
   - Enumerate small symmetric networks
   - Test MSF condition for homogeneous vs. heterogeneous parameter assignments
   - Count fraction supporting AISync

5. **Optimal disorder search:**
   - For topologies where disorder helps, optimize the zero-mean distribution
   - Use scipy.optimize to find distribution maximizing order parameter

### Baselines
- **Homogeneous case:** All oscillators identical (ω_i = 0 for all i)
- **Random heterogeneity:** ω_i drawn uniformly/normally, centered at 0
- **Structured heterogeneity:** Specific distributions designed to match topology

### Evaluation Metrics
- **Order parameter r:** Primary measure of synchronization (0 = incoherent, 1 = fully synchronized)
- **Critical coupling K_c:** Coupling strength at which r transitions from ~0 to >0
- **Phase-locking region area:** For feedforward networks, area of (σ̃, μ̃) space with stable equilibria
- **Synchronization time:** Time to reach r > 0.9 from random initial conditions

### Statistical Analysis Plan
- 50 independent trials per configuration (different random initial conditions)
- Report mean ± std of order parameter
- Two-sample t-tests comparing homogeneous vs. heterogeneous order parameters
- Significance level α = 0.01 with Bonferroni correction for multiple comparisons
- Effect sizes via Cohen's d

## Expected Outcomes
- H1 supported: For star and certain circulant graphs, zero-mean frequency disorder lowers K_c
- H2 supported: Feedforward networks show expanded phase-locking with μ-disorder
- H3 supported: ~10-50% of small symmetric networks exhibit AISync (matching Zhang et al.)
- H4 supported: Ring graphs show little benefit; star/hub graphs show significant benefit

## Timeline and Milestones
- Phase 0-1: Planning (this document) — 30 min
- Phase 2: Implementation — 60 min
- Phase 3: Run experiments — 60 min
- Phase 4: Analysis — 30 min
- Phase 5: Validation — 20 min
- Phase 6: Documentation — 30 min

## Potential Challenges
1. Numerical stiffness in Stuart-Landau integration → use adaptive RK45
2. Large parameter sweeps → parallelize, use coarse-then-fine grid
3. Phase-locking detection → use convergence criterion on |ω_i(t) - ω_j(t)|
4. False positives in synchronization detection → long integration times, multiple trials

## Success Criteria
1. At least one topology-disorder pair where heterogeneous r > homogeneous r with p < 0.01
2. Quantitative agreement with Ahmed et al. (2026) feedforward results
3. AISync fraction consistent with Zhang et al. (2017) predictions
4. Clear visualization showing disorder-enhanced synchronization regions
