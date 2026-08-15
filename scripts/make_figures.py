from pathlib import Path
import pandas as pd,matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def save(fig,n): fig.tight_layout(); fig.savefig(ROOT/'figures'/n,format='svg',bbox_inches='tight'); plt.close(fig)
def run(df,j):
 (ROOT/'figures').mkdir(exist_ok=True)
 fig,ax=plt.subplots(figsize=(10,4)); ax.axis('off'); labels=[(.03,'Acute exposure'),(.27,'Organizational stress'),(.52,'Support & stigma'),(.76,'Mental health'),(.76,'Help-seeking & retention')]; ys=[.6,.6,.6,.6,.2]
 for (x,t),y in zip(labels,ys): ax.text(x,y,t,transform=ax.transAxes,bbox=dict(boxstyle='round,pad=.5',fc='white'))
 ax.set_title('Justice Workforce Pathways — synthetic longitudinal mixed-methods design'); save(fig,'01_study_design.svg')
 m=df.groupby('wave')[['org_stress','distress','burnout','supervisor_support']].mean(); fig,ax=plt.subplots(figsize=(8,5)); [ax.plot(m.index,m[c],marker='o',label=c.replace('_',' ').title()) for c in m]; ax.set_xticks([1,2,3,4],['T1','T2','T3','T4']); ax.set_ylim(1,7); ax.legend(frameon=False); ax.set_title('Synthetic 4-wave trajectories'); save(fig,'02_longitudinal_trajectories.svg')
 q=pd.qcut(df.supervisor_support,3,labels=['Lower support','Middle support','Higher support']); tmp=df.assign(g=q,b=pd.qcut(df.org_stress,5,duplicates='drop')).groupby(['g','b'],observed=True).agg(stress=('org_stress','mean'),distress=('distress','mean')).reset_index(); fig,ax=plt.subplots(figsize=(8,5)); [ax.plot(d.stress,d.distress,marker='o',label=str(g)) for g,d in tmp.groupby('g',observed=True)]; ax.legend(frameon=False); ax.set_title('Synthetic stress × supervisor support pattern'); save(fig,'03_stress_support_interaction.svg')
 fig,ax=plt.subplots(figsize=(8,5)); jj=j.sort_values('mentions'); ax.barh(jj.theme.str.replace('_',' '),jj.mentions); ax.set_title('Synthetic interview themes'); save(fig,'04_qualitative_themes.svg')
 total=df.person_id.nunique(); ex=df[df.turnover_event==1].groupby('wave').person_id.nunique(); rem=total; surv=[]
 for w in [1,2,3,4]: rem-=int(ex.get(w,0)); surv.append(rem/total)
 fig,ax=plt.subplots(figsize=(8,5)); ax.step([0,12,24,36],surv,where='post'); ax.scatter([0,12,24,36],surv); ax.set_ylim(0,1.02); ax.set_title('Synthetic workforce retention'); save(fig,'05_retention_curve.svg')
