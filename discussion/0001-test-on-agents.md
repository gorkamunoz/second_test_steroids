---
id: 1
title: test on agents
type: task
status: resolved
author: gorkamunoz
waiting_on: none
labels: []
links: []
created: 2026-11-18 11:17
updated: 2026-11-18 11:24
model: opus
run_by: gorkamunoz
---

i am testing this feature, just open a lab, and do a nice plot that surprises me.

<!-- comment author="agent:worker" date="2026-11-18 11:19" -->
Taking this: I'll open a lab with a small, self-contained numerical experiment and a plot that's meant to surprise (plan: the Buffon/π-style 'emergent order from randomness' — likely the eigenvalue spectrum of random matrices or the chaos game). Will report back here with the figure.

_status: open → in-progress_

<!-- comment author="agent:worker" date="2026-11-18 11:24" -->
Done: [[lab:1]], **roots of Littlewood polynomials**.

![](labs/001-roots-of-littlewood-polynomials/figures/littlewood_roots.png)

The figure plots every complex root of every degree-20 polynomial with coefficients ±1: about 1M polynomials and 21M roots, computed in 45 s. You'd expect noise. Instead you get:
- **A ring.** 100% of the roots lie in $1/2<|z|<2$. This is proved, and the one-line argument is in the report. 59% of the roots are within 0.1 of the unit circle.
- **Holes at roots of unity** ($\pm1$, $\pm i$, $e^{\pm i\pi/3}$, …). Often the root of unity itself is a root, so it sits as a lone dot in the centre of its hole.
- **Fractal "dragons"** along the inner and outer edges (zoom on the right).

Report: [[file:labs/001-roots-of-littlewood-polynomials/report.md]]. Code: [[file:labs/001-roots-of-littlewood-polynomials/run.py]]. The run is deterministic, with no seed.

Side notes:
- I added `numpy` and `matplotlib` to `environment.yml` and installed them in the env.
- In this run `./dash` couldn't find the project env, so I opened bug [[thread:2]] with a proposed fix to `dashboard/env.sh`.

_status: in-progress → resolved · waiting on: none_
