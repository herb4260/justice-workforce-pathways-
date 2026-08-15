from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; DEMO=ROOT/'data'/'demo'; RES=ROOT/'results'; FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)

def save(fig,name):
    fig.tight_layout(); fig.savefig(FIG/name,format='svg',bbox_inches='tight'); plt.close(fig)

def run():
    p=pd.read_csv(DEMO/'officer_panel.csv'); s=pd.read_csv(DEMO/'scenario_events.csv'); q=pd.read_csv(RES/'09_qualitative_themes.csv')
    # 1 conceptual design
    fig,ax=plt.subplots(figsize=(10,5.2)); ax.axis('off')
    boxes=[(.05,.68,'Organizational justice\n+ supervisor fairness'),(.36,.68,'Training motivation'),(.64,.68,'Receptivity\nsatisfaction + skill'),(.64,.25,'Follow-up outcomes\nscenario performance'),(.36,.25,'Implementation fidelity\n+ peer/workload context'),(.05,.25,'Diagnostic levels\nunit • officer • behavior')]
    for x,y,t in boxes:
        ax.text(x,y,t,transform=ax.transAxes,ha='left',va='center',fontsize=12,bbox=dict(boxstyle='round,pad=.55',fc='white',ec='0.45'))
    arrows=[((.27,.68),(.35,.68)),((.54,.68),(.63,.68)),((.75,.61),(.75,.37)),((.57,.31),(.65,.31)),((.27,.31),(.35,.31))]
    for a,b in arrows: ax.annotate('',xy=b,xytext=a,xycoords='axes fraction',arrowprops=dict(arrowstyle='->',lw=1.5))
    ax.set_title('Training Justice Diagnostics — synthetic study architecture',fontsize=16,pad=14); save(fig,'01_study_architecture.svg')
    # 2 trajectories
    g=p.groupby(['wave','treatment']).scenario_skill.mean().unstack()
    fig,ax=plt.subplots(figsize=(8,5)); ax.plot([0,1,2],g[0],marker='o',label='Control'); ax.plot([0,1,2],g[1],marker='o',label='Training'); ax.set_xticks([0,1,2],['Baseline','Post','6-month']); ax.set_ylabel('Mean scenario skill'); ax.set_title('Synthetic training-effect trajectory'); ax.legend(); save(fig,'02_training_trajectories.svg')
    # 3 org justice x gender receptivity
    d=p[(p.wave==1)&(p.treatment==1)].dropna(subset=['receptivity']).copy(); fig,ax=plt.subplots(figsize=(8,5))
    for gender,grp in d.groupby('gender'):
        co=np.polyfit(grp.org_justice,grp.receptivity,1); xs=np.linspace(grp.org_justice.min(),grp.org_justice.max(),100); ax.scatter(grp.org_justice,grp.receptivity,alpha=.15,s=15); ax.plot(xs,np.polyval(co,xs),label=gender)
    ax.set_xlabel('Organizational justice'); ax.set_ylabel('Training receptivity'); ax.set_title('Fairness and receptivity by gender (synthetic)'); ax.legend(); save(fig,'03_justice_gender_receptivity.svg')
    # 4 fidelity-outcome
    u=p[(p.wave==2)&(p.treatment==1)].groupby('cohort_id').agg(fidelity=('implementation_fidelity','mean'),skill=('scenario_skill','mean')).reset_index(); fig,ax=plt.subplots(figsize=(8,5)); ax.scatter(u.fidelity,u.skill,s=45); co=np.polyfit(u.fidelity,u.skill,1); xs=np.linspace(u.fidelity.min(),u.fidelity.max(),100); ax.plot(xs,np.polyval(co,xs)); ax.set_xlabel('Implementation fidelity'); ax.set_ylabel('6-month skill'); ax.set_title('Implementation fidelity and transfer'); save(fig,'04_fidelity_transfer.svg')
    # 5 diagnostic concentration
    diag=pd.read_csv(RES/'07_diagnostic_concentration.csv'); c=diag[diag.level=='cohort_id'].copy(); c['case']=c['case'].astype(int).astype(str); c=c.sort_values('rate',ascending=False); fig,ax=plt.subplots(figsize=(9,5)); ax.bar(c['case'],c['rate']); ax.set_xlabel('Training cohort'); ax.set_ylabel('Low-performance rate'); ax.set_title('Diagnostic concentration across cohorts'); ax.tick_params(axis='x',rotation=90); save(fig,'05_diagnostic_concentration.svg')
    # 6 themes
    fig,ax=plt.subplots(figsize=(8,5)); qq=q.sort_values('share'); ax.barh(qq.theme,qq.share); ax.set_xlabel('Share of synthetic interviews coded'); ax.set_title('Implementation themes'); save(fig,'06_implementation_themes.svg')
    # 7 scenario transfer
    sc=s.groupby(['scenario','treatment']).performance_score.mean().unstack(); fig,ax=plt.subplots(figsize=(9,5)); sc.plot(kind='bar',ax=ax); ax.set_ylabel('Mean performance'); ax.set_title('Training transfer across behavioral-health scenarios'); ax.legend(['Control','Training']); ax.tick_params(axis='x',rotation=20); save(fig,'07_scenario_transfer.svg')
    # 8 bootstrapped temporal indirect effects
    med=pd.read_csv(RES/'05b_bootstrap_indirect_effects.csv'); fig,ax=plt.subplots(figsize=(8,4.5)); y=np.arange(len(med)); xerr=np.vstack([med.estimate-med.boot_ci_low,med.boot_ci_high-med.estimate]); ax.errorbar(med.estimate,y,xerr=xerr,fmt='o',capsize=5); ax.axvline(0,linewidth=1); ax.set_yticks(y,['Motivation → receptivity → transfer','Justice → receptivity → transfer']); ax.set_xlabel('Synthetic indirect effect (95% bootstrap CI)'); ax.set_title('Temporal pathway estimates'); save(fig,'08_bootstrap_pathways.svg')
    return list(FIG.glob('*.svg'))
if __name__=='__main__': print('Figures:',len(run()))
