import pandas as pd
import requests
import pandas as pd
from pathlib import Path
import matplotlib as mpl

mpl.rcParams['figure.dpi'] = 300


req = requests.get('https://www.corona-lokaal.nl/getvaccines.php')
req.raise_for_status()

data = req.json()['NL']

# format conversion
for k, v in data.items():
    if isinstance(v, dict):
        data[k] = v['value']
    #data[k] = v.replace('.', '').replace(',', '.')
    

cols = ['persons_fully_vaccinated', 'persons_single_dose', 'persons_at_least_one_dose', 'total_doses']
df = pd.DataFrame.from_dict(data, orient='index').T.set_index('date')[cols]
df.index = [x.replace(year=2021) for x in pd.to_datetime(df.index, format='%d/%m')]

df = df.rename(columns={
    'persons_fully_vaccinated': 'people_fully_vaccinated',
    'persons_at_least_one_dose': 'people_vaccinated',
    'total_doses': 'total_vaccinations',
})

df = df.astype(float)
#df['people_vaccinated'] = df[['people_fully_vaccinated', 'persons_single_dose']].sum(axis=1)
df = df.drop(columns=['persons_single_dose'])
#df['total_vaccinations'] = df.sum(axis=1)
df = df.astype(pd.Int64Dtype())
df.index = df.index - pd.Timedelta(days=1)

outdir = Path('data/models')
outfile = outdir / 'kalahiri.csv'

if outfile.exists():
    df_org = pd.read_csv(outfile, index_col=0)
    df_org.index = pd.to_datetime(df_org.index)
    
    for idx, row in df.iterrows():
        df_org.loc[idx] = row
        
    df = df_org.astype(pd.Int64Dtype())

df.sort_index(inplace=True)
df.index.rename('date', inplace=True)
df.to_csv(outfile)
