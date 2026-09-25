# anonlib

> [!NOTE]
> This repository has been anonymized for double-blind review. The library
> name, author names, affiliations, contact details and repository links have
> been removed or replaced. Identifying information will be restored after
> the review process.

**anonlib** is a Python library, powered by a Rust backend, for multi-objective
evolutionary community detection in complex networks. The evolutionary core is
written in Rust and exposed through [PyO3](https://pyo3.rs), giving it a large
speed advantage over pure-Python implementations while staying a drop-in for
the **NetworkX** / **igraph** ecosystem, making it well-suited to large-scale
graphs.

---

### Getting started

Build from source (requires a Rust toolchain and Python >= 3.10):

```bash
pip install maturin
maturin develop --release
```

```python
import networkx as nx
import anonlib

G = nx.karate_club_graph()          # any NetworkX / igraph graph, integer node ids
communities = anonlib.rimpso(G)     # -> dict[node, community]
```

> [!IMPORTANT]
> Graphs must be in **NetworkX** or **igraph** compatible format with integer
> node ids. Isolated nodes are assigned community `-1`.

Every detector returns a single crisp partition as `dict[node, community]`.

### Algorithms

`anonlib` exposes **nine community-detection algorithms** through **ten
detector entry points** (Shi-MOCD ships under two selection rules).

| API | Source | Objectives | Engine | Decision Making |
|---|---|---|---|---|
| `rimpso` | Anonymous, *under review* (2026) | Constant Potts split: cut fraction + pair coverage | memetic MOPSO over a resolution ladder | best-fit assortative block model |
| `hpmocd` | [Santos et al., *SNAM* 2025](https://doi.org/10.1007/s13278-025-01519-7) | decomposed modularity (intra, inter) | NSGA-II | max *Q* |
| `cdrme` | [Dabaghi-Zarandi et al., *JNCA* 2025](https://doi.org/10.1016/j.jnca.2024.104070) | Eq. 12 linkage scalar (single) | random walks + agglomerative merge | max *Q* |
| `mmcomo` | [Zhang et al., *IEEE CIM* 2023](https://ieeexplore.ieee.org/document/10188453) | kernel *k*-means + ratio cut | macro/micro co-evolutionary NSGA-II | max *Q* |
| `ccm` | [Shaik et al., *SN Comp. Sci.* 2021](https://doi.org/10.1007/s42979-020-00382-x) | community score + fitness + modularity | NSGA-III | max *Q* |
| `krm` | [Shaik et al., *SN Comp. Sci.* 2021](https://doi.org/10.1007/s42979-020-00382-x) | kernel *k*-means + ratio cut + modularity | NSGA-III | max *Q* |
| `gdpso` | [Cai et al., *Inf. Sciences* 2015](https://doi.org/10.1016/j.ins.2014.09.041) | Newman–Girvan modularity (single) | greedy discrete PSO | swarm best |
| `mocd_q` | [Shi et al., *Applied Soft Computing* 2012](https://doi.org/10.1016/j.asoc.2011.10.005) | decomposed modularity | PESA-II | max *Q* |
| `mocd_d` | [Shi et al., *Applied Soft Computing* 2012](https://doi.org/10.1016/j.asoc.2011.10.005) | decomposed modularity | PESA-II | max–min random-graph distance |
| `moga_net` | [Pizzuti, *IEEE TEC* 2012](https://doi.org/10.1109/TEVC.2011.2161090) | community score + fitness | NSGA-II | max *Q* |

Each detector has a module README with its full derivation, its parameter
table and the list of every deliberate divergence from its paper:
[`rimpso`](src/core/algorithms/rimpso/README.md) ·
[`hpmocd`](src/core/algorithms/hpmocd/README.md) ·
[`cdrme`](src/core/algorithms/cdrme/README.md) ·
[`mmcomo`](src/core/algorithms/mmcomo/README.md) ·
[`ccm`](src/core/algorithms/ccm/README.md) ·
[`krm`](src/core/algorithms/krm/README.md) ·
[`gdpso`](src/core/algorithms/gdpso/README.md) ·
[`mocd`](src/core/algorithms/mocd/README.md) (Shi-MOCD) ·
[`moganet`](src/core/algorithms/moganet/README.md) —
[index](src/core/algorithms/README.md).

### Usage

```python
import anonlib

# Proposed detector
part = anonlib.rimpso(G)          # RIMPSO         (recommended default)

# Baselines
part = anonlib.hpmocd(G)          # HP-MOCD   (Santos et al.)
part = anonlib.cdrme(G)           # CDRME     (Dabaghi-Zarandi et al.)
part = anonlib.mmcomo(G)          # MMCoMO    (Zhang et al.)
part = anonlib.ccm(G)             # CCM       (Shaik et al., NSGA-III)
part = anonlib.krm(G)             # KRM       (Shaik et al., NSGA-III)
part = anonlib.gdpso(G)           # GDPSO     (Cai et al., particle swarm)
part = anonlib.mocd_q(G)          # Shi-MOCD, max-modularity selection
part = anonlib.mocd_d(G)          # Shi-MOCD, max-min-distance selection
part = anonlib.moga_net(G)        # MOGA-Net  (Pizzuti)

# All return dict[node, community]; isolated nodes -> -1
```

Every detector except `hpmocd` takes its budget as keyword arguments. The
values below are the shipped defaults, which follow each paper wherever the
paper states them:

```python
anonlib.rimpso(G, pop_size=100, num_gens=100, inertia=0.4, cognitive=0.7, social=0.7,
               local_rate=0.35, archive=100, ls_period=10, seed=0)
anonlib.mmcomo(G, pop_size=100, num_gens=50, cross_rate=0.1, mut_rate=0.1, gap=10, beta=0.05)
anonlib.ccm(G,    pop_size=200, num_gens=100, cross_rate=0.8, mut_rate=1/68, r=1.0, alpha=1.0, divisions=12)
anonlib.krm(G,    pop_size=100, num_gens=100, cross_rate=0.8, mut_rate=1/34, divisions=12)
anonlib.moga_net(G, pop_size=300, num_gens=30, cross_rate=0.8, mut_rate=0.2, r=2.0, alpha=1.0)
anonlib.gdpso(G,  pop_size=100, num_gens=250, w=0.7298, c1=1.4961, c2=1.4961,
              mut_rate=0.1, mut_frac=0.1, lpa_sweeps=5)
anonlib.cdrme(G,  alpha_walk=1.0, n_walk=50, pop_size=300, elite_size=300,
              alpha_mut=0.5, mut_sweeps=10)
anonlib.mocd_q(G, pop_size=100, num_gens=100, cross_rate=0.9, mut_rate=0.1)
anonlib.mocd_d(G, pop_size=100, num_gens=100, cross_rate=0.9, mut_rate=0.1, rand_networks=3)
```

The one exception is Shi-MOCD: `mocd_q` and `mocd_d` default to the
HP-MOCD-parity benchmark budget, **not** Shi's published configuration, which
is `cross_rate=0.6`, `mut_rate=0.4` with per-graph population and generation
counts from the paper's Table 1. Pass those explicitly to reproduce the paper.

`hpmocd(G)` takes the graph only and runs at its published configuration; for
a tunable HP-MOCD, or to plug in your own Python objective functions, use the
`anonlib.HpMocd` class instead.

#### Pareto fronts

Seven of the eleven entry points expose the candidate set their selection
rule picks from:

```python
fronts = anonlib.rimpso_fronts(G)   # list[dict[node, community]]
fronts = anonlib.hpmocd_fronts(G)
fronts = anonlib.mmcomo_fronts(G)
fronts = anonlib.ccm_fronts(G)
fronts = anonlib.krm_fronts(G)
fronts = anonlib.moga_net_fronts(G)

# RIMPSO only: run its label-free selection rule over partitions produced
# elsewhere, which separates the search's contribution from the selector's
pick, points = anonlib.rimpso_select(G, candidates)
```

Those are *exactly* the detectors with a front accessor. `gdpso` and `cdrme`
are single-objective, and `mocd_q` / `mocd_d` do not expose theirs, so there is
no `gdpso_fronts`, `cdrme_fronts` or `mocd_fronts`.

### Helpers

```python
anonlib.max_cores(8)                 # set Rayon thread pool (first call wins)

# Fast native ground-truth agreement metrics between two {node: community}
# dicts, computed over their shared nodes
nmi, ami, ari, f1 = anonlib.gt_metrics(partition, gt)
anonlib.nmi(partition, gt)           # or each metric individually
anonlib.ami(partition, gt)
anonlib.ari(partition, gt)
anonlib.f1(partition, gt)            # pairwise F1
```

### License

This project is licensed under **GPL-3.0 or later**.

---

### Citation

Citation information is withheld during double-blind review.
