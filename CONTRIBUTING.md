# Contributing Guide

## Scope
This repository hosts reusable Streamlit-based clinical research registry projects under one parent platform.

## Project Structure
1. Keep each study under `projects/<study_name>/`.
2. Use `projects/_template_registry/` as the starting scaffold.
3. Keep one project README, one data dictionary, and one run manual per study.

## Naming Conventions
1. Directory names: `snake_case`
2. Streamlit app file: `streamlit_<study_name>_app.py`
3. Documentation: concise Markdown in the study folder (`README.md`, manual, data dictionary)

## Data Governance
1. Never commit PHI or identifiable operational datasets.
2. Keep operational CSV files local and ignored by `.gitignore`.
3. Commit only templates or de-identified examples.

## Schema and Methods Discipline
1. Define variables and thresholds before primary analysis.
2. Version any schema or definition changes in documentation.
3. Keep derived-variable formulas explicitly documented.

## Commit and PR Style
1. Use clear commit messages with action + scope.
2. Keep commits focused (one logical change per commit when practical).
3. Validate syntax before commit for modified Python files.

## Recommended Workflow for New Study
1. Copy template project:
```bash
cp -R projects/_template_registry projects/<study_name>
```
2. Rename app and update schema/validation.
3. Update study README + data dictionary.
4. Confirm `.gitignore` protects operational data.

## Global Git Identity Setup (One-Time)
Use your real name and institutional/professional email:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
Verify:
```bash
git config --global --get user.name
git config --global --get user.email
```
