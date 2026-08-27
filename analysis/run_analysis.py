"""
Main analysis driver. Reads the master dataset + exposure-duration table,
computes participant-minute rates with uncertainty, builds the comparison and
sensitivity tables, and writes results to analysis/output/.

Run: python3 analysis/run_analysis.py
This version runs against the VERIFIED anchor rows; it is extended as the
research agents' rows are appended to data/master_dataset.csv.
"""
import os
import numpy as np
import pandas as pd
from stats_lib import (poisson_ci, rate_ratio, pool_log_rates,
                       rate_per_minute_mc, rate_ratio_mc)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

PER = 1_000_000


def banner(t):
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


def main():
    mpath = os.path.join(ROOT, "data", "master_dataset.csv")
    if os.path.exists(mpath):
        df = pd.read_csv(mpath)
        banner(f"Master dataset loaded: {len(df)} rows")
        print(df[["row_id", "population", "endpoint", "events", "quality"]]
              .to_string(index=False))
    else:
        banner("Master dataset not yet assembled — running anchor smoke test")
    # Smoke test with verified anchors
    banner("Anchor smoke test (verified numbers)")
    r = poisson_ci(19, 4_908_478 * 120, per=PER)
    print(f"NCAA overall serious EHI (transport), 120min/AE: "
          f"{r[0]:.3f} [{r[1]:.3f}, {r[2]:.3f}] per 1e6 min")
    print("stats_lib OK")


if __name__ == "__main__":
    main()
