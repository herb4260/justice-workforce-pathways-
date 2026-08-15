from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DEMO=ROOT/'data'/'demo'

def validate(panel=None, scenarios=None, interviews=None, root=DEMO, check_balance=True):
    if panel is None: panel=pd.read_csv(root/'officer_panel.csv')
    if scenarios is None: scenarios=pd.read_csv(root/'scenario_events.csv')
    if interviews is None: interviews=pd.read_csv(root/'implementation_interviews.csv')
    assert panel.person_id.nunique()==480
    assert panel.cohort_id.nunique()==24
    assert set(panel.wave.unique())=={0,1,2}
    assert panel[panel.wave==0].shape[0]==480
    assert panel[panel.wave==2].person_id.nunique()>=390
    assert panel.groupby('person_id').wave.apply(lambda s: list(s)==sorted(s.tolist())).all()
    assert panel[['org_justice','supervisor_support','training_motivation','behavioral_health_confidence','distress','help_seeking_intent']].apply(lambda s:s.between(1,7).all()).all()
    assert panel.scenario_skill.between(20,100).all()
    assert scenarios.performance_score.between(20,100).all()
    assert scenarios.person_id.nunique()==panel[panel.wave==2].person_id.nunique()
    assert scenarios.groupby('person_id').size().eq(4).all()
    assert set(interviews.synthetic_flag.astype(str).str.lower().unique()) <= {'true','1'}
    # Baseline balance is a diagnostic, not a deterministic property of randomization.
    # For the fixed demonstration seed we require reasonable balance; stress tests may skip this chance criterion.
    if check_balance:
        b=panel[panel.wave==0]
        for v in ['age','org_justice','training_motivation']:
            m=b.groupby('treatment')[v].mean()
            assert abs(m.iloc[1]-m.iloc[0]) < (3.0 if v=='age' else .45)
    # No scale collapse or extreme floor/ceiling pile-up.
    for v in ['org_justice','training_motivation','scenario_skill','distress']:
        assert panel[v].std()>.25
    assert (panel.training_motivation >= 6.9).mean() < .10
    assert (panel.training_motivation <= 1.1).mean() < .05
    # Treatment should have a visible but non-deterministic average effect at follow-up.
    f=panel[panel.wave==2].groupby('treatment').scenario_skill.mean()
    assert 3 < (f.loc[1]-f.loc[0]) < 18
    assert 0.05 < scenarios.safe_resolution.mean() < .95
    return True

if __name__=='__main__':
    validate(); print('Data validation passed.')
