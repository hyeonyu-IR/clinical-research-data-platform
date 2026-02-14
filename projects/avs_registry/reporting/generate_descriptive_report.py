#!/usr/bin/env python3
"""Generate reproducible descriptive AVS research outputs from registry CSV."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AVS descriptive report artifacts")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("projects/avs_registry/data/avs/avs_registry.csv"),
        help="Path to AVS registry CSV",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("projects/avs_registry/reporting/outputs"),
        help="Output directory root for report artifacts",
    )
    return parser.parse_args()


def load_and_type(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if df.empty:
        return df

    if "procedure_date" in df.columns:
        df["procedure_date"] = pd.to_datetime(df["procedure_date"], errors="coerce")
        df["year"] = df["procedure_date"].dt.year

    for col in ["age_years", "selectivity_index_right", "selectivity_index_left", "lateralization_index"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if {"selectivity_index_right", "selectivity_index_left"}.issubset(df.columns):
        df["bilateral_selective"] = (
            (df["selectivity_index_right"] >= 2.0) & (df["selectivity_index_left"] >= 2.0)
        )
    else:
        df["bilateral_selective"] = pd.NA

    return df


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            {
                "metric": [
                    "total_cases",
                    "median_age_years",
                    "female_percent",
                    "bilateral_selective_percent",
                    "complication_percent",
                ],
                "value": [0, pd.NA, pd.NA, pd.NA, pd.NA],
            }
        )

    female_pct = pd.NA
    if "sex" in df.columns and len(df) > 0:
        female_pct = round(100.0 * (df["sex"].astype(str).str.lower() == "female").mean(), 1)

    bilateral_pct = pd.NA
    if "bilateral_selective" in df.columns:
        bilateral_pct = round(100.0 * pd.to_numeric(df["bilateral_selective"], errors="coerce").mean(), 1)

    complication_pct = pd.NA
    if "complication" in df.columns and len(df) > 0:
        complication_pct = round(100.0 * (df["complication"].astype(str) == "Yes").mean(), 1)

    med_age = pd.NA
    if "age_years" in df.columns:
        med_age = round(df["age_years"].median(), 1)

    return pd.DataFrame(
        {
            "metric": [
                "total_cases",
                "median_age_years",
                "female_percent",
                "bilateral_selective_percent",
                "complication_percent",
            ],
            "value": [len(df), med_age, female_pct, bilateral_pct, complication_pct],
        }
    )


def write_markdown_report(df: pd.DataFrame, summary_df: pd.DataFrame, out_md: Path) -> None:
    lines: list[str] = []
    lines.append("# AVS Descriptive Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")

    lines.append("## Cohort Summary")
    lines.append("")
    for _, row in summary_df.iterrows():
        lines.append(f"- {row['metric']}: {row['value']}")

    lines.append("")
    lines.append("## Annual Case Volume")
    lines.append("")
    if not df.empty and "year" in df.columns:
        yearly = df.groupby("year", dropna=True).size().sort_index()
        if yearly.empty:
            lines.append("- No valid procedure dates available.")
        else:
            for y, n in yearly.items():
                lines.append(f"- {int(y)}: {int(n)}")
    else:
        lines.append("- No data available.")

    lines.append("")
    lines.append("## Interpretation Distribution")
    lines.append("")
    if not df.empty and "final_interpretation" in df.columns:
        counts = df["final_interpretation"].value_counts(dropna=False)
        for k, n in counts.items():
            lines.append(f"- {k}: {int(n)}")
    else:
        lines.append("- No data available.")

    lines.append("")
    lines.append("## Management Distribution")
    lines.append("")
    if not df.empty and "management_plan" in df.columns:
        counts = df["management_plan"].value_counts(dropna=False)
        for k, n in counts.items():
            lines.append(f"- {k}: {int(n)}")
    else:
        lines.append("- No data available.")

    out_md.write_text("\n".join(lines), encoding="utf-8")


def generate_descriptive_report(input_csv: Path, outdir_root: Path) -> dict[str, Path]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    in_path = input_csv.expanduser().resolve()
    outdir = outdir_root.expanduser().resolve() / f"avs_descriptive_{timestamp}"
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_and_type(in_path)
    summary_df = summary_table(df)

    summary_csv = outdir / "01_summary_metrics.csv"
    year_csv = outdir / "02_yearly_case_volume.csv"
    interp_csv = outdir / "03_interpretation_distribution.csv"
    plan_csv = outdir / "04_management_distribution.csv"
    md_path = outdir / "AVS_Descriptive_Report.md"

    summary_df.to_csv(summary_csv, index=False)

    if not df.empty and "year" in df.columns:
        df.groupby("year", dropna=True).size().reset_index(name="cases").to_csv(year_csv, index=False)
    else:
        pd.DataFrame(columns=["year", "cases"]).to_csv(year_csv, index=False)

    if not df.empty and "final_interpretation" in df.columns:
        (
            df["final_interpretation"]
            .value_counts(dropna=False)
            .rename_axis("final_interpretation")
            .reset_index(name="cases")
            .to_csv(interp_csv, index=False)
        )
    else:
        pd.DataFrame(columns=["final_interpretation", "cases"]).to_csv(interp_csv, index=False)

    if not df.empty and "management_plan" in df.columns:
        (
            df["management_plan"]
            .value_counts(dropna=False)
            .rename_axis("management_plan")
            .reset_index(name="cases")
            .to_csv(plan_csv, index=False)
        )
    else:
        pd.DataFrame(columns=["management_plan", "cases"]).to_csv(plan_csv, index=False)

    write_markdown_report(df=df, summary_df=summary_df, out_md=md_path)

    return {
        "run_dir": outdir,
        "summary_csv": summary_csv,
        "year_csv": year_csv,
        "interpretation_csv": interp_csv,
        "management_csv": plan_csv,
        "report_markdown": md_path,
    }


def main() -> None:
    args = parse_args()
    artifacts = generate_descriptive_report(input_csv=args.input, outdir_root=args.outdir)

    print("Generated report artifacts:")
    print(f"- {artifacts['summary_csv']}")
    print(f"- {artifacts['year_csv']}")
    print(f"- {artifacts['interpretation_csv']}")
    print(f"- {artifacts['management_csv']}")
    print(f"- {artifacts['report_markdown']}")


if __name__ == "__main__":
    main()
