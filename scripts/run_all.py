from pathlib import Path
import sys,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts'))
from generate_synthetic_data import generate,interviews
from validate_data import validate
from analyze_quantitative import run as qr
from analyze_qualitative import run as ql
from make_figures import run as figs
def main():
 d=ROOT/'data/generated'; r=ROOT/'results/generated'; d.mkdir(parents=True,exist_ok=True); r.mkdir(parents=True,exist_ok=True); df=generate(); it=interviews(df); s=validate(df); df.to_csv(d/'panel.csv',index=False); it.to_csv(d/'interviews.csv',index=False); qr(df).to_csv(r/'model_estimates.csv',index=False); c,f,j=ql(it,df); f.to_csv(r/'theme_frequencies.csv',index=False); j.to_csv(r/'mixed_methods_joint_display.csv',index=False); figs(df,j); pd.DataFrame([s]).to_json(r/'validation_summary.json',orient='records',indent=2); print('Justice Workforce Pathways completed successfully.',s)
if __name__=='__main__': main()
