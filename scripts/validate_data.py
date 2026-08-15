SCALES=['org_stress','supervisor_support','peer_support','stigma','distress','burnout','ptsd']
def validate(df):
 assert df.person_id.nunique()==420 and set(df.wave)=={1,2,3,4} and not df.duplicated(['person_id','wave']).any(); counts=df.groupby('wave').person_id.nunique(); assert counts.iloc[-1]>=250 and (counts.diff().dropna()<=0).all()
 for c in SCALES: assert df[c].between(1,7).all() and df[c].std()>.35 and (df[c]<=1.25).mean()<.12 and (df[c]>=6.75).mean()<.12,c
 turn=df.groupby('person_id').turnover_event.max().mean(); assert .05<turn<.35 and .01<df.suicidal_ideation.mean()<.4; assert df[['org_stress','distress']].corr().iloc[0,1]>.2 and df[['supervisor_support','distress']].corr().iloc[0,1]<-.1
 return {'n_people':420,'n_rows':len(df),'turnover_rate':float(turn),'wave4_n':int(counts.loc[4])}
