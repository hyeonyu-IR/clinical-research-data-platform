# AVS Registry Data Dictionary

## Purpose
This dictionary defines the baseline fields for a de-identified adrenal venous sampling (AVS) research registry.

## Core Variables
| Field | Type | Description |
|---|---|---|
| `record_id` | string | Auto-generated unique row ID. |
| `entry_timestamp` | datetime | App timestamp when record was saved. |
| `patient_code` | string | De-identified study ID (no MRN/name). |
| `age_years` | integer | Age at procedure. |
| `sex` | categorical | Female/Male/Other. |
| `bmi_kg_m2` | numeric | Body mass index at procedure period. |
| `procedure_date` | date | AVS procedure date. |
| `operator_name` | string | Primary procedural operator. |
| `referring_service` | string | Referring clinical service. |
| `aldosterone_ng_dl_ivc` | numeric | Aldosterone from IVC sample. |
| `cortisol_ug_dl_ivc` | numeric | Cortisol from IVC sample. |
| `aldosterone_ng_dl_right` | numeric | Aldosterone from right adrenal vein sample. |
| `cortisol_ug_dl_right` | numeric | Cortisol from right adrenal vein sample. |
| `aldosterone_ng_dl_left` | numeric | Aldosterone from left adrenal vein sample. |
| `cortisol_ug_dl_left` | numeric | Cortisol from left adrenal vein sample. |
| `selectivity_index_right` | numeric | Right selectivity index. |
| `selectivity_index_left` | numeric | Left selectivity index. |
| `lateralization_index` | numeric | Lateralization index used for interpretation. |
| `cosyntropin_used` | categorical | Cosyntropin stimulation used during AVS (Yes/No/Unknown). |
| `cosyntropin_route` | categorical | Administration route (infusion/bolus/other/unknown). |
| `cosyntropin_dose` | numeric | Cosyntropin dose in mcg (optional). |
| `contralateral_suppression` | categorical | Yes/No/Unknown. |
| `final_interpretation` | categorical | Unilateral right/left, bilateral, non-diagnostic, indeterminate. |
| `management_plan` | categorical | Surgical/medical/repeat AVS/pending MDT. |
| `bp_improved_3m` | categorical | Blood pressure improvement at 3 months (Yes/No/Unknown). |
| `k_normalized_3m` | categorical | Potassium normalization at 3 months (Yes/No/Unknown). |
| `complication` | categorical | Procedure complication recorded (Yes/No/Unknown). |
| `notes` | free text | Study notes; do not include direct identifiers. |

## Derived App Variables (not stored directly)
| Field | Formula |
|---|---|
| `year` | Year extracted from `procedure_date` |
| `month` | Month extracted from `procedure_date` |
| `bilateral_selective` | `selectivity_index_right >= 2` AND `selectivity_index_left >= 2` |

## Quality Notes
1. Keep direct identifiers out of the dataset.
2. Use one institutional rule set for interpretation thresholds and document that in Methods.
3. For manuscript reproducibility, version any major field definition changes.
