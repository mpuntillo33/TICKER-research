# Cold-run log — Project 1 (ACI)

**Goal:** one end-to-end run in a fresh environment, following only the README's "Setup and run" commands, recorded.

| Item | Detail |
|---|---|
| Date / machine | Oct 19, 2026; Windows 11 laptop; PowerShell; Python 3.12.10 |
| Source | Fresh `git clone --branch PROJECT-1` of github.com/mpuntillo33/ticker-research (commit `78a4938`) into a new folder |
| Environment | New virtual environment (`py -3.12 -m venv .venv`), packages from `requirements.txt` only |
| Recordings | Attempt 1: 20:28:51, 1:48 long. Attempt 2: 20:34:27, 4:31 long. Kept outside the repo (file size): `Project 1\Submission\cold-run\` |

## What happened

1. **First failure (attempt 1, 0:00–0:20):** `cd $HOME\Desktop` failed with *"Cannot find path 'C:\Users\maxpu\Desktop' because it does not exist."*
   The Desktop on this machine is redirected (OneDrive), so that folder is not at the default path.
   **Resolution:** ran the README commands from the home folder instead (`C:\Users\maxpu`). This step was a
   convenience line given in chat, not a README instruction; the README itself does not depend on a Desktop folder.
2. Attempt 1 cloned the repo, created `.venv`, and started `pip install -r requirements.txt`; the recording stopped
   during the install (no error on screen).
3. **Attempt 2** continued in the same fresh clone and `.venv` (pip reported packages "already satisfied" from attempt 1), then:
   - `tests\test_engine.py`: **10/10 PASS** (known answers $27.4974 and $291.75, articulation, monotonicity, bridge, changed-input, fail-loudly, comps consistency).
   - `analysis.py`: base **$17.89/share**, EV $18,553m, terminal value 79.7%, all checks PASS.
   - `comps.py`: EV/EBITDA ACI 4.31x, KR 6.33x, SFM 6.95x; consistency checks PASS.
   - `tools\make_report.py` and `jupyter lab app.ipynb`: report regenerated; notebook server and kernel started (20:37:25).

## Limitations

- The two recordings together cover the run; attempt 2 reused attempt 1's fresh clone and environment rather than re-cloning.
- JupyterLab warned "Notebook app.ipynb is not trusted" (expected for a freshly cloned notebook) and "Could not determine jupyterlab build status without nodejs" (cosmetic).
