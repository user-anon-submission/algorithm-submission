# Detectors

Every detector takes a graph and returns a partition as `dict[node, community]`. Isolated nodes are assigned community `-1`.

`rimpso` is the proposed algorithm. The other nine entry points implement published methods; see [Algorithms](../algorithms.md) for the paper and the selection rule behind each.

## Proposed algorithm

::: anonlib.rimpso

## Baselines

::: anonlib.hpmocd

!!! note "Tunable HP-MOCD"
    `hpmocd` takes the graph and nothing else: it runs at the published configuration (`pop_size=100`, `num_gens=100`, `cross_rate=0.7`, `mut_rate=0.5`). The `anonlib.HpMocd` class exposes the same search with those four as constructor arguments, plus `set_objectives` for plugging in your own Python objective functions and `set_on_generation` for a per-generation callback.

::: anonlib.cdrme

::: anonlib.mmcomo

::: anonlib.ccm

::: anonlib.krm

::: anonlib.gdpso

::: anonlib.mocd_q

::: anonlib.mocd_d

::: anonlib.moga_net

