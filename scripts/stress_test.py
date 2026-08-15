from __future__ import annotations
import argparse, tempfile
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generate_synthetic_data import generate
from validate_data import validate

def main(start=1,count=100):
    effects=[]; ret=[]
    with tempfile.TemporaryDirectory() as td:
        for seed in range(start,start+count):
            p,s,i=generate(seed,Path(td)); validate(p,s,i,Path(td),check_balance=False)
            f=p[p.wave==2].groupby('treatment').scenario_skill.mean(); effects.append(f.loc[1]-f.loc[0]); ret.append(p[p.wave==2].person_id.nunique())
    assert min(effects)>3 and max(effects)<18
    assert min(ret)>=390
    print(f'Stress test passed for seeds {start}..{start+count-1}; effect range {min(effects):.2f}–{max(effects):.2f}.')
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--start',type=int,default=1); ap.add_argument('--count',type=int,default=100); a=ap.parse_args(); main(a.start,a.count)
