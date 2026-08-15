from pathlib import Path
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from generate_synthetic_data import generate
from validate_data import validate
from analyze_quantitative import run as quantitative
from analyze_qualitative import run as qualitative
from make_figures import run as make_figures

def test_generation_and_validation(tmp_path):
    p,s,i=generate(4260,tmp_path); assert validate(p,s,i,tmp_path)

def test_reproducible_generation(tmp_path):
    a=tmp_path/'a'; b=tmp_path/'b'; p1,s1,i1=generate(777,a); p2,s2,i2=generate(777,b)
    pd.testing.assert_frame_equal(p1.reset_index(drop=True),p2.reset_index(drop=True)); pd.testing.assert_frame_equal(s1.reset_index(drop=True),s2.reset_index(drop=True))

def test_randomization_balance_and_effect_direction(tmp_path):
    p,s,i=generate(4260,tmp_path); b=p[p.wave==0]; assert abs(b.groupby('treatment').org_justice.mean().diff().iloc[-1])<.45
    f=p[p.wave==2].groupby('treatment').scenario_skill.mean(); assert f.loc[1]>f.loc[0]+3

def test_model_outputs_finite():
    p,s,i=generate(); validate(p,s,i); models=quantitative(p,s,bootstrap_reps=100)
    for m in models.values():
        assert m.params.notna().all(); assert m.bse.notna().all(); assert (m.bse<10).all()

def test_qualitative_coding():
    p,s,i=generate(); counts,coded=qualitative(i); assert counts['count'].sum()>0; assert len(coded)==len(i)

def test_figures_created():
    p,s,i=generate(); validate(p,s,i); quantitative(p,s); qualitative(i); figs=make_figures(); assert len(figs)==8; assert all(f.stat().st_size>500 for f in figs)
