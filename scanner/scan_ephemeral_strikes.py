import csv
import hashlib
import json
from pathlib import Path

SYMBOL = "QQQ"
EXPIRY = "2026-06-19"
CONTRACT_SIZE = 100
TOL_PRICE = 0.02

VENDOR_FILES = {
    "MC": r"C:\Users\darre\Dropbox\strawberry_canyon\inbox\marketchameleon_QQQ_1m.csv",
    "BCH": r"C:\Users\darre\Dropbox\strawberry_canyon\inbox\barchart_QQQ_1m.csv",
}

OPTIONS_SNAP = r"C:\Users\darre\Dropbox\strawberry_canyon\inbox\options_chain_QQQ.csv"
ATR14_FILE = r"C:\Users\darre\Dropbox\strawberry_canyon\inbox\atr14_QQQ.csv"
OUT_CSV = r"C:\Users\darre\Dropbox\strawberry_canyon\inbox\sv_emit_rows.csv"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def read_last_row(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
        return rows[-1] if rows else None


def load_chain(path):
    chain = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("symbol") == SYMBOL and row.get("expiry") == EXPIRY:
                key = (float(row["strike"]), row["side"].lower())
                chain[key] = row
    return chain


def load_atr(path):
    row = read_last_row(path)
    return float(row["atr14"]) if row and row.get("atr14") else None


def parity_ok(row_a, row_b):
    if not row_a or not row_b:
        return False

    price_a = float(row_a.get("close") or row_a.get("last") or row_a.get("vwap"))
    price_b = float(row_b.get("close") or row_b.get("last") or row_b.get("vwap"))

    return abs(price_a - price_b) <= TOL_PRICE


def spread_pct(bid, ask):
    mid = (bid + ask) / 2.0
    return (ask - bid) / mid if mid > 0 else 1.0


def main():
    row_mc = read_last_row(VENDOR_FILES["MC"])
    row_bch = read_last_row(VENDOR_FILES["BCH"])

    if not parity_ok(row_mc, row_bch):
        print("NO EMIT: dual-vendor parity failed")
        return

    spot = float(row_mc.get("close") or row_mc.get("last") or row_mc.get("vwap"))
    atr14 = load_atr(ATR14_FILE)

    if not atr14 or atr14 <= 0:
        print("NO EMIT: missing or invalid ATR14")
        return

    chain = load_chain(OPTIONS_SNAP)
    emits = []

    for (strike, side), row in chain.items():
        dist_atr = abs(strike - spot) / atr14

        if dist_atr <= 1.0:
            oi = float(row.get("oi", 0))
            gamma = float(row.get("gamma_per_contract", row.get("gamma", 0)))
            bid = float(row.get("bid", 0) or 0)
            ask = float(row.get("ask", 0) or 0)

            gex_1pct = gamma * CONTRACT_SIZE * oi * (spot ** 2) * 0.01
            gamma_vega_proxy = gamma * max(1.0, float(row.get("iv", 0.0))) * CONTRACT_SIZE
            spread = spread_pct(bid, ask)

            emits.append({
                "emit_id": f"sv_gg_{Path(OUT_CSV).stem}_{len(emits) + 1}",
                "symbol": SYMBOL,
                "expiry": EXPIRY,
                "strike": strike,
                "side": side,
                "spot": round(spot, 2),
                "atr14": round(atr14, 2),
                "dist_atr": round(dist_atr, 2),
                "oi": int(oi),
                "gamma_per_contract": round(gamma, 6),
                "gex_1pct": int(gex_1pct),
                "gamma_vega_proxy": int(gamma_vega_proxy),
                "bid": round(bid, 2),
                "ask": round(ask, 2),
                "spread_pct": round(spread, 2),
                "dual_vendor_parity": True,
                "feed_hashes": json.dumps([
                    sha256_file(VENDOR_FILES["MC"]),
                    sha256_file(VENDOR_FILES["BCH"]),
                ]),
                "mc_chain_uri": "LIVE_MC_CHAIN_URI",
                "bch_chain_uri": "LIVE_BCH_CHAIN_URI",
                "timestamp_utc": row_mc.get("timestamp") or row_mc.get("datetime") or "LIVE_TS",
            })

    if not emits:
        print("NO EMIT: no strikes within 1 ATR")
        return

    header = [
        "emit_id",
        "symbol",
        "expiry",
        "strike",
        "side",
        "spot",
        "atr14",
        "dist_atr",
        "oi",
        "gamma_per_contract",
        "gex_1pct",
        "gamma_vega_proxy",
        "bid",
        "ask",
        "spread_pct",
        "dual_vendor_parity",
        "feed_hashes",
        "mc_chain_uri",
        "bch_chain_uri",
        "timestamp_utc",
    ]

    output_path = Path(OUT_CSV)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    exists = output_path.exists()

    with open(output_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)

        if not exists:
            writer.writeheader()

        for emit in emits:
            writer.writerow(emit)

    print(f"EMITTED {len(emits)} row(s) → {OUT_CSV}")


if __name__ == "__main__":
    main()
