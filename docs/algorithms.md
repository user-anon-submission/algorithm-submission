# Algorithms

`anonlib` exposes **nine community-detection algorithms** through **ten
detector entry points** — Shi-MOCD ships under two selection rules, `mocd_q`
and `mocd_d`.

**RIMPSO** is the proposed algorithm. *Every other detector is an
implementation of a published method*, written from its paper in this
repository.

## Overview

| API | Algorithm | Objectives & engine | Selection rule |
|---|---|---|---|
| [`rimpso`](api/detectors.md#anonlib.rimpso) | **RIMPSO** — Anonymous, *under review* (2026) | exact Constant Potts split into cut fraction + pair coverage — the front *is* the resolution profile; memetic particle swarm niched along a geometric resolution ladder, with decomposition-based archive truncation | best-fitting degree-corrected assortative block model, Schwarz-penalised (front via [`rimpso_fronts`](api/fronts.md#anonlib.rimpso_fronts)) |
| [`hpmocd`](api/detectors.md#anonlib.hpmocd) | **HP-MOCD** — [Santos et al., *SNAM* 2025](https://doi.org/10.1007/s13278-025-01519-7) | decomposed modularity (intra, inter), parallel NSGA-II | max modularity *Q* (front via [`hpmocd_fronts`](api/fronts.md#anonlib.hpmocd_fronts)) |
| [`cdrme`](api/detectors.md#anonlib.cdrme) | **CDRME** — [Dabaghi-Zarandi et al., *JNCA* 2025](https://doi.org/10.1016/j.jnca.2024.104070) | softmax-weighted random walks build a primary community set; stochastic agglomerative merge chains optimise the paper's Eq. (12) linkage scalar — a single objective, so there is no front | max modularity *Q* |
| [`mmcomo`](api/detectors.md#anonlib.mmcomo) | **MMCoMO** — [Zhang et al., *IEEE CIM* 2023](https://ieeexplore.ieee.org/document/10188453) | kernel *k*-means + ratio cut, macro/micro co-evolutionary NSGA-II over a dense diffusion kernel | max *Q* (front via [`mmcomo_fronts`](api/fronts.md#anonlib.mmcomo_fronts)) |
| [`ccm`](api/detectors.md#anonlib.ccm) | **CCM** — [Shaik et al., *SN Computer Science* 2021](https://doi.org/10.1007/s42979-020-00382-x) | community score + community fitness + modularity, NSGA-III | max *Q* (front via [`ccm_fronts`](api/fronts.md#anonlib.ccm_fronts)) |
| [`krm`](api/detectors.md#anonlib.krm) | **KRM** — [Shaik et al., *SN Computer Science* 2021](https://doi.org/10.1007/s42979-020-00382-x) | kernel *k*-means + ratio cut + modularity, NSGA-III | max *Q* (front via [`krm_fronts`](api/fronts.md#anonlib.krm_fronts)) |
| [`gdpso`](api/detectors.md#anonlib.gdpso) | **GDPSO** — [Cai et al., *Information Sciences* 2015](https://doi.org/10.1016/j.ins.2014.09.041) | Newman–Girvan modularity — a single objective, so there is no front — maximised by a greedy discrete particle swarm | best position the swarm ever held |
| [`mocd_q`](api/detectors.md#anonlib.mocd_q) | **Shi-MOCD** — [Shi et al., *Applied Soft Computing* 2012](https://doi.org/10.1016/j.asoc.2011.10.005) | decomposed modularity, PESA-II | max *Q* (Shi Eq. 3.8) |
| [`mocd_d`](api/detectors.md#anonlib.mocd_d) | **Shi-MOCD** — [Shi et al., *Applied Soft Computing* 2012](https://doi.org/10.1016/j.asoc.2011.10.005) | decomposed modularity, PESA-II | max–min distance to Erdős–Rényi control fronts (Shi Eqs. 3.9–3.11) |
| [`moga_net`](api/detectors.md#anonlib.moga_net) | **MOGA-Net** — [Pizzuti, *IEEE TEC* 2012](https://doi.org/10.1109/TEVC.2011.2161090) | community score + community fitness, NSGA-II | max *Q*, Pizzuti Sec. V-E (front via [`moga_net_fronts`](api/fronts.md#anonlib.moga_net_fronts)) |

All detectors return a single crisp partition as `dict[node, community]`;
isolated nodes are assigned community `-1`.

Each one has a module README carrying its full derivation, its parameter table
and every deliberate divergence from its paper:
[`rimpso`](../src/core/algorithms/rimpso/README.md) ·
[`hpmocd`](../src/core/algorithms/hpmocd/README.md) ·
[`cdrme`](../src/core/algorithms/cdrme/README.md) ·
[`mmcomo`](../src/core/algorithms/mmcomo/README.md) ·
[`ccm`](../src/core/algorithms/ccm/README.md) ·
[`krm`](../src/core/algorithms/krm/README.md) ·
[`gdpso`](../src/core/algorithms/gdpso/README.md) ·
[`mocd`](../src/core/algorithms/mocd/README.md) (Shi-MOCD) ·
[`moganet`](../src/core/algorithms/moganet/README.md) ·
[index](../src/core/algorithms/README.md).

## Which one should I use?

- **[`rimpso`](api/detectors.md#anonlib.rimpso)** — the recommended default:
  one run covers every resolution, and the partition is chosen for you with no
  ground truth and no resolution parameter to set. The whole profile is
  available from [`rimpso_fronts`](api/fronts.md#anonlib.rimpso_fronts).
- **[`hpmocd`](api/detectors.md#anonlib.hpmocd)** — the published HP-MOCD
  behaviour with max-modularity selection.
- **The other seven** — re-implemented baselines, for papers and benchmarks.
  Each takes its budget as keyword arguments at the defaults its own paper
  states; see the [detector API reference](api/detectors.md) for every
  signature.

## RIMPSO

RIMPSO (Resolution-Indexed Memetic Particle Swarm Optimisation) minimises the
exact affine decomposition of the Constant Potts Model into two conflicting
objectives:

```text
cut(C)  = 1 - sum_c |E(c)| / m        fraction of edges leaving their community
pair(C) = sum_c C(n_c, 2) / C(n, 2)   fraction of node pairs put together
```

with `n` every node of the graph. Isolated nodes never move and are returned
as community `-1`; each is its own singleton, so they add nothing to `pair`'s
numerator while still counting in its denominator.

One giant community gives `cut = 0, pair = 1`; all singletons give
`cut = 1, pair = 0`. Because `H_g(C)/m = 1 - cut(C) - (g/g_d)*pair(C)`, with
`g_d = 2m/(n(n-1))` the edge density over those same `n` nodes,
minimising any positive weighting `a*cut + b*pair` is exactly maximising CPM
at resolution `g = g_d*b/a`. The resolution is therefore not a search
parameter but the exchange rate between the two objectives, and the Pareto
front *is* the resolution profile — a single run sweeps the whole ladder.

**The search.** A particle swarm populates that front, each particle pinned to
its own resolution on a geometric ladder over `[1/n^2, 1]` — the whole range
where `gamma` can still change the answer. Per node, velocity is the
probability that the node is unstable: an unstable node adopts an attractor's
label, a stable one gets a resolution-directed local move. Every tenth
iteration the particle is repaired back to a CPM local optimum and a
community-merge sweep runs, which is what makes the flight an optimiser rather
than a drift — the repair sharpens, the merge coarsens, and no run of
single-node moves can do the latter.

**The archive.** The external Pareto archive is truncated by keeping the best
member at each rung of the ladder rather than the least crowded. Crowding
distance is a diversity criterion with no notion of quality, and was measured
evicting the archive's best member while nothing dominated it.

**The selection.** One partition is returned with no ground truth, no target
community count and no parameter: the member that a **degree-corrected
assortative block model** fits best once its own free densities are paid for.
Giving each community its own internal edge density and everything between
communities one shared density, and profiling those densities out, leaves a
log-likelihood ratio against the configuration model that is two bincounts,
`L(C) = sum_c e_c ln(e_c/E_c) + e_out ln(e_out/E_out)` with `E_c = d_c^2/4m`;
each community brings a free density, so they are charged
`(B+1)/2 * ln(2m)`. Neither degenerate partition needs a special case: one
community explains nothing the degrees do not, so `L = 0` and it pays `ln(2m)`
anyway, while all-singletons puts no edge inside a community and is rejected as
disassortative. There is no degeneracy filter and no fallback stage.

[`rimpso`](api/detectors.md#anonlib.rimpso) returns the selected member,
[`rimpso_fronts`](api/fronts.md#anonlib.rimpso_fronts) returns every member
with its `(cut, pair)` point and the selected index, and
[`rimpso_select`](api/fronts.md#anonlib.rimpso_select) runs the selection
rule alone over partitions produced elsewhere. RIMPSO is **deterministic** —
byte-identical output at any thread count.

## HP-MOCD

HP-MOCD optimises decomposed modularity with a parallel NSGA-II and returns
the max-*Q* solution from the Pareto front. The front itself is exposed for
inspection via [`hpmocd_fronts`](api/fronts.md#anonlib.hpmocd_fronts).
Published in
[Social Network Analysis and Mining (2025)](https://doi.org/10.1007/s13278-025-01519-7).

[`hpmocd`](api/detectors.md#anonlib.hpmocd) and
[`hpmocd_fronts`](api/fronts.md#anonlib.hpmocd_fronts) take the graph and
nothing else: they run at the published configuration (`pop_size=100`,
`num_gens=100`, `cross_rate=0.7`, `mut_rate=0.5`). For a tunable HP-MOCD, or
to supply your own Python objective functions, use the `anonlib.HpMocd` class.

## The re-implemented baselines

The seven detectors below are other people's algorithms, ported from their
papers so that benchmarks in this repository compare against a faithful
implementation rather than a paraphrase. Each module README lists what was
read, what the paper leaves open, and every place this port deliberately
diverges from it.

**Original code released by the authors — three of the seven.**

- **MOGA-Net** ([Moganet2016.zip](https://staff.icar.cnr.it/pizzuti/codice/Moganet2016.zip))
  is MATLAB, shipped as obfuscated P-code: the search loop cannot be read, but
  its result files can, and they were used to settle the objectives.
- **GDPSO** ([doctor-cai/GDPSO](https://github.com/doctor-cai/GDPSO)) is C++
  with no licence file, so this port was written clean-room from a description
  of it; no reference source was copied.
- **CDRME**'s reference is a private Python notebook supplied by the authors,
  vendored in this repository at `res/original_algs/cdrme` as plain Python.
  It is **not published at any public URL**, so none is cited here. It was
  consulted only to disambiguate what the paper leaves open, and four of its
  choices were deliberately not reproduced.

**No original code exists** for MMCoMO, CCM, KRM or Shi-MOCD. The authors'
sites and GitHub were searched; only the papers' text and tables constrain
those four ports.

Two of the seven are single-objective and therefore have no Pareto front and
no `*_fronts` accessor: `gdpso` maximises Newman–Girvan modularity directly,
and `cdrme` maximises the sum its paper's Eq. (12) forms out of inner and
outer linkage. `mocd_q` and `mocd_d` are multi-objective but expose no front
accessor either; the two names are the same PESA-II search under Shi's two
published model-selection rules.

!!! warning "Shi-MOCD defaults are not Shi's"
    [`mocd_q`](api/detectors.md#anonlib.mocd_q) and
    [`mocd_d`](api/detectors.md#anonlib.mocd_d) default to this repository's
    HP-MOCD-parity benchmark budget (`cross_rate=0.9`, `mut_rate=0.1`), not to
    the paper's `pc=0.6`, `pm=0.4` with per-graph population and generation
    counts from its Table 1. Pass those explicitly to reproduce the paper.


## Citation

Citation information is withheld during double-blind review.
