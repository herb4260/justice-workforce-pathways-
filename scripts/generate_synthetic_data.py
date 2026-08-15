from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; SEED=20260816
clip=lambda x:np.clip(x,1,7); logistic=lambda x:1/(1+np.exp(-x))
def generate(seed=SEED,n=420,n_fac=28):
 r=np.random.default_rng(seed); fac=r.integers(1,n_fac+1,n); fs=r.normal(0,.35,n_fac+1); trait=r.normal(0,.55,n); st=r.normal(0,.45,n); active=np.ones(n,bool); rows=[]; pdist=clip(r.normal(3,.7,n)); pstig=clip(r.normal(3.7,.75,n))
 for w,m in enumerate([0,12,24,36],1):
  t=w-1; org=clip(3.55+.5*fs[fac]+.35*trait+.25*t+r.normal(0,.55,n)); acute=r.poisson(.55+.16*t+.1*np.maximum(trait,0),n); sup=clip(4.55+.55*st-.18*fs[fac]+r.normal(0,.55,n)); peer=clip(4.75+.4*st+r.normal(0,.5,n)); stigma=clip(3.75+.28*org-.26*sup-.15*peer+.18*pstig+r.normal(0,.55,n)); distress=clip(2.25+.34*pdist+.30*org+.17*acute-.24*sup-.12*peer-.015*org*sup+.28*trait+r.normal(0,.55,n)); burnout=clip(1.55+.5*distress+.25*org-.16*sup+r.normal(0,.48,n)); ptsd=clip(1.45+.34*distress+.28*acute+.08*org+r.normal(0,.58,n)); hs=r.binomial(1,logistic(-1.5+.34*distress-.30*stigma+.20*sup+.12*peer)); si=r.binomial(1,logistic(-4.3+.52*distress+.16*burnout+.12*ptsd)); overtime=np.maximum(0,r.normal(16+5*org+3*acute,8,n)).round(1); sick=r.poisson(np.maximum(.2,.35+.28*distress+.1*burnout)); crit=r.poisson(.3+.2*acute); turn=np.zeros(n,int)
  if w>1: turn=((r.random(n)<logistic(-4.20+.28*org+.20*burnout-.22*sup+.08*t))&active).astype(int)
  for i in np.where(active)[0]: rows.append([f'JWP{i+1:04d}',f'F{fac[i]:02d}',w,m,acute[i],org[i],sup[i],peer[i],stigma[i],distress[i],burnout[i],ptsd[i],si[i],hs[i],overtime[i],sick[i],crit[i],turn[i]])
  active &= turn==0
  if w<4: active &= ~(r.random(n)<(.025+.01*t))
  pdist,pstig=distress,stigma
 cols='person_id facility_id wave months acute_exposure org_stress supervisor_support peer_support stigma distress burnout ptsd suicidal_ideation help_seeking overtime_hours sick_days critical_incidents turnover_event'.split(); return pd.DataFrame(rows,columns=cols)
def interviews(df,seed=SEED):
 r=np.random.default_rng(seed+9); themes={'stigma':'People say support exists, but I still worry that asking for help changes how coworkers see me.','organizational_distrust':'Policies can feel unpredictable from one supervisor to another.','supervisor_support':'My supervisor checks in after difficult incidents and makes it easier to speak up early.','peer_support':'The people on my shift understand the work, and talking with them helps me reset.','workload':'Overtime and short staffing make it hard to recover before the next shift.','critical_incident':'Some incidents stay with you after the shift ends.','help_seeking_access':'Confidential and clear services make help feel more realistic.'}; keys=list(themes); s=df[df.wave.isin([2,4])].sample(120,random_state=seed); out=[]
 for _,x in s.iterrows():
  p=np.array([x.stigma,x.org_stress,x.supervisor_support,x.peer_support,x.org_stress,min(7,2*x.acute_exposure+1),8-x.stigma]); p=p/p.sum(); ch=[keys[j] for j in r.choice(7,2,False,p=p)]; out.append({'person_id':x.person_id,'wave':int(x.wave),'excerpt':' '.join(themes[k] for k in ch),'themes':'|'.join(ch)})
 return pd.DataFrame(out)
