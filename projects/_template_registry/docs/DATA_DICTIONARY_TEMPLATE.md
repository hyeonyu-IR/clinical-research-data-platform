# Data Dictionary Template

## Study Metadata
- Study name:
- PI:
- Version/date:
- Primary endpoint:

## Variables
| Field | Type | Allowed Values | Definition |
|---|---|---|---|
| `record_id` | string | auto-generated | Unique record identifier |
| `entry_timestamp` | datetime | ISO-8601 | Save timestamp |
| `subject_code` | string | local convention | De-identified subject ID |
| `visit_date` | date | YYYY-MM-DD | Visit/procedure date |
| `category` | categorical | study-defined | Group/category variable |
| `outcome` | categorical/text | study-defined | Primary outcome field |
| `notes` | text | free text | Non-identifying notes |

## Governance Notes
1. Do not include direct identifiers.
2. Document all derived-variable formulas.
3. Record changes in definitions with version/date.
