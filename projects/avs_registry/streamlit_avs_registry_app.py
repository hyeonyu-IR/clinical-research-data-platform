#!/usr/bin/env python3
"""Streamlit AVS registry template: CSV-backed data entry + descriptive dashboard."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any
import uuid

import pandas as pd
import streamlit as st

from reporting.generate_descriptive_report import generate_descriptive_report


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = REPO_ROOT / "data" / "avs" / "avs_registry.csv"
DEFAULT_TEMPLATE_PATH = REPO_ROOT / "data" / "avs" / "avs_registry_template.csv"
DEFAULT_REPORTING_OUTDIR = REPO_ROOT / "reporting" / "outputs"

CSV_COLUMNS = [
    "record_id",
    "entry_timestamp",
    "patient_code",
    "age_years",
    "sex",
    "bmi_kg_m2",
    "procedure_date",
    "operator_name",
    "referring_service",
    "aldosterone_ng_dl_ivc",
    "cortisol_ug_dl_ivc",
    "aldosterone_ng_dl_right",
    "cortisol_ug_dl_right",
    "aldosterone_ng_dl_left",
    "cortisol_ug_dl_left",
    "selectivity_index_right",
    "selectivity_index_left",
    "lateralization_index",
    "contralateral_suppression",
    "final_interpretation",
    "management_plan",
    "bp_improved_3m",
    "k_normalized_3m",
    "complication",
    "notes",
]

INTERPRETATION_OPTIONS = [
    "Unilateral right",
    "Unilateral left",
    "Bilateral hypersecretion",
    "Non-diagnostic",
    "Indeterminate",
]

PLAN_OPTIONS = [
    "Right adrenalectomy",
    "Left adrenalectomy",
    "Medical therapy",
    "Repeat AVS",
    "Pending MDT decision",
]


def ensure_dataset(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    if DEFAULT_TEMPLATE_PATH.exists():
        template_df = pd.read_csv(DEFAULT_TEMPLATE_PATH)
        template_df.to_csv(path, index=False)
        return
    pd.DataFrame(columns=CSV_COLUMNS).to_csv(path, index=False)


def load_data(path: Path) -> pd.DataFrame:
    ensure_dataset(path)
    df = pd.read_csv(path)
    for col in CSV_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    return df[CSV_COLUMNS]


def to_yes_no(value: Any) -> str:
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return "Unknown"


def safe_number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except TypeError:
        pass
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def row_from_form(form: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_id": f"avs_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}",
        "entry_timestamp": datetime.now().isoformat(timespec="seconds"),
        "patient_code": str(form["patient_code"]).strip(),
        "age_years": int(form["age_years"]),
        "sex": form["sex"],
        "bmi_kg_m2": safe_number(form["bmi_kg_m2"]),
        "procedure_date": form["procedure_date"].isoformat(),
        "operator_name": str(form["operator_name"]).strip(),
        "referring_service": str(form["referring_service"]).strip(),
        "aldosterone_ng_dl_ivc": safe_number(form["aldo_ivc"]),
        "cortisol_ug_dl_ivc": safe_number(form["cort_ivc"]),
        "aldosterone_ng_dl_right": safe_number(form["aldo_r"]),
        "cortisol_ug_dl_right": safe_number(form["cort_r"]),
        "aldosterone_ng_dl_left": safe_number(form["aldo_l"]),
        "cortisol_ug_dl_left": safe_number(form["cort_l"]),
        "selectivity_index_right": safe_number(form["si_r"]),
        "selectivity_index_left": safe_number(form["si_l"]),
        "lateralization_index": safe_number(form["li"]),
        "contralateral_suppression": to_yes_no(form["contralateral_suppression"]),
        "final_interpretation": form["final_interpretation"],
        "management_plan": form["management_plan"],
        "bp_improved_3m": to_yes_no(form["bp_improved_3m"]),
        "k_normalized_3m": to_yes_no(form["k_normalized_3m"]),
        "complication": to_yes_no(form["complication"]),
        "notes": str(form["notes"]).strip(),
    }


def validate_entry(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not row["patient_code"]:
        errors.append("Patient code is required (use a de-identified study ID).")
    if row["age_years"] < 18 or row["age_years"] > 100:
        errors.append("Age should be between 18 and 100 years for adult AVS workflow.")
    if not row["operator_name"]:
        errors.append("Operator name is required.")
    proc_date = datetime.fromisoformat(row["procedure_date"]).date()
    if proc_date > date.today():
        errors.append("Procedure date cannot be in the future.")

    if row["final_interpretation"] == "Non-diagnostic" and row["management_plan"] not in {
        "Repeat AVS",
        "Pending MDT decision",
    }:
        errors.append("For non-diagnostic cases, management plan should usually be Repeat AVS or Pending MDT decision.")
    return errors


def append_row(path: Path, row: dict[str, Any]) -> None:
    df = load_data(path)
    updated = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    tmp = path.with_suffix(".tmp")
    updated.to_csv(tmp, index=False)
    tmp.replace(path)


def typed_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out["procedure_date"] = pd.to_datetime(out["procedure_date"], errors="coerce")
    out["year"] = out["procedure_date"].dt.year
    out["month"] = out["procedure_date"].dt.to_period("M").astype(str)

    numeric_cols = [
        "age_years",
        "bmi_kg_m2",
        "selectivity_index_right",
        "selectivity_index_left",
        "lateralization_index",
    ]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out["bilateral_selective"] = (
        (out["selectivity_index_right"] >= 2.0) & (out["selectivity_index_left"] >= 2.0)
    )
    return out


def entry_tab(data_path: Path) -> None:
    st.subheader("AVS Data Entry")
    st.caption("Data are appended to CSV automatically after validation.")

    with st.form("avs_entry_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            patient_code = st.text_input("Patient Study Code*", placeholder="AVS_0001")
            age_years = st.number_input("Age (years)*", min_value=18, max_value=100, value=52, step=1)
            sex = st.selectbox("Sex*", options=["Female", "Male", "Other"])
            bmi_kg_m2 = st.number_input("BMI (kg/m2)", min_value=10.0, max_value=80.0, value=26.0, step=0.1)
        with c2:
            procedure_date = st.date_input("Procedure Date*", value=date.today())
            operator_name = st.text_input("Primary Operator*", placeholder="Interventional radiologist name")
            referring_service = st.text_input("Referring Service", placeholder="Endocrinology")
        with c3:
            final_interpretation = st.selectbox("Final Interpretation*", options=INTERPRETATION_OPTIONS)
            management_plan = st.selectbox("Management Plan*", options=PLAN_OPTIONS)
            contralateral_suppression = st.selectbox("Contralateral Suppression", options=[None, True, False], format_func=to_yes_no)
            complication = st.selectbox("Any Procedure Complication", options=[None, True, False], format_func=to_yes_no)

        st.markdown("**Hormone Measurements and Derived Indices**")
        h1, h2, h3 = st.columns(3)
        with h1:
            aldo_ivc = st.number_input("Aldosterone IVC (ng/dL)", min_value=0.0, value=20.0, step=1.0)
            cort_ivc = st.number_input("Cortisol IVC (ug/dL)", min_value=0.0, value=10.0, step=0.5)
        with h2:
            aldo_r = st.number_input("Aldosterone Right (ng/dL)", min_value=0.0, value=100.0, step=1.0)
            cort_r = st.number_input("Cortisol Right (ug/dL)", min_value=0.0, value=20.0, step=0.5)
            si_r = st.number_input("Selectivity Index Right", min_value=0.0, value=2.0, step=0.1)
        with h3:
            aldo_l = st.number_input("Aldosterone Left (ng/dL)", min_value=0.0, value=100.0, step=1.0)
            cort_l = st.number_input("Cortisol Left (ug/dL)", min_value=0.0, value=20.0, step=0.5)
            si_l = st.number_input("Selectivity Index Left", min_value=0.0, value=2.0, step=0.1)

        li = st.number_input("Lateralization Index", min_value=0.0, value=4.0, step=0.1)
        o1, o2 = st.columns(2)
        with o1:
            bp_improved_3m = st.selectbox("BP Improved at 3 Months", options=[None, True, False], format_func=to_yes_no)
        with o2:
            k_normalized_3m = st.selectbox("Potassium Normalized at 3 Months", options=[None, True, False], format_func=to_yes_no)

        notes = st.text_area(
            "Notes",
            placeholder="Procedure details, interpretation rationale, and follow-up summary. Avoid direct PHI.",
            height=120,
        )

        submit = st.form_submit_button("Save Case")

    if submit:
        raw = {
            "patient_code": patient_code,
            "age_years": age_years,
            "sex": sex,
            "bmi_kg_m2": bmi_kg_m2,
            "procedure_date": procedure_date,
            "operator_name": operator_name,
            "referring_service": referring_service,
            "aldo_ivc": aldo_ivc,
            "cort_ivc": cort_ivc,
            "aldo_r": aldo_r,
            "cort_r": cort_r,
            "aldo_l": aldo_l,
            "cort_l": cort_l,
            "si_r": si_r,
            "si_l": si_l,
            "li": li,
            "contralateral_suppression": contralateral_suppression,
            "final_interpretation": final_interpretation,
            "management_plan": management_plan,
            "bp_improved_3m": bp_improved_3m,
            "k_normalized_3m": k_normalized_3m,
            "complication": complication,
            "notes": notes,
        }
        row = row_from_form(raw)
        errors = validate_entry(row)
        if errors:
            for err in errors:
                st.error(err)
        else:
            append_row(data_path, row)
            st.success(f"Saved case {row['record_id']} to {data_path}.")


def review_tab(df: pd.DataFrame, data_path: Path) -> None:
    st.subheader("Record Review and Export")
    if df.empty:
        st.warning("No records found. Add the first case in the Data Entry tab.")
        return

    display_cols = [
        "record_id",
        "procedure_date",
        "patient_code",
        "sex",
        "age_years",
        "final_interpretation",
        "management_plan",
        "bilateral_selective",
        "complication",
    ]
    st.dataframe(df[display_cols].sort_values("procedure_date", ascending=False), use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Registry CSV",
        data=csv_bytes,
        file_name=f"avs_registry_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

    st.caption(f"Current data source: {data_path}")


def dashboard_tab(df: pd.DataFrame) -> None:
    st.subheader("Descriptive Dashboard")
    if df.empty:
        st.warning("No records available for dashboard rendering.")
        return

    min_date = df["procedure_date"].min().date()
    max_date = df["procedure_date"].max().date()
    c1, c2 = st.columns(2)
    with c1:
        start_date = st.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
    with c2:
        end_date = st.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

    filtered = df[(df["procedure_date"].dt.date >= start_date) & (df["procedure_date"].dt.date <= end_date)].copy()
    if filtered.empty:
        st.info("No records in selected date range.")
        return

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total cases", int(len(filtered)))
    m2.metric("Median age", f"{filtered['age_years'].median():.1f}")
    m3.metric("Bilateral selective rate", f"{100 * filtered['bilateral_selective'].mean():.1f}%")
    m4.metric("Complication rate", f"{100 * (filtered['complication'] == 'Yes').mean():.1f}%")

    yearly = filtered.groupby("year", dropna=True).size().rename("cases")
    st.markdown("**Cases by Year**")
    st.bar_chart(yearly)

    interp = filtered["final_interpretation"].value_counts(dropna=False)
    st.markdown("**Final Interpretation Distribution**")
    st.bar_chart(interp)

    plan = filtered["management_plan"].value_counts(dropna=False)
    st.markdown("**Management Plan Distribution**")
    st.bar_chart(plan)


def _recent_report_runs(report_root: Path, limit: int = 20) -> list[Path]:
    if not report_root.exists():
        return []
    runs = [path for path in report_root.iterdir() if path.is_dir() and path.name.startswith("avs_descriptive_")]
    runs.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return runs[:limit]


def _run_artifact_paths(run_dir: Path) -> list[Path]:
    preferred = [
        run_dir / "01_summary_metrics.csv",
        run_dir / "02_yearly_case_volume.csv",
        run_dir / "03_interpretation_distribution.csv",
        run_dir / "04_management_distribution.csv",
        run_dir / "AVS_Descriptive_Report.md",
    ]
    existing = [p for p in preferred if p.exists()]
    if existing:
        return existing
    return sorted([p for p in run_dir.iterdir() if p.is_file()])


def _render_report_history_panel(report_root: Path) -> None:
    st.markdown("### Report History")
    runs = _recent_report_runs(report_root)
    if not runs:
        st.info("No prior report runs found in the selected output root.")
        return

    run_options = {run.name: run for run in runs}
    selected_name = st.selectbox("Select Previous Report Run", options=list(run_options.keys()))
    selected_run = run_options[selected_name]
    st.caption(f"Run directory: {selected_run}")

    artifacts = _run_artifact_paths(selected_run)
    if not artifacts:
        st.warning("No artifact files found in the selected run folder.")
        return

    st.write("Available artifacts:")
    for artifact in artifacts:
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.code(str(artifact))
        with col_b:
            st.download_button(
                label=f"Download {artifact.name}",
                data=artifact.read_bytes(),
                file_name=artifact.name,
                mime="text/plain",
                key=f"history_download_{selected_name}_{artifact.name}",
            )


def reporting_tab(data_path: Path) -> None:
    st.subheader("Report Generation")
    st.caption("Generate timestamped, manuscript-ready descriptive artifacts from the current registry CSV.")

    report_root_input = st.text_input("Reporting Output Root", value=str(DEFAULT_REPORTING_OUTDIR))
    report_root = Path(report_root_input).expanduser()

    if st.button("Generate Descriptive Report Artifacts"):
        try:
            artifacts = generate_descriptive_report(
                input_csv=data_path,
                outdir_root=report_root,
            )
            st.success(f"Report generated in: {artifacts['run_dir']}")
            st.write("Generated files:")
            st.code(
                "\n".join(
                    [
                        str(artifacts["summary_csv"]),
                        str(artifacts["year_csv"]),
                        str(artifacts["interpretation_csv"]),
                        str(artifacts["management_csv"]),
                        str(artifacts["report_markdown"]),
                    ]
                )
            )

            md_text = Path(artifacts["report_markdown"]).read_text(encoding="utf-8")
            st.download_button(
                label="Download Markdown Report",
                data=md_text,
                file_name=Path(artifacts["report_markdown"]).name,
                mime="text/markdown",
            )
        except Exception as exc:
            st.error(f"Report generation failed: {exc}")

    st.divider()
    _render_report_history_panel(report_root)


def init_sidebar() -> Path:
    st.sidebar.header("Configuration")
    data_path_input = st.sidebar.text_input("Registry CSV Path", value=str(DEFAULT_DATA_PATH))
    data_path = Path(data_path_input).expanduser()

    if st.sidebar.button("Initialize Empty Registry"):
        data_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(columns=CSV_COLUMNS).to_csv(data_path, index=False)
        st.sidebar.success(f"Initialized: {data_path}")

    st.sidebar.info("Use de-identified study codes. Keep direct PHI out of this registry.")
    return data_path


def main() -> None:
    st.set_page_config(page_title="AVS Research Registry", layout="wide")
    st.title("AVS Research Registry Template")
    st.caption("Structured Streamlit data-entry template with CSV backend and descriptive analytics.")

    data_path = init_sidebar()
    df = typed_frame(load_data(data_path))

    tab1, tab2, tab3, tab4 = st.tabs(["Data Entry", "Review / Export", "Dashboard", "Reporting"])
    with tab1:
        entry_tab(data_path)
    with tab2:
        review_tab(df, data_path)
    with tab3:
        dashboard_tab(df)
    with tab4:
        reporting_tab(data_path)


if __name__ == "__main__":
    main()
