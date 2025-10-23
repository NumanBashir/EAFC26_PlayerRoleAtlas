# src/mine_rules.py
import pandas as pd
from pathlib import Path
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import argparse

def main(baskets_path, out_dir, min_support, min_conf):
    # 1) load baskets from Phase 1 (column: items = list[str])
    df = pd.read_parquet(baskets_path) if baskets_path.endswith(".parquet") else pd.read_csv(baskets_path)
    baskets = df["items"].apply(lambda x: x if isinstance(x, list) else eval(x)).tolist()

    # 2) binarize (one-hot per item)
    te = TransactionEncoder()
    X = pd.DataFrame(te.fit(baskets).transform(baskets), columns=te.columns_)

    # 3) frequent itemsets (Apriori)
    freq = apriori(X, min_support=min_support, use_colnames=True)

    # 4) association rules (confidence+lift)
    rules = association_rules(freq, metric="confidence", min_threshold=min_conf)
    # make sets readable
    rules["antecedents"] = rules["antecedents"].apply(lambda s: tuple(sorted(s)))
    rules["consequents"] = rules["consequents"].apply(lambda s: tuple(sorted(s)))

    # 5) save outputs
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    freq.sort_values("support", ascending=False).to_csv(f"{out_dir}/frequent_itemsets.csv", index=False)
    rules.sort_values(["lift","confidence"], ascending=False).to_csv(f"{out_dir}/rules.csv", index=False)

    print(f"✅ itemsets={len(freq)} | rules={len(rules)} → {out_dir}")
    print(rules.head(10).to_string(index=False))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--baskets", default="data/processed/baskets.parquet")
    ap.add_argument("--out_dir", default="outputs")
    ap.add_argument("--min_support", type=float, default=0.01)  # tweak if too many/few itemsets
    ap.add_argument("--min_conf", type=float, default=0.2)
    args = ap.parse_args()
    main(args.baskets, args.out_dir, args.min_support, args.min_conf)
