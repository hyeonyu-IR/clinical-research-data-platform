# Clinical Research Data Platform

Centralized repository for Streamlit-based clinical research data-entry tools and lightweight analytics.

## Repository Strategy
- Keep one parent repository for shared patterns and governance.
- Implement each clinical study as a sub-project under `projects/`.
- Avoid creating many near-duplicate repositories for each project.

## Current Sub-Projects
- `projects/avs_registry`: Adrenal Venous Sampling (AVS) registry template.

## Suggested Expansion Path
1. Add `projects/<new_study>/` using the same template pattern.
2. Keep a data dictionary and run manual per sub-project.
3. Export clean CSV for downstream formal statistics in R.

## Next GitHub Step
After the first local commit, create one GitHub repository for this parent platform and push `main`.
