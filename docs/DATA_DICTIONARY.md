# Data dictionary

## `officer_panel.csv`
| Variable | Meaning |
|---|---|
| `person_id` | Synthetic officer/recruit identifier |
| `cohort_id` | Synthetic training cohort |
| `unit_id` | Synthetic organizational unit |
| `wave` | 0 baseline, 1 post, 2 six-month follow-up |
| `treatment` | Cohort assignment to training condition |
| `gender` | Synthetic gender category used for moderation demonstration |
| `org_justice` | Perceived organizational justice, 1–7 |
| `supervisor_support` | Perceived supervisor support, 1–7 |
| `internal_locus` | Internal locus-of-control proxy, 1–7 |
| `self_efficacy` | Self-efficacy proxy, 1–7 |
| `training_motivation` | Motivation to engage with training, 1–7 |
| `receptivity` | Mean of satisfaction and perceived skill acquisition, 1–7 |
| `scenario_skill` | Synthetic behavioral-health scenario performance, 20–100 |
| `behavioral_health_confidence` | Confidence responding to behavioral-health calls, 1–7 |
| `distress` | Synthetic psychological distress, 1–7 |
| `help_seeking_intent` | Intent to seek support if needed, 1–7 |
| `overtime_hours` | Synthetic interval overtime exposure |
| `critical_incidents` | Synthetic critical-incident count |
| `implementation_fidelity` | Synthetic cohort implementation fidelity |

## `scenario_events.csv`
Repeated four-scenario transfer assessment at six months, with scenario type, performance score, and a synthetic safe-resolution indicator.

## `implementation_interviews.csv`
Synthetic interview excerpts used only to demonstrate transparent qualitative coding and mixed-method integration.
