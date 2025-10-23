# Build baskets from transactions

import pandas as pd
from pathlib import Path
import argparse

def main(input_csv, out_parquet, out_csv):
    # 1) Load raw file (comma-separated)
    df = pd.read_csv(input_csv, low_memory=False)

    # 2) Parse datetime (your sample is day-first: 30-10-2016 09:58)
    if "date_time" in df.columns:
        df["date_time"] = pd.to_datetime(df["date_time"], dayfirst=True, errors="coerce")

    # 3) Clean item text a bit
    df["Item"] = df["Item"].astype(str).str.strip()

    # 4) Sort by time then transaction (if date_time exists)
    sort_cols = ["date_time", "Transaction"] if "date_time" in df.columns else ["Transaction"]
    df = df.sort_values(sort_cols)

    # 5) Build baskets: unique items per transaction (dedup within basket)
    baskets = (df.groupby("Transaction")["Item"]
                 .apply(lambda s: sorted(set(s)))
                 .reset_index(name="items"))

    # 6) Save
    Path(out_parquet).parent.mkdir(parents=True, exist_ok=True)
    baskets.to_parquet(out_parquet, index=False)
    baskets.to_csv(out_csv, index=False)

    print(f"✅ Baskets: {len(baskets)}")
    print(f"➡ Saved: {out_parquet}")
    print(f"➡ Also saved (CSV): {out_csv}")
    # Show a tiny preview
    print(baskets.head(5).to_string(index=False))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/raw/bread_basket.csv")
    ap.add_argument("--out_parquet", default="data/processed/baskets.parquet")
    ap.add_argument("--out_csv", default="data/processed/baskets.csv")
    args = ap.parse_args()
    main(args.input, args.out_parquet, args.out_csv)
