# 🍓 Strawberry Canyon — Ephemeral Strike Scanner

A lightweight Python scanner for detecting actionable option strikes within **1 ATR of spot** using:

- dual-vendor parity
- gamma exposure proxies
- auditable feed hashes
- structured CSV emit rows

Built for:

- Gamma Garden
- Strawberry Canyon
- strike-volume monitoring
- fast gamma workflows
- low-entropy options scanning

---

# Philosophy

```text
Simple inputs.
Hard gates.
Replayable outputs.
```

The scanner is intentionally minimal.

It does not attempt to predict markets.

It identifies nearby strikes where dealer hedging activity, gamma concentration, and liquidity conditions may create short-lived opportunities worth inspecting.

---

# Features

- ✅ Strike filtering within 1 ATR
- ✅ Dual-vendor parity validation
- ✅ Gamma exposure estimation
- ✅ Bid-ask spread checks
- ✅ SHA-256 feed hashing
- ✅ Structured emit rows
- ✅ Trello / Airtable compatible
- ✅ Strawberry Canyon pipeline friendly

---

# Inputs

The scanner expects:

```text
1. Vendor minute CSV #1
2. Vendor minute CSV #2
3. Options chain snapshot CSV
4. ATR14 CSV
```

Example vendors:

- MarketChameleon
- Barchart

---

# Core Logic

The scanner calculates:

```text
dist_atr = abs(strike - spot) / ATR14
```

Only strikes with:

```text
dist_atr <= 1.0
```

are emitted.

The script also validates:

- vendor price agreement
- liquidity quality
- gamma concentration

before creating an output row.

---

# Example Emit Row

```csv
emit_id,symbol,expiry,strike,side,spot,atr14,dist_atr,oi,gamma_per_contract,gex_1pct
sv_gg_001,QQQ,2026-06-19,715,call,712.00,4.04,0.74,1200,0.012,7299994
```

---

# Repository Structure

```text
strawberry-canyon-ephemeral-strike-scanner/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── scanner/
│   └── scan_ephemeral_strikes.py
│
├── docs/
│   └── strawberry-canyon-ephemeral-strike-scanner.md
│
├── samples/
│   ├── options_chain_QQQ.csv
│   ├── marketchameleon_QQQ_1m.csv
│   └── barchart_QQQ_1m.csv
│
└── output/
    └── sv_emit_rows.csv
```

---

# Installation

```bash
pip install -r requirements.txt
```

---

# Run

```bash
python scanner/scan_ephemeral_strikes.py
```

---

# Output

The scanner appends rows to:

```text
output/sv_emit_rows.csv
```

Each row includes:

- strike
- side
- spot
- ATR distance
- open interest
- gamma proxy
- spread quality
- parity state
- feed hashes
- timestamp

---

# Auditability

Every emitted row contains SHA-256 hashes of the underlying vendor files.

This preserves a replayable evidence trail for:

- research
- journaling
- automation
- forensic review

---

# Strawberry Canyon

Designed for integration into:

```text
03_portfolio/gamma
```

or:

```text
inbox/gamma_garden
```

Potential downstream integrations:

- Trello
- Airtable
- Obsidian
- Discord alerts
- execution dashboards

---

# Design Goal

The goal is not maximum complexity.

The goal is:

```text
Capture high-signal option structure
with minimal operational friction.
```

---

# License

MIT

---

# Author

Darren Hill  
Strawberry Canyon
