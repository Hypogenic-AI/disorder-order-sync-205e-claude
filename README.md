# When Disorder Creates Order: Unexpected Synchronization in Heterogeneous Networks

Systematic numerical investigation of how deliberately introducing zero-mean parameter disorder into coupled oscillator networks can improve synchronization, subject to the barycentric condition (Palacios, In, Amani, 2024).

## Key Results

- **Stuart-Landau feedforward networks:** Excitation-parameter disorder nearly doubles the phase-locking region (35.6% -> 61.4% of parameter space), with phase-locking fraction increasing monotonically from 61% to 100%
- **Kuramoto ring networks:** Fixed disorder realizations improve the order parameter by up to 32% near the synchronization transition, but the effect is realization-dependent
- **Circulant graph survey:** 20-37% of circulant graphs show improved synchronization from disorder, with simple rings benefiting most
- **Trade-off discovered:** In feedforward networks, disorder improves stability (phase locking) at the cost of reduced signal amplitude

## Project Structure

```
.
├── REPORT.md              # Full research report with results and analysis
├── README.md              # This file
├── planning.md            # Research plan and methodology
├── src/                   # Experiment and analysis code
│   ├── kuramoto.py        # Kuramoto model simulation
│   ├── stuart_landau.py   # Stuart-Landau oscillator model
│   ├── networks.py        # Network topology generation
│   ├── experiment1_kuramoto_disorder.py   # Exp 1: Kuramoto across topologies
│   ├── experiment2_stuart_landau.py       # Exp 2: Feedforward networks
│   ├── experiment3_aisync.py              # Exp 3: AISync verification
│   ├── experiment4_quick.py               # Exp 4: Optimal disorder strength
│   ├── experiment5_ring_deep_dive.py      # Exp 5: Ring network deep dive
│   ├── analysis_and_plots.py             # Statistical analysis & figures
│   └── plot_experiment5.py               # Additional ring network plots
├── results/               # JSON result files
├── figures/               # Generated figures (12 plots)
├── papers/                # Reference papers (PDFs)
├── literature_review.md   # Literature review
└── resources.md           # Resource catalog
```

## Reproducing Results

```bash
# Activate environment
source .venv/bin/activate

# Run experiments (order doesn't matter, ~3.5 hours total)
python src/experiment1_kuramoto_disorder.py
python src/experiment2_stuart_landau.py
python src/experiment3_aisync.py
python src/experiment4_quick.py
python src/experiment5_ring_deep_dive.py

# Generate figures and statistics
python src/analysis_and_plots.py
python src/plot_experiment5.py
```

## Dependencies

Python 3.10+, NumPy, SciPy, NetworkX, Matplotlib, SymPy. Install with:
```bash
uv venv && source .venv/bin/activate && uv add numpy scipy networkx matplotlib sympy
```

See [REPORT.md](REPORT.md) for full details.
