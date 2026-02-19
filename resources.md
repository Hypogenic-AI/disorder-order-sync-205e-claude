# Resources Catalog

## Summary
This document catalogs all resources gathered for the mathematics research project "When Disorder Creates Order: Unexpected Synchronization in Heterogeneous Networks."

## Papers
Total papers downloaded: 14
Total key paywalled papers identified: 6

| # | Title | Authors | Year | File | Key Results |
|---|-------|---------|------|------|-------------|
| 1 | Effects of Heterogeneity in Two-Cell Feedforward Networks | Ahmed, Cameron, Palacios et al. | 2026 | papers/2602.12434_palacios_heterogeneity_feedforward.pdf | Excitation inhomogeneity enhances amplification; phase locking persists broadly |
| 2 | Trade-Off in Multilayer Networks | Singh, Rai, Palacios et al. | 2025 | papers/2511.19047_palacios_multilayer.pdf | Multilayer connectivity trade-offs |
| 3 | Dn Symmetric Hamiltonian Gyroscopes | Buono, Chan, Palacios, In | 2013 | papers/1309.3196_buono_palacios_gyroscopes.pdf | Dihedral symmetry, normal forms, bifurcation |
| 4 | Asymmetry-Induced Synchronization | Zhang, Nishikawa, Motter | 2017 | papers/1705.07907_zhang_asymmetry_sync.pdf | AISync definition, multilayer construction, prevalence |
| 5 | Converse Symmetry Breaking (Experiment) | Molnar, Nishikawa, Motter | 2020 | papers/2009.05582_motter_converse_symm_breaking.pdf | First experimental CSB demonstration |
| 6 | Asymmetry Underlies Stability in Power Grids | Molnar, Nishikawa, Motter | 2021 | papers/2103.10952_molnar_asymmetry_power.pdf | CSB in power grid models |
| 7 | Synchronization Landscape / Compensatory Structures | Nishikawa, Motter | 2010 | papers/0909.2874_nishikawa_motter_landscape.pdf | Optimal synchronization via mixed interactions |
| 8 | Synchronization is Optimal in Nondiag. Networks | Nishikawa, Motter | 2006 | papers/cond-mat_0605619_nishikawa_optimal.pdf | Optimal synchronizability requires asymmetry |
| 9 | Low Dimensional Behavior (Ott-Antonsen) | Ott, Antonsen | 2008 | papers/0806.0004_ott_antonsen.pdf | Dimensional reduction for globally coupled oscillators |
| 10 | Synchronization Survey (Dörfler-Bullo) | Dörfler, Bullo | 2014 | papers/1209.1335_dorfler_bullo_sync.pdf | Comprehensive Kuramoto synchronization conditions |
| 11 | Onset of Synchronization | Restrepo, Ott, Hunt | 2005 | papers/cond-mat_0411202_restrepo_onset.pdf | Critical coupling from adjacency eigenvalues |
| 12 | Partially Integrable Hierarchical Oscillators | Pikovsky, Rosenblum | 2008 | papers/0811.3925_pikovsky_rosenblum.pdf | Watanabe-Strogatz ansatz for subpopulations |
| 13 | Synchronization Phase Transition (Bronski-DeVille) | Bronski, DeVille | 2016 | papers/1609.05765_bronski_deville.pdf | Phase-locked state analysis |
| 14 | Disorder-Induced Order in Opinion Dynamics | Vendeville et al. | 2020 | papers/2002.09366_disorder_order_opinion.pdf | Disorder-induced order analogy |

See `papers/README.md` for detailed descriptions.

## Prior Results Catalog

Key theorems and lemmas available for our proofs:

| Result | Source | Statement Summary | Used For |
|--------|--------|-------------------|----------|
| Kuramoto phase transition | Kuramoto (1975) | Critical coupling $K_c = 2/(\pi g(0))$ for global coupling | Baseline synchronization onset |
| Ott-Antonsen reduction | Ott, Antonsen (2008) | Infinite-population dynamics reduces to ODE for order parameter | Analytical study of heterogeneous populations |
| Master Stability Function | Pecora, Carroll (1998) | Synchronization stability via $\psi(\lambda_j)$ | Stability analysis on networks |
| AISync prevalence | Zhang et al. (2017) | 10-50% of symmetric networks support AISync | Existence of disorder-enhanced sync |
| Proposition 1 (feedforward) | Ahmed et al. (2026) | Phase-locking region bounded by explicit elliptic/parametric curves | Feedforward network analysis |
| Barycentric condition | Palacios et al. (2024) | Heterogeneity must be zero-mean relative to bifurcation point | Proper measurement of disorder effects |
| CSB experimental validation | Molnar et al. (2020) | Non-identical oscillators synchronize better experimentally | Physical evidence for hypothesis |
| Compensatory structures | Nishikawa, Motter (2010) | Mixed interactions can optimize synchronizability | Network design principles |
| Synchronization conditions | Dörfler, Bullo (2014) | Coupling strength vs. frequency spread bounds | Reference synchronization criteria |

