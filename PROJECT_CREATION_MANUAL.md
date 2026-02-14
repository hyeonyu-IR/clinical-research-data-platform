# Project Creation Manual

## Purpose
This manual standardizes how to add a new clinical research data-entry project under this parent repository.

## Recommended Structure
Each new project should live under `projects/<study_name>/` and include:
1. Streamlit app entry point
2. Study-specific manual
3. Data dictionary
4. Data folder with tracked template CSV and ignored operational data

## Quick Commands
From repository root:
```bash
cp -R projects/_template_registry projects/<study_name>
mv projects/<study_name>/streamlit_registry_template_app.py projects/<study_name>/streamlit_<study_name>_app.py
```

## Required Edits After Copy
1. Update `projects/<study_name>/README.md`
2. Update field schema in app file and in `data/project_data/registry_template.csv`
3. Update data dictionary in `docs/DATA_DICTIONARY_TEMPLATE.md`
4. Add study-specific validation rules in Streamlit form submission logic
5. Add/adjust `.gitignore` rules so PHI-containing operational files are never committed

## Git Hygiene
1. Commit template-based scaffold early.
2. Keep operational CSV exports out of Git.
3. Keep de-identified examples only.

## Suggested Naming Convention
- Directory: `snake_case`
- App file: `streamlit_<study_name>_app.py`
- Project README: `projects/<study_name>/README.md`
- Data dictionary: `projects/<study_name>/docs/<STUDY>_DATA_DICTIONARY.md`

## Journal/Quality Improvement Alignment
1. Lock variable definitions before primary analysis.
2. Version threshold rules in writing (e.g., selectivity criteria).
3. Capture outcome time points explicitly (e.g., 3/6/12 months).
