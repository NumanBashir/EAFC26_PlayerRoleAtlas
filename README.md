# EAFC26 Player Role Atlas

Cluster EAFC26 players into interpretable role archetypes per position family (DF/MF/FW; GK separate), evaluate with silhouette/DBI, and visualize with a 2D UMAP role map.

---

## Setup & Run

1. **Clone and create a virtual env**

   ```bash
   git clone https://github.com/NumanBashir/EAFC26_PlayerRoleAtlas eafc26-role-atlas
   cd eafc26-role-atlas

   python -m venv .venv
   # mac/linux
   source .venv/bin/activate
   # windows (PowerShell)
   # .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
