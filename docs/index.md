---
hide:
  - navigation
  - toc
---

<div class="anonlib-hero" markdown>

<h1 class="anonlib-sr-title">anonlib</h1>

Evolutionary community detection for Python, with the heavy lifting done in parallel Rust.

[Getting started](getting-started.md){ .md-button .md-button--primary }
[API reference](api/detectors.md){ .md-button }

</div>

```bash
pip install anonlib
```

<div class="anonlib-highlights">
  <div>
    <strong>Rust + PyO3 core</strong>
    <span>Rayon parallelism on every core</span>
  </div>
  <div>
    <strong>Ten algorithms</strong>
    <span>NSGA-II · NSGA-III · PESA-II · PSO</span>
  </div>
  <div>
    <strong>GPL-3.0-or-later</strong>
    <span>Free and open source</span>
  </div>
</div>

<div class="grid cards" markdown>

- :material-rocket-launch:{ .lg .middle } **Fast by construction**

    ---

    The core is written in Rust with PyO3 bindings and Rayon data
    parallelism — evolutionary search scales across every core you
    give it with `max_cores`.

- :material-power-plug:{ .lg .middle } **Drop-in for NetworkX and igraph**

    ---

    Pass your `networkx.Graph` or `igraph.Graph` directly. Every
    detector returns a plain `dict` mapping node to community.

- :material-flask:{ .lg .middle } **Learn by example**

    ---

    Plot detected communities, plug in custom objectives, and walk
    Pareto fronts with copy-paste-runnable examples.

    [:octicons-arrow-right-24: Examples](examples/plotting.md)

</div>

