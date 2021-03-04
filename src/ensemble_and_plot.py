# In[2]:


import pandas as pd
from pathlib import Path

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

for col in df_merged.columns.get_level_values(0).unique():
    ax = df_merged[col].plot(style='o', figsize=(12,4), grid=True, alpha=.8)
    ax.set_title(col)
    ax.get_figure().savefig(f'data/{col}.png', dpi=300)

df_merged.astype(pd.Int64Dtype())


# In[3]:


df_stats = pd.DataFrame(index=pd.to_datetime([]))

for col in df_merged.columns.get_level_values(0).unique():
    df_calc = df_merged[col].T.describe().T[[f'min', 'max', 'mean']]
    #df_calc.columns = [(col, x) for x in df_calc.columns]
    df_calc.columns = [f'{col}_{x}' if x != 'mean' else f'{col}' for x in df_calc.columns]
    
    df_stats = df_stats.join(df_calc, how='outer')
    
#df_stats.columns = pd.MultiIndex.from_tuples(df_stats.columns)
df_stats = df_stats[sorted(df_stats.columns)]

df_stats = df_stats.round(0).astype(pd.Int64Dtype())
df_stats.index.rename('date', inplace=True)
df_stats.to_csv('data/ensemble.csv')
df_stats


# In[4]:


df_nl = pd.read_csv('https://covid-analytics.nl/daily-vaccine-rollout.csv', index_col=0)
df_nl.index = pd.to_datetime(df_nl.index)
df_nl.sort_index(inplace=True)
df_nl


# In[5]:


# import matplotlib as mpl
# mpl.rcParams['figure.dpi'] = 300

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import numpy as np


def _y_fmt_human(y, pos):
    decades = [1e9, 1e6, 1e3, 1e0, 1e-3, 1e-6, 1e-9]
    suffix = ["G", "M", "k", "", "m", "u", "n"]
    if y == 0:
        return str(0)
    for i, d in enumerate(decades):
        if np.abs(y) >= d:
            val = y / float(d)
            signf = len(str(val).split(".")[1])
            if signf == 0:
                return f'{int(val)} {suffix[i]}'
            else:
                if signf == 1:
                    if str(val).split(".")[1] == "0":
                        return f'{int(val)} {suffix[i]}'
                tx = "{" + "val:.{signf}f".format(signf=signf) + "} {suffix}"
                return tx.format(val=val, suffix=suffix[i])

    return y

