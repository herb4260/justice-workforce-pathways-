# Methods

## Conceptual structure
The design separates **acute occupational exposure** (critical incidents, violence exposure) from **chronic organizational/operational stress** (overtime, staffing pressure, schedule instability, perceived fairness). It then evaluates support, stigma, help-seeking, distress, burnout, suicidal ideation, and retention over time.

## Mixed-methods logic
The synthetic cohort links three evidence streams by `person_id` and `wave`: (1) repeated self-report measures, (2) administrative/personnel indicators, and (3) semi-structured interview excerpts. Quantitative and qualitative results are integrated in a joint-display table rather than treated as unrelated projects.

## Quantitative models
- Gaussian GEE: person-clustered repeated distress, including an organizational stress × supervisor-support interaction.
- Lagged panel regression: prior-wave predictors of next-wave distress.
- Binomial GEE: help-seeking as a repeated binary outcome.
- Discrete-time binomial GEE: turnover hazard across post-baseline risk intervals among personnel still at risk; baseline is excluded because no turnover interval exists at entry by design.

## Qualitative component
Synthetic interview excerpts are generated from a transparent theme dictionary: stigma, organizational distrust, supervisor support, peer support, workload, critical incidents, and help-seeking access. Coding is deterministic and auditable; it is intended to demonstrate a reproducible content-analysis workflow, not automated inference about real interviews.

## Methodological grounding
The architecture is informed by public descriptions of longitudinal correctional-officer well-being research that combines repeated interviews, organizational context, administrative/personnel records, and qualitative inquiry, including Northeastern University's *Turning Points in the Careers of Correction Officers* and correction-officer well-being projects. The project remains independent: sample size, variables, synthetic data-generating mechanisms, code, and results are original to this repository.

References:
- Northeastern University School of Criminology and Criminal Justice. Turning Points in the Careers of Correction Officers.
- National Institute of Justice / Office of Justice Programs. Research on correction officer suicide, institutional environment, and well-being.