## Computational Tools

| Tool | Purpose | Location | Notes |
|------|---------|----------|-------|
| SymPy 1.14 | Symbolic computation | pip package (installed) | For normal form computations, algebraic manipulation |
| NetworkX 3.6 | Graph theory | pip package (installed) | For Laplacian eigenvalue computation, graph enumeration |
| NumPy 2.4 | Numerical arrays | pip package (installed) | For numerical experiments |
| SciPy 1.17 | Scientific computing | pip package (installed) | For ODE integration, eigenvalue computation, optimization |
| Matplotlib 3.10 | Visualization | pip package (installed) | For bifurcation diagrams, phase portraits |

All tools installed in `.venv/` virtual environment.

## Resource Gathering Notes

### Search Strategy
1. Used paper-finder service with 10 different search queries covering: disorder-induced synchronization, Kuramoto model heterogeneity, parameter symmetry breaking, equivariant bifurcation theory, heterogeneity-promotes-synchronization, and specific author searches (Palacios, Motter).
2. Used arXiv API for targeted author searches (Palacios) and topic searches.
3. Used Semantic Scholar API for paper metadata and reference extraction.
4. Total papers evaluated: ~1000+ from paper-finder, narrowed to 14 downloaded PDFs.

### Selection Criteria
- **Priority 1:** Papers by Palacios group (directly addresses barycentric condition and disorder in networks).
- **Priority 2:** Papers by Motter group (AISync/CSB framework, experimental validation).
- **Priority 3:** Foundational mathematical results (Ott-Antonsen, MSF, Kuramoto theory).
- **Priority 4:** Papers demonstrating or analyzing disorder-order phenomena in specific systems.

### Challenges Encountered
1. The central reference (Palacios, In, Amani 2024) is paywalled (Int. J. Bifurcation and Chaos). The abstract from Semantic Scholar provides the key ideas, and the 2026 arXiv paper by the same group extends the work.
2. Several classic papers (Braiman et al. 1995, Pecora-Carroll 1998, Strogatz 2000, Acebron et al. 2005) are not available on arXiv and are in paywalled journals.
3. The Palacios group's arXiv presence is limited (only 3 papers found), suggesting most of their work is in journals.

## Recommendations for Proof Construction

Based on gathered resources, we recommend:

1. **Proof strategy:** The most promising approach combines:
   - **Normal form analysis** (Palacios style) to study bifurcation structure with heterogeneity parameters.
   - **Laplacian spectral analysis** (Motter style) to connect heterogeneity to synchronization stability.
   - The key insight is that the barycentric condition constrains the admissible heterogeneity to zero-mean perturbations around the bifurcation point, and within this constraint, certain topologies admit eigenvalue configurations that improve stability.

2. **Key prerequisites:**
   - The MSF framework (Pecora-Carroll) for stability analysis.
   - The Ott-Antonsen reduction for mean-field analysis of infinite populations.
   - Normal form theory near Hopf/pitchfork bifurcations.
   - The barycentric condition from Palacios et al. (2024).

3. **Computational tools:**
   - SymPy for symbolic normal-form computations and equilibrium analysis.
   - NetworkX for enumerating symmetric graphs and computing Laplacian spectra.
   - SciPy for numerical ODE integration to verify analytical predictions.
   - NumPy/Matplotlib for bifurcation diagram generation.

4. **Potential difficulties:**
   - Bridging the gap between the Palacios approach (specific normal forms, feedforward topology) and the Motter approach (general oscillators, symmetric networks) requires careful formulation.
   - The barycentric condition is derived in the context of parameter symmetry breaking near bifurcation; extending it to global synchronization analysis requires justification.
   - Explicit computation of synchronization region boundaries for general topologies is likely intractable; focus on specific tractable classes (circulant graphs, feedforward, ring, star).
