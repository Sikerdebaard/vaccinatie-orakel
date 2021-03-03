from github import Github
import pandas as pd
from pathlib import Path


g = Github()
r = g.get_repo("YorickBleijenberg/COVID_data_RIVM_Netherlands")
csvfiles = [csvfile.name for csvfile in r.get_contents("vaccination/daily-dashboard-update")]

baseurl = 'https://raw.githubusercontent.com/YorickBleijenberg/COVID_data_RIVM_Netherlands/master/vaccination/daily-dashboard-update/'

cols = ['people_vaccinated', 'people_fully_vaccinated']
df_estimates = pd.DataFrame(index=pd.to_datetime([]))
for csvfile in csvfiles:
    if 'vaccine-data' not in csvfile:
        print('Skipping', csvfile)
        continue
        
    df = pd.read_csv(f'{baseurl}{csvfile}', index_col=0)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    
    idx = df.index[-1]
    row = df.loc[idx][cols]
    
    for col in cols:
        df_estimates.at[idx, col] = row[col]
        
df_estimates = df_estimates.sort_index().resample('D').last()

df_estimates['total_vaccinations'] = df_estimates.sum(axis=1)
df_estimates = df_estimates.astype(pd.Int64Dtype())
df_estimates.index = df_estimates.index - pd.Timedelta(days=1)

outdir = Path('data/models')
outfile = outdir / 'yorickb.csv'

if outfile.exists():
    df_org = pd.read_csv(outfile, index_col=0)
    df_org.index = pd.to_datetime(df_org.index)

    for idx, row in df_estimates.iterrows():
        df_org.loc[idx] = row

    df_estimates = df_org.astype(pd.Int64Dtype())

df_estimates.sort_index(inplace=True)
df_estimates.index.rename('date', inplace=True)
df_estimates.to_csv(outfile)
