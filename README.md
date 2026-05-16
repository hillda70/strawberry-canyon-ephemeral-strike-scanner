# 🍓 Strawberry Canyon

> *Two travelers on the Tōkaidō road, bent into sudden rain, pressing forward.*  
> *The whole is assumed. The parts are what you notice when you look more carefully.*  
> — After Hiroshige, *Driving Rain at Shōno*, c. 1833

---

Strawberry Canyon is a framework for understanding markets as adaptive physiological systems rather than deterministic machines.

Most technical analysis assumes mechanism: parts assembled into a whole, signals producing fixed outputs. Strawberry Canyon assumes the opposite. The regime is the whole. The signals are derived from it.

The framework converts structured market data into cross-asset regime surfaces, volatility state models, and execution-oriented signal layers.

The philosophical foundation is **functional contextualism** — the tradition running from William James through Stephen C. Pepper to Steven Hayes. Truth is what works in service of a goal, situated in context. An indicator is not true or false. It is functional or non-functional relative to the current regime and your position within it.

The core phrase: **committed action in context.**

---

## The ecosystem

| Repo | Layer | Description |
|------|-------|-------------|
| `strawberry-canyon` | Philosophy & engine | Core framework, regime model, market physiology |
| [`ripple-prism`](https://github.com/hillda70/ripple-prism) | Structural / gamma | Dealer gamma positioning, systematic flows, liquidity regime transitions |
| [`strawberry-canyon-ephemeral-strike-scanner`](https://github.com/hillda70/strawberry-canyon-ephemeral-strike-scanner) | Execution | Lightweight options strike scanner for Gamma Garden and Strawberry Canyon workflows |
| [`gamma-garden-preflight`](https://github.com/hillda70/gamma-garden-preflight) | Execution | Preflight validation layer for Gamma Garden workflows |

---

## Core concepts

**SUI — Scroll Utilization Index**  
`HiLo% / ATRP` — range utilization relative to expected volatility. Measures how much of the vol budget has been consumed. SUI > 1.0 is nonlinear territory.

**Session Force (S_F)**  
Directional conviction of the session relative to prior structure. Positive or negative. The primary axis of the phase space.

**Fragility ratio**  
`ROC(13) / ATRP(14)` — momentum per unit of volatility. Measures whether a move is earning its vol budget.

**Dist_Fib50**  
Distance from the 50% Fibonacci retracement of the 3-month range, expressed in ATRs. Structural position within the cycle.

**The phase space**

| | IV rising | IV falling |
|---|---|---|
| **S_F positive** | Active propagation | Orderly stabilization |
| **S_F negative** | Downside transmission | Exhaustion / absorption |

---

## Repository structure

```
strawberry-canyon/
├── src/          # Core engine and signal computation
├── docs/         # Framework documentation and working papers
├── examples/     # Reference implementations
└── README.md
```

---

## Philosophy

Markets are not machines. They are adaptive systems moving through interacting states — compressing, releasing, propagating, absorbing.

The edge does not come from indicators. It comes from recognizing when movement is likely to propagate, when it is likely to dissipate, and when the system is transitioning between those states.

This is participant ethnography of markets. The observation and the participation are inseparable. The knowledge cannot be obtained any other way.

For the full theoretical framework, see [`docs/manifesto.md`](docs/manifesto.md).

---

**Strawberry Canyon Partners**  
Chicago, Illinois · 2026  
Author: Darren Hill
