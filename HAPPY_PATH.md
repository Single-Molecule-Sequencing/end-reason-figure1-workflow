# HAPPY PATH — Exact Reproduce Contract

This repo reproduces Figure 1 as **source-artwork + scripted conversion/packaging**.

## Inputs (must exist)

- `/home/AtheyLab/agent-jobs/end-reason-fig4-recount/end_reason_6_5_26/manuscript/figures/fig1_workflow.pdf`
- `/home/AtheyLab/agent-jobs/end-reason-fig4-recount/end_reason_6_5_26/manuscript/figures/fig1_workflow.png`

## Steps

```bash
git clone https://github.com/Single-Molecule-Sequencing/end-reason-figure1-workflow
cd end-reason-figure1-workflow
python3 2_analysis/scripts/package_figure1.py \
  --source-pdf /home/AtheyLab/agent-jobs/end-reason-fig4-recount/end_reason_6_5_26/manuscript/figures/fig1_workflow.pdf \
  --source-png /home/AtheyLab/agent-jobs/end-reason-fig4-recount/end_reason_6_5_26/manuscript/figures/fig1_workflow.png \
  --out-dir 3_results/figures
```

## Expected outputs

- `3_results/figures/Figure_1_final.pdf`
- `3_results/figures/Figure_1_final.png`
- `3_results/figures/Figure_1_final.svg`

## Contract boundary

- In scope: deterministic packaging + conversion provenance.
- Out of scope: re-authoring the conceptual diagram from raw sequencing records.
