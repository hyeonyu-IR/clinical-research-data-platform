# AVS Reporting Manual

## Purpose
Generate reproducible descriptive outputs (CSV + Markdown) from the AVS registry for interim review, QI meetings, and manuscript preparation.

## Option A: In Streamlit (Recommended)
1. Run app:
```bash
streamlit run projects/avs_registry/streamlit_avs_registry_app.py
```
2. Open the **Reporting** tab.
3. Confirm `Reporting Output Root` path.
4. Click **Generate Descriptive Report Artifacts**.
5. Review generated file paths and download markdown report if needed.
6. In **Report History**, select a prior run and download any artifact file (CSV/Markdown) directly.

## Option B: Command Line
Script:
- `projects/avs_registry/reporting/generate_descriptive_report.py`

Run from repository root:
```bash
python projects/avs_registry/reporting/generate_descriptive_report.py \
  --input projects/avs_registry/data/avs/avs_registry.csv \
  --outdir projects/avs_registry/reporting/outputs
```

## Output Structure
Each run creates a timestamped folder:
- `projects/avs_registry/reporting/outputs/avs_descriptive_<YYYYMMDD_HHMMSS>/`

Files generated:
1. `01_summary_metrics.csv`
2. `02_yearly_case_volume.csv`
3. `03_interpretation_distribution.csv`
4. `04_management_distribution.csv`
5. `AVS_Descriptive_Report.md`

## Notes
1. If input CSV is empty, script still produces empty-but-structured files.
2. This is descriptive reporting only; final inferential statistics should be performed in R.
3. Keep operational data de-identified and out of Git.
