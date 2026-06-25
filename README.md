# End-Reason Figure 1 — Workflow Illustration

<!-- LAB:DASHBOARD-BADGE BEGIN -->
📊 **[Live dashboard](https://single-molecule-sequencing.github.io/end-reason-figure1-workflow/)**
<!-- LAB:DASHBOARD-BADGE END -->

Companion repo for Figure 1 from the end-reason manuscript.

## 3-folder map

| Folder | Purpose |
|---|---|
| `1_experiment/` | Source-artwork pointers + lifecycle notes for the canonical figure assets |
| `2_analysis/` | Scripted conversion/packaging contract (`commands.md`, `scripts/environment.yaml`) |
| `3_results/` | Final figure outputs and legend/provenance notes |

Additional infrastructure:
- `HAPPY_PATH.md` — exact reproduce contract
- `analysis.yaml` — analysis manifest metadata
- `docs/index.html` — static dashboard for GitHub Pages
- `provenance/runs.jsonl` — append-only artifact production log
