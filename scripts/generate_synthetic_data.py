from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / 'data' / 'demo'
SEED = 4260
N = 480
N_COHORTS = 24
WAVES = [0, 1, 2]
SCENARIOS = ['suicidal_crisis', 'psychosis', 'youth_behavioral_health', 'cognitive_disability']
THEMES = {
    'leadership_support': ['supervisor backed the training', 'leaders reinforced the skills', 'supervisor follow-up helped'],
    'goal_clarity': ['goals were clear', 'we understood what success looked like', 'expectations were specific'],
    'workload_barrier': ['staffing made practice difficult', 'calls were too heavy', 'overtime reduced practice time'],
    'peer_norms': ['peers encouraged the approach', 'squad culture supported it', 'coworkers took it seriously'],
    'practical_relevance': ['scenarios felt realistic', 'skills fit actual calls', 'examples matched field work'],
    'implementation_friction': ['no time to reinforce it', 'the message changed by supervisor', 'follow-up was inconsistent'],
}

def clip(x, lo, hi):
    return np.minimum(np.maximum(x, lo), hi)

def logistic(x):
    return 1/(1+np.exp(-x))

def generate(seed: int = SEED, out_dir: Path | None = None):
    rng = np.random.default_rng(seed)
    out_dir = Path(out_dir or DEMO)
    out_dir.mkdir(parents=True, exist_ok=True)

    cohort_ids = np.repeat(np.arange(1, N_COHORTS+1), N//N_COHORTS)
    rng.shuffle(cohort_ids)
    unit_map = {c: 1 + (c-1)//3 for c in range(1, N_COHORTS+1)}
    cohort_justice = {c: float(rng.normal(0, .35)) for c in range(1,N_COHORTS+1)}
    # Pair-matched cluster randomization: adjacent cohorts on baseline justice tendency are paired,
    # then one cohort per pair is randomized to training. This improves demonstration-seed balance
    # without forcing individual-level equality.
    ordered = sorted(cohort_justice, key=cohort_justice.get)
    treatment_cohorts=set()
    for j in range(0, N_COHORTS, 2):
        pair=ordered[j:j+2]; treatment_cohorts.add(int(rng.choice(pair)))
    cohort_fidelity = {c: float(clip(rng.normal(0.78, 0.10), 0.50, 0.98)) if c in treatment_cohorts else 0.0 for c in range(1,N_COHORTS+1)}

    base = pd.DataFrame({'person_id': np.arange(1,N+1), 'cohort_id': cohort_ids})
    base['unit_id'] = base.cohort_id.map(unit_map)
    base['treatment'] = base.cohort_id.isin(treatment_cohorts).astype(int)
    base['gender'] = rng.choice(['man','woman'], size=N, p=[.67,.33])
    base['age'] = np.clip(np.rint(rng.normal(27.4, 3.6, N)), 22, 42).astype(int)
    base['prior_public_safety'] = rng.binomial(1, .18, N)
    base['internal_locus'] = clip(rng.normal(4.6, .85, N), 1, 7)
    base['self_efficacy'] = clip(rng.normal(4.8, .8, N), 1, 7)
    person_trait = rng.normal(0, .45, N)
    base['org_justice_t0'] = clip(4.45 + base.cohort_id.map(cohort_justice).to_numpy() + .25*person_trait + rng.normal(0,.65,N), 1, 7)
    base['supervisor_support_t0'] = clip(4.55 + .48*(base.org_justice_t0-4.5) + rng.normal(0,.65,N), 1, 7)
    female = (base.gender=='woman').astype(float)
    base['training_motivation_t0'] = clip(1.45 + .28*base.org_justice_t0 + .25*base.internal_locus + .20*base.self_efficacy + .22*female + rng.normal(0,.60,N), 1, 7)
    base['baseline_skill'] = clip(58 + 3.2*base.self_efficacy + 1.3*base.prior_public_safety + rng.normal(0,6,N), 35, 90)
    base['baseline_confidence'] = clip(2.2 + .48*base.self_efficacy + rng.normal(0,.6,N), 1, 7)
    base['baseline_distress'] = clip(3.0 - .18*base.org_justice_t0 + rng.normal(0,.7,N), 1, 7)

    panel_rows=[]
    retained = np.ones(N, dtype=bool)
    post_receptivity = {}
    for wave in WAVES:
        if wave==0:
            active = np.ones(N,dtype=bool)
        elif wave==1:
            dropout_p = logistic(-4.2 + .24*base.baseline_distress - .16*base.org_justice_t0)
            retained = retained & (rng.random(N) > dropout_p)
            active = retained.copy()
        else:
            dropout_p = logistic(-4.0 + .26*base.baseline_distress - .14*base.org_justice_t0)
            retained = retained & (rng.random(N) > dropout_p)
            active = retained.copy()
        for i,row in base[active].iterrows():
            treated_now = row.treatment==1 and wave>0
            fidelity = cohort_fidelity[int(row.cohort_id)] if treated_now else 0.0
            orgj = clip(row.org_justice_t0 + .08*wave + .10*treated_now*fidelity + rng.normal(0,.36),1,7)
            sups = clip(row.supervisor_support_t0 + .10*wave + .12*treated_now*fidelity + rng.normal(0,.38),1,7)
            overtime = max(0, rng.normal(15 + 3.2*wave + 2.0*(row.baseline_distress-2.5), 5.5))
            critical = rng.poisson(max(.2, 1.0 + .4*wave))
            base_growth = 1.7*wave
            treatment_gain = treated_now * fidelity * (8.0 if wave==1 else 10.0)
            transfer_from_receptivity = 0.0 if wave < 2 else 2.1*(post_receptivity.get(int(row.person_id), 5.0)-5.0)
            skill = clip(row.baseline_skill + base_growth + treatment_gain + transfer_from_receptivity + 1.0*(orgj-4.5) + rng.normal(0,4.2), 30, 100)
            confidence = clip(row.baseline_confidence + .18*wave + treated_now*fidelity*.75 + .12*(sups-4.5) + rng.normal(0,.38),1,7)
            distress = clip(row.baseline_distress + .08*wave + .08*critical + .025*overtime - .16*(orgj-4.5) - .15*(sups-4.5) + rng.normal(0,.35),1,7)
            if wave==0:
                satisfaction=np.nan; perceived_skill=np.nan; receptivity=np.nan
            else:
                gender_moderation = .13*(orgj-4.5)*(1.0 if row.gender=='man' else .35)
                satisfaction = clip(1.55 + .40*row.training_motivation_t0 + .26*orgj + .30*treated_now*fidelity + gender_moderation + rng.normal(0,.45),1,7)
                perceived_skill = clip(1.35 + .36*row.training_motivation_t0 + .30*orgj + .35*treated_now*fidelity + gender_moderation + rng.normal(0,.45),1,7)
                receptivity=(satisfaction+perceived_skill)/2
                if wave==1 and row.treatment==1:
                    post_receptivity[int(row.person_id)] = float(receptivity)
            help_intent = clip(3.1 + .25*orgj + .20*sups - .20*distress + .10*treated_now*fidelity + rng.normal(0,.48),1,7)
            panel_rows.append({
                'person_id':int(row.person_id),'cohort_id':int(row.cohort_id),'unit_id':int(row.unit_id),'wave':wave,'months':[0,1,6][wave],
                'treatment':int(row.treatment),'trained_now':int(treated_now),'gender':row.gender,'age':int(row.age),'prior_public_safety':int(row.prior_public_safety),
                'internal_locus':row.internal_locus,'self_efficacy':row.self_efficacy,'org_justice':orgj,'supervisor_support':sups,
                'training_motivation':row.training_motivation_t0,'receptivity':receptivity,'training_satisfaction':satisfaction,'perceived_skill_acquisition':perceived_skill,
                'scenario_skill':skill,'behavioral_health_confidence':confidence,'distress':distress,'help_seeking_intent':help_intent,
                'overtime_hours':overtime,'critical_incidents':critical,'implementation_fidelity':fidelity,'synthetic_flag':True
            })
    panel=pd.DataFrame(panel_rows)

    # Scenario-level transfer data at 6-month follow-up.
    t2=panel[panel.wave==2].copy()
    sc_rows=[]
    scenario_difficulty={'suicidal_crisis':-3.0,'psychosis':-1.5,'youth_behavioral_health':-2.2,'cognitive_disability':0.5}
    for _,r in t2.iterrows():
        for scen in SCENARIOS:
            score=clip(r.scenario_skill + scenario_difficulty[scen] + .9*(r.org_justice-4.5) + rng.normal(0,4.5),20,100)
            safe_prob=logistic(-1.3 + .035*(score-60) + .15*(r.supervisor_support-4.5))
            sc_rows.append({'person_id':int(r.person_id),'cohort_id':int(r.cohort_id),'unit_id':int(r.unit_id),'scenario':scen,
                            'performance_score':score,'safe_resolution':int(rng.random()<safe_prob),'treatment':int(r.treatment),
                            'implementation_fidelity':r.implementation_fidelity,'synthetic_flag':True})
    scenarios=pd.DataFrame(sc_rows)

    # Synthetic implementation interviews among treated officers at waves 1/2.
    treated=panel[(panel.treatment==1)&(panel.wave.isin([1,2]))].copy()
    sample_n=min(64,len(treated))
    sample_idx=rng.choice(treated.index,size=sample_n,replace=False)
    interview_rows=[]
    for idx in sample_idx:
        r=treated.loc[idx]
        probs={
            'leadership_support': logistic(-.1 + .55*(r.supervisor_support-4.5)),
            'goal_clarity': logistic(.1 + 1.4*(r.implementation_fidelity-.7)),
            'workload_barrier': logistic(-.5 + .055*(r.overtime_hours-15)),
            'peer_norms': logistic(-.1 + .40*(r.org_justice-4.5)),
            'practical_relevance': logistic(.25 + 1.2*(r.implementation_fidelity-.7)),
            'implementation_friction': logistic(-.4 - 1.1*(r.implementation_fidelity-.7) + .04*(r.overtime_hours-15)),
        }
        chosen=[k for k,p in probs.items() if rng.random()<p]
        if not chosen: chosen=[rng.choice(list(THEMES))]
        excerpt='; '.join(rng.choice(THEMES[k]) for k in chosen[:3]).capitalize()+'.'
        interview_rows.append({'interview_id':f'I{len(interview_rows)+1:03d}','person_id':int(r.person_id),'wave':int(r.wave),
                               'cohort_id':int(r.cohort_id),'excerpt':excerpt,'true_themes':'|'.join(chosen),'synthetic_flag':True})
    interviews=pd.DataFrame(interview_rows)

    panel.to_csv(out_dir/'officer_panel.csv',index=False)
    scenarios.to_csv(out_dir/'scenario_events.csv',index=False)
    interviews.to_csv(out_dir/'implementation_interviews.csv',index=False)
    return panel, scenarios, interviews

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=SEED); ap.add_argument('--out',type=str,default=str(DEMO))
    a=ap.parse_args(); p,s,i=generate(a.seed,Path(a.out)); print(f'Generated {p.person_id.nunique()} officers, {len(p)} panel rows, {len(s)} scenarios, {len(i)} interviews.')
