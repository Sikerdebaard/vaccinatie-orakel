from github import Github
import matplotlib as mpl
import pandas as pd
from pathlib import Path

mpl.rcParams['figure.dpi'] = 300

g = Github()
r = g.get_repo("Sikerdebaard/opencoronastats")

csvfiles = [csvfile.name for csvfile in r.get_contents("data/vaccine_estimate/daily_estimates")]

baseurl = 'https://raw.githubusercontent.com/Sikerdebaard/opencoronastats/master/data/vaccine_estimate/daily_estimates/'

cols = ['vaccinated', 'fully_vaccinated', 'single_dose_vaccinated']
df_estimates = pd.DataFrame(index=pd.to_datetime([]))
for csvfile in csvfiles:
    if 'vaccinated-estimate' not in csvfile:
        print('Skipping', csvfile)
        continue
        
    df = pd.read_csv(f'{baseurl}{csvfile}', index_col=0)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    
    idx = df.index[-1]
    row = df.loc[idx][cols]
    
    for col in cols:
        df_estimates.at[idx, col] = row[col]
        
df_estimates = df_estimates.sort_index().resample('D').last().ffill().round(0)

df_estimates = df_estimates.astype(pd.Int64Dtype())

df_estimates = df_estimates.rename(columns={
    'vaccinated': 'total_vaccinations',
    'fully_vaccinated': 'people_fully_vaccinated',
    'single_dose_vaccinated': 'people_vaccinated',
})


outdir = Path('data/models')
outfile = outdir / 'covid_nl.csv'

if outfile.exists():
    df_org = pd.read_csv(outfile, index_col=0)
    df_org.index = pd.to_datetime(df_org.index)

    for idx, row in df_estimates.iterrows():
        df_org.loc[idx] = row

    df_estimates = df_org.astype(pd.Int64Dtype())

df_estimates.sort_index(inplace=True)
df_estimates.index.rename('date', inplace=True)
df_estimates.to_csv(outfile)

