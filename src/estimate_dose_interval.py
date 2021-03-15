import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pathlib import Path


df_nl = pd.read_csv('https://covid-analytics.nl/daily-vaccine-rollout.csv', index_col=0)
df_nl.index = pd.to_datetime(df_nl.index)

df_gt = df_nl['people_fully_vaccinated'].dropna().astype(int).to_frame()

def intervals_for(df_model, df_doses, people_fully_vaccinated='people_fully_vaccinated'):
    intervals = []
    for idx, row in df_model.iterrows():
        doses_administered = row[people_fully_vaccinated]
        closest_matches = (df_doses['total_vaccinations'] - doses_administered).abs().sort_values()
        closest_idx = closest_matches.index[0]
        interval = (idx - closest_idx).days

        intervals += [(idx, interval)]

    df_intervals = pd.DataFrame(intervals, columns=['date', 'interval_days']).set_index('date')
    df_intervals.sort_index(inplace=True)


    return df_intervals

df_rivm_intervals = intervals_for(df_gt, df_nl)

df_ensemble = pd.read_csv('data/ensemble.csv', index_col=0)
df_ensemble.index = pd.to_datetime(df_ensemble.index)

df_ensemble = df_ensemble['people_fully_vaccinated'].rename('ensemble').to_frame()

df_intervals = intervals_for(df_ensemble, df_nl, 'ensemble').rename(columns={'interval_days': 'ensemble / @vaccinorakel'})


df_merged = pd.DataFrame(index=pd.to_datetime([]))
twitter_users = []
for modelfile in Path('data/models').glob('*.csv'):
    twitter_user = f'@{modelfile.stem}'
    twitter_users += [twitter_user]
    df = pd.read_csv(modelfile, index_col=0)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    df.columns = [(x, twitter_user) for x in df.columns]

    df_merged = df_merged.join(df, how='outer')

df_merged.sort_index(inplace=True)
df_merged.columns = pd.MultiIndex.from_tuples(df_merged.columns)
df_merged = df_merged[sorted(df_merged.columns)]

df_merged = df_merged['people_fully_vaccinated']

for col in df_merged.columns:
    df_tmp = intervals_for(df_merged, df_nl, people_fully_vaccinated=col).rename(columns={'interval_days': col})
    df_tmp = df_tmp.loc[df_merged[col].dropna().index]
    df_intervals = df_intervals.join(df_tmp, how='outer')


df_intervals = df_intervals.join(df_rivm_intervals.rename(columns={'interval_days': 'RIVM/LNAZ'}))
df_intervals = df_intervals.resample('D').last()
df_intervals.index.rename('date', inplace=True)
df_intervals = df_intervals.round(0).astype(pd.Int64Dtype())

df_intervals.to_csv('data/estimated_dose_interval.csv')

style = ['-'] * (df_intervals.columns.shape[0] - 1) + ['o']
ax = df_intervals.plot(grid=True, style=style, figsize=(8,4), alpha=.7)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_title('KNN Estimated dose interval')
ax.set_ylabel('days')

fig = ax.get_figure()
fig.tight_layout()
fig.savefig('data/estimated_dose_interval.png', dpi=300)
