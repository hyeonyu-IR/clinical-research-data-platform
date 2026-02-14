# Clinical Research Data Platform

Centralized repository for Streamlit-based clinical research data-entry tools and lightweight analytics.

## Repository Strategy
- Keep one parent repository for shared patterns and governance.
- Implement each clinical study as a sub-project under `projects/`.
- Avoid creating many near-duplicate repositories for each project.

## Current Sub-Projects
- `projects/avs_registry`: Adrenal Venous Sampling (AVS) registry implementation.
- `projects/_template_registry`: Reusable starter scaffold for new registry projects.

## Standard Workflow for New Study
1. Copy template: `cp -R projects/_template_registry projects/<study_name>`
2. Rename app file to `streamlit_<study_name>_app.py`
3. Update schema and validation logic in app + data dictionary
4. Keep operational data local and git-ignored

Detailed steps: `PROJECT_CREATION_MANUAL.md`

## Current AVS Project
Run AVS app:
```bash
streamlit run projects/avs_registry/streamlit_avs_registry_app.py
```

## Suggested Expansion Path
1. Add `projects/<new_study>/` using the template scaffold.
2. Keep one data dictionary and one run manual per sub-project.
3. Export clean CSV for downstream formal statistics in R.

## Next GitHub Step
Create one GitHub repository for this parent platform and push `main`.
