from __future__ import annotations
import argparse, tempfile, sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generate_synthetic_data import generate
from validate_data import validate
from analyze_quantitative import run

def main(start=501,count=10,bootstrap_reps=50):
    failures=[]
    with tempfile.TemporaryDirectory() as td:
        for seed in range(start,start+count):
            p,s,i=generate(seed,Path(td)); validate(p,s,i,Path(td),check_balance=False)
            try:
                models=run(p,s,bootstrap_reps=bootstrap_reps)
                for name,m in models.items():
                    if not (np.isfinite(m.params).all() and np.isfinite(m.bse).all() and (m.bse<12).all()):
                        failures.append((seed,name,'unstable coefficients/SE'))
            except Exception as e:
                failures.append((seed,'exception',repr(e)))
    assert not failures, failures
    print(f'Model stress test passed for {count} seeds ({start}..{start+count-1}).')
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--start',type=int,default=501); ap.add_argument('--count',type=int,default=10); ap.add_argument('--bootstrap-reps',type=int,default=50); a=ap.parse_args(); main(a.start,a.count,a.bootstrap_reps)
