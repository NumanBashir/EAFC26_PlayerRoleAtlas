import pandas as pd

files = [
    r"data/raw/all_leagues/BIG_per90_BrasileiroSerieA_25.csv",
    r"data/raw/all_leagues/BIG_per90_Bundesliga_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_Championship_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_Eredivisie_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_JupilerProLeague_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_LaLiga_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_LigaMX_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_LigaProfesionalArgentina_25.csv",
    r"data/raw/all_leagues/BIG_per90_Ligue1_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_MLS_25.csv",
    r"data/raw/all_leagues/BIG_per90_PremierLeague_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_Primeira_Liga_24_25.csv",
    r"data/raw/all_leagues/BIG_per90_SerieA_24_25.csv",
]

# Read each file and append rows
dfs = [pd.read_csv(path, low_memory=False) for path in files]
combined = pd.concat(dfs, ignore_index=True)

# Write one combined CSV (comma-separated)
combined.to_csv(r"data/processed/combined.csv", index=False)

print(f"Combined {len(files)} files → combined.csv ({len(combined)} rows)")
