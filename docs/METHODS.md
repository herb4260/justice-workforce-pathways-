# Methods

## Aim
This repository is a synthetic methodological prototype for evaluating police training as an **organizational process**, not merely as a pre/post score change. It asks how perceptions of organizational justice and supervisor support shape training motivation and receptivity, how receptivity predicts later transfer, and whether implementation problems are diffuse or concentrated across organizational units and training contexts.

## Design
- 480 synthetic police recruits/officers nested in 24 training cohorts and 8 units.
- Cohort-level assignment to a behavioral-health communication training condition or wait-list comparison.
- Three waves: baseline, immediate post-training, and six-month follow-up.
- Linked synthetic survey, scenario-performance, workload/administrative, and semi-structured interview streams.
- Four behavioral-health transfer scenarios: suicidal crisis, psychosis, youth behavioral-health crisis, and cognitive disability.

## Quantitative strategy
1. **Baseline randomization diagnostics** using standardized mean differences.
2. **Training-motivation model** examining organizational justice, locus of control, self-efficacy, and gender.
3. **Training-receptivity model** examining motivation, organizational justice, supervisor support, implementation fidelity, and organizational-justice × gender moderation.
4. **Longitudinal GEE / DiD-style model** for scenario skill across baseline, post-training, and follow-up.
5. **Temporal pathway model** linking baseline motivation and organizational justice to post-training receptivity and six-month skill, plus 1,000-replicate nonparametric bootstrap indirect effects. These are temporal statistical pathways, not causal mediation claims.
6. **Scenario-transfer GEE** for repeated behavioral-health scenarios.
7. **Problem-oriented diagnostic concentration analysis** asking whether synthetic low performance (pre-specified demonstration threshold: score < 70) is concentrated by cohort, unit, or behavior/scenario rather than assuming an agency-wide mechanism. The threshold is illustrative, not a validated operational cut-point.
8. **Implementation-fidelity analysis** linking cohort fidelity, receptivity, and later skill.

## Qualitative strategy
Synthetic implementation interviews are coded with a transparent dictionary covering leadership support, goal clarity, workload barriers, peer norms, practical relevance, and implementation friction. The purpose is to demonstrate auditable mixed-method integration, not automated interpretation of real interview data.

## Methodological grounding
The architecture is informed by several strands of police research:
- Wolfe et al.'s theory of police training motivation and receptivity, in which motivation precedes receptivity and supervisor organizational justice can shape perceived skill acquisition.
- Recent longitudinal work with newly recruited Korean police officers examining motivation, receptivity, training outcomes, organizational justice, and gender heterogeneity.
- Experimental evaluation of an internal traffic-stop dashboard using group randomization, difference-in-differences logic, administrative data, and qualitative implementation interviews.
- Problem-oriented diagnostic work that moves beyond detecting a disparity toward locating whether a problem is diffuse or concentrated at organizational, individual, ecological, or behavioral levels before selecting an intervention.

## Boundaries
All coefficients, people, agencies, interviews, and outcomes are synthetic. The project does not estimate the effect of any real training program and must not be used to characterize any real police agency or demographic group.

## References used to ground the methodological design
- Nam, Y., Wolfe, S. E., & Kim, Y. S. (2026). *Toward a Comprehensive Model of Police Training: A Longitudinal Study Examining Predictors of Officers’ Training Motivation, Receptivity, and Outcomes*. Justice Quarterly, 43(4), 952–978. https://doi.org/10.1080/07418825.2025.2585859
- Nam, Y., Wolfe, S. E., & Kim, Y. S. (2026). *Gendered responses to fairness: Organizational justice and police training receptivity*. Journal of Criminal Justice, 105, 102693. https://doi.org/10.1016/j.jcrimjus.2026.102693
- Knode, J. L., Carter, T. M., & Wolfe, S. E. (2026). *Beyond Identification: A Problem-Oriented Approach to Diagnosing Racial Disparities in Policing*. Journal of Quantitative Criminology, 42, 61–90. https://doi.org/10.1007/s10940-025-09618-6
- Carter, T., Wolfe, S. E., Knode, J., & Henry, G. (2024). *Attempting to reduce traffic stop racial disparities: An experimental evaluation of an internal dashboard intervention*. Criminology & Public Policy, 23, 543–568. https://doi.org/10.1111/1745-9133.12664
- Wolfe, S. E., McLean, K., Rojek, J., Alpert, G. P., & Smith, M. R. (2022). *Advancing a Theory of Police Officer Training Motivation and Receptivity*. Justice Quarterly, 39(1), 201–223. https://doi.org/10.1080/07418825.2019.1703027
