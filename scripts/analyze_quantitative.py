from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.genmod.cov_struct import Exchangeable
from statsmodels.genmod.families import Gaussian
ROOT=Path(__file__).resolve().parents[1]; DEMO=ROOT/'data'/'demo'; RES=ROOT/'results'
RES.mkdir(exist_ok=True)

def tidy(result, model):
    conf=result.conf_int(); out=pd.DataFrame({'term':result.params.index,'estimate':result.params.values,'std_error':result.bse,'p_value':result.pvalues})
    out['ci_low']=conf[0].values; out['ci_high']=conf[1].values; out.insert(0,'model',model); return out

def run(panel=None, scenarios=None, bootstrap_reps=1000):
    panel=pd.read_csv(DEMO/'officer_panel.csv') if panel is None else panel.copy()
    scenarios=pd.read_csv(DEMO/'scenario_events.csv') if scenarios is None else scenarios.copy()
    # Baseline balance
    b=panel[panel.wave==0]
    bal=[]
    for v in ['age','org_justice','supervisor_support','training_motivation','scenario_skill','distress']:
        g=b.groupby('treatment')[v].agg(['mean','std'])
        pooled=np.sqrt((g.loc[0,'std']**2+g.loc[1,'std']**2)/2); smd=(g.loc[1,'mean']-g.loc[0,'mean'])/pooled
        bal.append({'variable':v,'control_mean':g.loc[0,'mean'],'treatment_mean':g.loc[1,'mean'],'smd':smd})
    pd.DataFrame(bal).to_csv(RES/'01_randomization_balance.csv',index=False)

    # Training motivation model at baseline.
    mot=smf.ols('training_motivation ~ org_justice + internal_locus + self_efficacy + C(gender)',data=b).fit(cov_type='HC3')
    tidy(mot,'baseline_training_motivation').to_csv(RES/'02_motivation_model.csv',index=False)

    # Receptivity model among treated post-training, including gender moderation.
    post=panel[(panel.wave==1)&(panel.treatment==1)].copy(); post['man']=(post.gender=='man').astype(int)
    rec=smf.ols('receptivity ~ training_motivation + org_justice*man + supervisor_support + implementation_fidelity',data=post).fit(cov_type='HC3')
    tidy(rec,'post_training_receptivity').to_csv(RES/'03_receptivity_gender_moderation.csv',index=False)

    # Longitudinal GEE skill model (clustered by person), a DiD-style treatment x post/follow-up model.
    panel['post']= (panel.wave>=1).astype(int); panel['followup']=(panel.wave==2).astype(int)
    gee=smf.gee('scenario_skill ~ treatment + post + followup + treatment:post + treatment:followup + org_justice + supervisor_support + overtime_hours + critical_incidents',
                groups='person_id',data=panel,cov_struct=Exchangeable(),family=Gaussian()).fit()
    tidy(gee,'longitudinal_skill_gee').to_csv(RES/'04_longitudinal_training_effect.csv',index=False)

    # Follow-up skill: pathway linking motivation -> receptivity -> outcome, treated group.
    wide=panel.pivot(index='person_id',columns='wave',values=['training_motivation','receptivity','scenario_skill','org_justice','distress'])
    wide.columns=[f'{a}_w{b}' for a,b in wide.columns]; wide=wide.reset_index()
    meta=b[['person_id','treatment','gender','self_efficacy']]
    wide=wide.merge(meta,on='person_id',how='left')
    tw=wide[wide.treatment==1].dropna(subset=['receptivity_w1','scenario_skill_w2'])
    path=smf.ols('scenario_skill_w2 ~ scenario_skill_w0 + training_motivation_w0 + receptivity_w1 + org_justice_w0 + self_efficacy',data=tw).fit(cov_type='HC3')
    tidy(path,'training_pathway_followup_skill').to_csv(RES/'05_training_pathway.csv',index=False)

    # Nonparametric bootstrap indirect effects for the training pathway.
    # This is a temporal statistical pathway in synthetic data, not a causal mediation claim.
    med=tw[['training_motivation_w0','receptivity_w1','scenario_skill_w2','scenario_skill_w0','org_justice_w0','self_efficacy']].dropna().copy()
    a_model=smf.ols('receptivity_w1 ~ training_motivation_w0 + org_justice_w0 + self_efficacy',data=med).fit()
    b_model=smf.ols('scenario_skill_w2 ~ scenario_skill_w0 + training_motivation_w0 + receptivity_w1 + org_justice_w0 + self_efficacy',data=med).fit()
    point={'motivation_via_receptivity':a_model.params['training_motivation_w0']*b_model.params['receptivity_w1'],
           'justice_via_receptivity':a_model.params['org_justice_w0']*b_model.params['receptivity_w1']}
    rng=np.random.default_rng(4260); boot={k:[] for k in point}
    for _ in range(bootstrap_reps):
        samp=med.iloc[rng.integers(0,len(med),len(med))]
        aa=smf.ols('receptivity_w1 ~ training_motivation_w0 + org_justice_w0 + self_efficacy',data=samp).fit()
        bb=smf.ols('scenario_skill_w2 ~ scenario_skill_w0 + training_motivation_w0 + receptivity_w1 + org_justice_w0 + self_efficacy',data=samp).fit()
        boot['motivation_via_receptivity'].append(aa.params['training_motivation_w0']*bb.params['receptivity_w1'])
        boot['justice_via_receptivity'].append(aa.params['org_justice_w0']*bb.params['receptivity_w1'])
    pd.DataFrame([{'path':k,'estimate':point[k],'boot_ci_low':np.quantile(boot[k],.025),'boot_ci_high':np.quantile(boot[k],.975),'bootstrap_reps':bootstrap_reps} for k in point]).to_csv(RES/'05b_bootstrap_indirect_effects.csv',index=False)

    # Scenario-level transfer GEE.
    sc=scenarios.merge(panel[panel.wave==2][['person_id','org_justice','supervisor_support']],on='person_id',how='left')
    transfer=smf.gee('performance_score ~ treatment + C(scenario) + implementation_fidelity + org_justice + supervisor_support',groups='person_id',data=sc,cov_struct=Exchangeable(),family=Gaussian()).fit()
    tidy(transfer,'scenario_transfer_gee').to_csv(RES/'06_scenario_transfer.csv',index=False)

    # Diagnostic concentration: low performance (<70) across levels, inspired by problem-oriented diagnosis.
    sc['low_performance']=(sc.performance_score<70).astype(int)
    rows=[]
    for level in ['cohort_id','unit_id','scenario']:
        g=sc.groupby(level).agg(n=('low_performance','size'),failures=('low_performance','sum'),rate=('low_performance','mean')).reset_index()
        total=g.failures.sum(); g['share_of_failures']=g.failures/total if total else 0
        g=g.sort_values('share_of_failures',ascending=False); g['cum_failure_share']=g.share_of_failures.cumsum(); g['level']=level
        rows.append(g.rename(columns={level:'case'}))
    diag=pd.concat(rows,ignore_index=True); diag.to_csv(RES/'07_diagnostic_concentration.csv',index=False)

    # Implementation fidelity and later transfer among trained officers.
    # Keep person-level variation and use cohort-clustered SE because fidelity is assigned at cohort level.
    u=panel[(panel.wave==2)&(panel.treatment==1)].dropna(subset=['receptivity']).copy()
    imp=smf.ols('scenario_skill ~ implementation_fidelity + receptivity + distress + org_justice',data=u).fit(
        cov_type='cluster', cov_kwds={'groups':u['cohort_id']})
    tidy(imp,'implementation_fidelity_outcome').to_csv(RES/'08_implementation_model.csv',index=False)
    return {'motivation':mot,'receptivity':rec,'gee':gee,'pathway':path,'transfer':transfer,'implementation':imp}

if __name__=='__main__':
    m=run(); print('Quantitative analyses complete:', ', '.join(m))