def model_to_chart(df_model, df_regionvals, chart_file_out_path, title, subtitle=None, plot_realworld=True, dpi=300):
    ignore = ('min', 'max')
    use_cols = [x for x in df_model.columns if not any([y in x for y in ignore])]
    
    print(use_cols)

    df_filter = df_model.copy()
    cols_filter = [x for x in df_model.columns if 'fully' in x]

    lastidx = None
    for idx, row in df_filter[cols_filter].iterrows():
        if row.sum() == 0:
            lastidx = idx
            df_filter.loc[idx, cols_filter] = None
    df_filter.loc[lastidx, cols_filter] = 0

    df_filter = df_filter.join(df_regionvals['total_vaccinations'])

    if plot_realworld:
        realworldcols = []
        legend = ["Total doses administered (real)", "People fully vaccinated (estimate)", "People vaccinated (estimate)"]
        if 'people_vaccinated' in df_regionvals.columns and df_regionvals['people_vaccinated'].sum() > 0:
            realworldcols.append('people_vaccinated')
            legend.append('people_vaccinated')
        if 'people_fully_vaccinated' in df_regionvals.columns  and df_regionvals['people_fully_vaccinated'].sum() > 0:
            realworldcols.append('people_fully_vaccinated')
            legend.append('People fully vaccinated (real)')

        df_filter = df_filter.join(df_regionvals[realworldcols])
        cols = ['total_vaccinations', *use_cols, *realworldcols]
    else:
        cols = ['total_vaccinations', *use_cols]
        legend = ["Total doses administered (real)", "People fully vaccinated (estimate)", "People vaccinated (estimate)"]

    df_filter.index = df_filter.index.date

    style = ['o'] + (['-'] * 2)
    colors = [
        [.6, .6, .6],
        [0, .7, .1],
        [1, .5, .1],
    ]
    if plot_realworld:
        if 'people_vaccinated' in realworldcols:
            colors.append([1, 0, 0])
            style.append('o')
        if 'people_fully_vaccinated' in realworldcols:
            colors.append([0.66, 0.55, 0.84])
            style.append('o')

    params = dict(
        figsize=(12, 9),
        alpha=.7,
        color=colors,
        grid=True,
        lw=3,
        fontsize=12,
        style=style,
    )

    ax = df_filter[cols].plot(**params)
    ax.legend(legend, loc='upper left')

    fill_colors = {
        'fully_vaccinated': (0, .8, 0),
        'vaccinated': (1, .7, 0),
    }

    for col in use_cols:
        plt.fill_between(df_filter.index, df_filter[f'{col}_min'], df_filter[f'{col}_max'], color=fill_colors[col], alpha=.2)

    ax.set_ylabel(ylabel='Number of people vaccinated (real)')
    ax.yaxis.set_major_formatter(FuncFormatter(_y_fmt_human))
    fig = ax.get_figure()

    ax.set_xticks([])
    ax.set_xticks([], minor=True)

    locator = mdates.AutoDateLocator(minticks=3, maxticks=15)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    if title:
        mid = (fig.subplotpars.right + fig.subplotpars.left) / 2
        plt.suptitle(title, x=mid, y=.95, fontsize=16)

    if subtitle:
        ax.set_title(subtitle, fontsize=12)

    ax.margins(x=0, y=0)
    
    handles, labels = ax.get_legend_handles_labels()
    
    labelsmappings = dict(zip(labels, legend))
    # sort both labels and handles by labels
    labels, handles = zip(*sorted(zip(labels, handles), reverse=True, key=lambda t: labelsmappings[t[0]].split('(')[-1]))
    ax.legend(handles, [labelsmappings[x] for x in labels])


    fig.savefig(chart_file_out_path, dpi=dpi)

    #plt.close()

df_tmp = df_stats.copy()
df_tmp.columns = [x.replace('people_', '') for x in df_tmp.columns]
df_tmp = df_tmp[[x for x in df_tmp.columns if 'total_vaccinations' not in x]]
df_tmp[sorted(df_tmp.columns)]
model_to_chart(df_tmp.astype(float), df_nl, 'data/ensemble.png', 'Ensemble ' + ' '.join(sorted(twitter_users)))
#df_tmp


# In[8]:


import sklearn.metrics as metrics
import json


def regression_results(y_true, y_pred):
    explained_variance = metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error = metrics.mean_absolute_error(y_true, y_pred) 
    mse = metrics.mean_squared_error(y_true, y_pred) 
    mean_squared_log_error = metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error = metrics.median_absolute_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)
    
    result = {
        'explained_variance': round(explained_variance,4),
        'mean_squared_log_error': round(mean_squared_log_error,4),
        'r2': r2,
        'MAE': mean_absolute_error,
        'MSE': mse,
        'RMSE': np.sqrt(mse),
    }
    
    return result

df_gt = df_nl['people_fully_vaccinated'].dropna().astype(int).to_frame()  # ground-truth


statscols = ['people_fully_vaccinated']
results = {}

for col in statscols:
    if col not in results:
        results[col] = {}
        
    intersect = set(df_gt[col].index) & set(df_stats[col].index)
    results[col]['ensemble'] = regression_results(df_gt[col].loc[intersect].values.astype(int), df_stats[col].loc[intersect].astype(int))
    results[col]['ensemble']['count_datapoints'] = len(intersect)
    
    for model in df_merged[col].columns:
        df_tmp = df_merged[col, model].dropna()
        intersect = set(df_gt[col].index) & set(df_tmp.index)
        results[col][model] = regression_results(df_gt[col].loc[intersect].values.astype(int), df_tmp.loc[intersect].astype(int))
        results[col][model]['count_datapoints'] = len(intersect)
    
df_metrics = pd.DataFrame(results['people_fully_vaccinated'])
df_metrics.to_csv('data/metrics.csv')

with open('data/metrics.json', 'w') as fh:
    json.dump(results, fh)
    
df_metrics
