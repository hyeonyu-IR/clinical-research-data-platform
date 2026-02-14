# AVS Registry Sub-Project

Streamlit-based data entry and descriptive dashboard for adrenal venous sampling (AVS) research.

## Run Streamlit App
```bash
streamlit run projects/avs_registry/streamlit_avs_registry_app.py
```

## Generate Descriptive Report Artifacts
```bash
python projects/avs_registry/reporting/generate_descriptive_report.py \
  --input projects/avs_registry/data/avs/avs_registry.csv \
  --outdir projects/avs_registry/reporting/outputs
```

See: `projects/avs_registry/REPORTING_MANUAL.md`

## Key Files
- `projects/avs_registry/streamlit_avs_registry_app.py`
- `projects/avs_registry/STREAMLIT_RESEARCH_TEMPLATE_MANUAL.md`
- `projects/avs_registry/REPORTING_MANUAL.md`
- `projects/avs_registry/reporting/generate_descriptive_report.py`
- `projects/avs_registry/docs/AVS_DATA_DICTIONARY.md`
- `projects/avs_registry/data/avs/avs_registry_template.csv`
