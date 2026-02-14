# Streamlit Research Registry Template Manual

## Purpose
This manual describes a reusable Streamlit pattern for clinical research data entry with CSV backend storage and instant descriptive analytics.

Primary implementation included in this repository:
- `streamlit_avs_registry_app.py` (AVS-focused baseline)

## Why this helps
1. Reduces friction versus direct spreadsheet editing.
2. Enforces structured fields at entry time.
3. Provides immediate descriptive feedback for project direction.
4. Keeps a clean export for downstream statistical analysis (R/SAS/Python).

## Files Added
1. `streamlit_avs_registry_app.py`
2. `data/avs/avs_registry_template.csv`
3. `docs/AVS_DATA_DICTIONARY.md`
4. `data/avs/README.md`

## Run
From repository root:
```bash
streamlit run streamlit_avs_registry_app.py
```
Default URL:
- `http://localhost:8501`

## Workflow
1. Open app and confirm `Registry CSV Path` in sidebar.
2. Enter one AVS case in **Data Entry**.
3. Click **Save Case**.
4. Review accumulated rows in **Review / Export**.
5. Download CSV for backup or import into R.
6. Inspect trends and distributions in **Dashboard**.

## Validation Rules Included
1. `patient_code` required.
2. Age constrained to adult AVS workflow range (18-100).
3. Procedure date cannot be in the future.
4. For non-diagnostic interpretation, management is restricted to repeat/pending options.

## Adapt This Template to Other Projects
1. Copy `streamlit_avs_registry_app.py` to a new app file.
2. Replace `CSV_COLUMNS` and form fields for your disease/procedure area.
3. Update categorical options and validation rules.
4. Keep a dedicated data dictionary in `docs/`.

## Recommendations for Research Quality
1. Add periodic data-audit checks (missingness, outliers, coding consistency).
2. Freeze a schema version before starting formal analysis.
3. Add a small outcomes module (e.g., 6- and 12-month follow-up).
4. Consider SQLite/PostgreSQL backend once multi-user concurrent data entry grows.

## Constructive Limitations (Current Version)
1. CSV backend is simple but not ideal for concurrent multi-user edits.
2. No role-based authentication is implemented.
3. Advanced statistical modeling is intentionally out of scope.
4. Complication taxonomy is binary in this baseline and may need granularity.

