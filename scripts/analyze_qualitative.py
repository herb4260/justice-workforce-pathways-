import pandas as pd
def run(i,p):
 rows=[{'person_id':r.person_id,'wave':r.wave,'theme':t} for _,r in i.iterrows() for t in r.themes.split('|')]; c=pd.DataFrame(rows); f=c.groupby('theme').size().rename('mentions').reset_index(); j=c.merge(p[['person_id','wave','distress','help_seeking','org_stress','supervisor_support']],on=['person_id','wave']).groupby('theme').agg(mentions=('theme','size'),mean_distress=('distress','mean'),help_seeking_rate=('help_seeking','mean'),mean_org_stress=('org_stress','mean'),mean_supervisor_support=('supervisor_support','mean')).reset_index(); return c,f,j
