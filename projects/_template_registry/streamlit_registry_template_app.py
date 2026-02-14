#!/usr/bin/env python3
"""Generic Streamlit registry template for clinical research sub-projects."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = REPO_ROOT / "projects" / "_template_registry" / "data" / "project_data" / "registry.csv"

# Replace these columns for each study-specific project.
CSV_COLUMNS = [
    "record_id",
    "entry_timestamp",
    "subject_code",
    "visit_date",
    "category",
    "outcome",
    "notes",
]


def ensure_dataset(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        pd.DataFrame(columns=CSV_COLUMNS).to_csv(path, index=False)


def load_data(path: Path) -> pd.DataFrame:
    ensure_dataset(path)
    df = pd.read_csv(path)
    for col in CSV_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    return df[CSV_COLUMNS]


def append_row(path: Path, row: dict[str, object]) -> None:
    df = load_data(path)
    out = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    tmp = path.with_suffix(".tmp")
    out.to_csv(tmp, index=False)
    tmp.replace(path)


def main() -> None:
    st.set_page_config(page_title="Registry Template", layout="wide")
    st.title("Clinical Registry Template")
    st.caption("Replace schema, validation, and dashboard logic for each study.")

    data_path = Path(st.sidebar.text_input("Registry CSV Path", str(DEFAULT_DATA_PATH))).expanduser()
    df = load_data(data_path)

    tab1, tab2, tab3 = st.tabs(["Data Entry", "Review", "Dashboard"])

    with tab1:
        with st.form("entry_form", clear_on_submit=True):
            subject_code = st.text_input("Subject Code*")
            visit_date = st.date_input("Visit Date", value=date.today())
            category = st.text_input("Category")
            outcome = st.text_input("Outcome")
            notes = st.text_area("Notes")
            submit = st.form_submit_button("Save")

        if submit:
            if not subject_code.strip():
                st.error("Subject Code is required.")
            else:
                row = {
                    "record_id": f"rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "entry_timestamp": datetime.now().isoformat(timespec="seconds"),
                    "subject_code": subject_code.strip(),
                    "visit_date": visit_date.isoformat(),
                    "category": category.strip(),
                    "outcome": outcome.strip(),
                    "notes": notes.strip(),
                }
                append_row(data_path, row)
                st.success("Record saved.")

    with tab2:
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"registry_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

    with tab3:
        st.metric("Total records", len(df))
        if not df.empty and "visit_date" in df.columns:
            plot_df = df.copy()
            plot_df["visit_date"] = pd.to_datetime(plot_df["visit_date"], errors="coerce")
            trend = plot_df.dropna(subset=["visit_date"]).groupby(plot_df["visit_date"].dt.to_period("M")).size()
            if not trend.empty:
                st.bar_chart(trend)


if __name__ == "__main__":
    main()
