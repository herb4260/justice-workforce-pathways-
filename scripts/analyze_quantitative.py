import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def tidy(result, model_name):
    ci = result.conf_int()
    return pd.DataFrame({
        'model': model_name,
        'term': result.params.index,
        'estimate': result.params.values,
        'se': result.bse.values,
        'ci_low': ci[0].values,
        'ci_high': ci[1].values,
        'p_value': result.pvalues.values,
    })


def run(df):
    out = []

    distress = smf.gee(
        'distress ~ I(months/12) + acute_exposure + org_stress * supervisor_support + peer_support + stigma',
        groups='person_id',
        data=df,
        cov_struct=sm.cov_struct.Exchangeable(),
    ).fit()
    out.append(tidy(distress, 'GEE distress'))

    lagged = df.sort_values(['person_id', 'wave']).copy()
    for col in ['distress', 'org_stress', 'acute_exposure', 'supervisor_support', 'stigma']:
        lagged['lag_' + col] = lagged.groupby('person_id')[col].shift()
    lagged = lagged.dropna(subset=['lag_distress'])
    panel = smf.ols(
        'distress ~ lag_distress + lag_org_stress + lag_acute_exposure + lag_supervisor_support + lag_stigma + C(wave)',
        lagged,
    ).fit(cov_type='cluster', cov_kwds={'groups': lagged.person_id})
    out.append(tidy(panel, 'Lagged panel distress'))

    help_seek = smf.gee(
        'help_seeking ~ distress + stigma + supervisor_support + peer_support + C(wave)',
        groups='person_id',
        data=df,
        family=sm.families.Binomial(),
        cov_struct=sm.cov_struct.Exchangeable(),
    ).fit()
    out.append(tidy(help_seek, 'GEE help-seeking'))

    # Wave 1 is entry/baseline and has no turnover risk interval by design.
    # Restricting the hazard model to waves 2–4 avoids structural separation.
    at_risk = df[df.wave > 1].copy()
    turnover = smf.gee(
        'turnover_event ~ I(months/12) + org_stress + burnout + supervisor_support + overtime_hours',
        groups='person_id',
        data=at_risk,
        family=sm.families.Binomial(),
        cov_struct=sm.cov_struct.Independence(),
    ).fit()
    out.append(tidy(turnover, 'Discrete-time turnover'))

    estimates = pd.concat(out, ignore_index=True)
    numeric = estimates[['estimate', 'se', 'ci_low', 'ci_high', 'p_value']]
    assert np.isfinite(numeric).all().all()
    assert (estimates.se >= 0).all()
    assert estimates.se.max() < 10, 'Unstable model detected: excessively large standard error.'
    return estimates
