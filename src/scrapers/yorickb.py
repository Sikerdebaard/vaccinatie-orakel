from github import Github
import pandas as pd
from pathlib import Path


g = Github()
r = g.get_repo("YorickBleijenberg/COVID_data_RIVM_Netherlands")
csvfiles = [csvfile.name for csvfile in r.get_contents("vaccination/daily-dashboard-update")]
csvfiles = list(sorted(csvfiles))

baseurl = 'https://raw.githubusercontent.com/YorickBleijenberg/COVID_data_RIVM_Netherlands/master/vaccination/daily-dashboard-update/'

cols = ['people_vaccinated', 'people_fully_vaccinated']

outdir = Path('data/models')
outfile = outdir / 'yorickb.csv'

if outfile.exists():
    df_estimates = pd.read_csv(outfile, index_col=0)
    df_estimates.index = pd.to_datetime(df_estimates.index)
    
    print(f'Loaded {outfile}')
else:
    df_estimates = pd.DataFrame(index=pd.to_datetime([]))
    
for csvfile in csvfiles:
    if 'vaccine-data' not in csvfile:
        print('Skipping', csvfile)
        continue
        
    print(csvfile)

    df = pd.read_csv(f'{baseurl}{csvfile}', index_col=0)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    idx = df.index[-1]
    row = df.loc[idx][cols]

    if idx not in df_estimates.index or idx.date() == pd.to_datetime('today').date():
        print(f'Updating {idx}')
        for col in cols:
            df_estimates.at[idx, col] = row[col]


df_estimates['total_vaccinations'] = df_estimates.sum(axis=1)

df_estimates = df_estimates.astype(pd.Int64Dtype())

df_estimates.sort_index(inplace=True)
df_estimates.index.rename('date', inplace=True)

df_estimates.to_csv(outfile)
