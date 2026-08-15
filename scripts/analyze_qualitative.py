from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DEMO=ROOT/'data'/'demo'; RES=ROOT/'results'; RES.mkdir(exist_ok=True)
KEYWORDS={
'leadership_support':['supervisor backed','leaders reinforced','supervisor follow-up'],
'goal_clarity':['goals were clear','success looked like','expectations were specific'],
'workload_barrier':['staffing made','calls were too heavy','overtime reduced'],
'peer_norms':['peers encouraged','squad culture','coworkers took'],
'practical_relevance':['scenarios felt','skills fit','examples matched'],
'implementation_friction':['no time to reinforce','message changed','follow-up was inconsistent']}

def run(interviews=None):
    x=pd.read_csv(DEMO/'implementation_interviews.csv') if interviews is None else interviews.copy()
    for theme,keys in KEYWORDS.items():
        x[theme]=x.excerpt.str.lower().apply(lambda t:int(any(k in t for k in keys)))
    counts=x[list(KEYWORDS)].sum().sort_values(ascending=False).rename_axis('theme').reset_index(name='count')
    counts['share']=counts['count']/len(x); counts.to_csv(RES/'09_qualitative_themes.csv',index=False)
    coded=x[['interview_id','person_id','wave','cohort_id','excerpt']+list(KEYWORDS)]
    coded.to_csv(RES/'10_coded_interviews.csv',index=False)
    return counts,coded
if __name__=='__main__':
    c,_=run(); print(c.to_string(index=False))
