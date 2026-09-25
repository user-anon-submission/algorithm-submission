# Pareto fronts

These functions expose the full candidate set a detector selects its final partition from, letting you inspect or re-select solutions yourself.

Six of the ten detector entry points have one. `gdpso` and `cdrme` optimize a single scalar, so they have no Pareto front and no `gdpso_fronts` / `cdrme_fronts`; `mocd_q` and `mocd_d` are multi-objective but expose no front accessor.

::: anonlib.rimpso_fronts

::: anonlib.rimpso_select

::: anonlib.hpmocd_fronts

::: anonlib.mmcomo_fronts

::: anonlib.ccm_fronts

::: anonlib.krm_fronts

::: anonlib.moga_net_fronts
