import pandas as pd
import sklearn.metrics as metrics
import json
import numpy as np


df_nl = pd.read_csv('https://covid-analytics.nl/daily-vaccine-rollout.csv', index_col=0)
df_nl.index = pd.to_datetime(df_nl.index)
df_nl.sort_index(inplace=True)

df_ensemble = pd.read_csv('data/ensemble.csv', index_col=0)
df_ensemble.index = pd.to_datetime(df_ensemble.index)

df_divbytwo = (df_nl['total_vaccinations'] / 2).rename('people_fully_vaccinated').to_frame()
df_divbytwo['people_vaccinated'] = df_divbytwo['people_fully_vaccinated']
df_divbytwo.index = pd.to_datetime(df_divbytwo.index)

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

df_gt = df_nl['people_fully_vaccinated'].dropna().astype(int).to_frame()

results = {}

col = 'people_fully_vaccinated'
intersect = set(df_gt[col].index) & set(df_ensemble[col].index)
overall_intersect = intersect.copy()
results['ensemble'] = regression_results(df_gt[col].loc[intersect].values.astype(int), df_ensemble[col].loc[intersect].astype(int))
results['ensemble']['count_datapoints'] = len(intersect)

intersect = set(df_gt[col].index) & set(df_divbytwo[col].index)
overall_intersect = intersect.copy()
results['divide by two'] = regression_results(df_gt[col].loc[intersect].values.astype(int), df_divbytwo[col].loc[intersect].astype(int))
results['divide by two']['count_datapoints'] = len(intersect)

df_metrics = pd.DataFrame(results)
df_metrics.T.to_csv('data/comparison-ensemble-vs-divbytwo.csv')

df_merged = df_nl['people_fully_vaccinated'].rename('RIVM/LNAZ (real)').to_frame()
df_merged = df_merged.join(df_ensemble['people_fully_vaccinated'].rename('ensemble (estimate)'), how='outer')
df_merged = df_merged.join(df_divbytwo['people_fully_vaccinated'].rename('divide by two (estimate)'), how='outer')

df_merged.sort_index(inplace=True)
df_merged = df_merged[df_merged.index >= df_ensemble.index[0]]
ax = df_merged.plot(style=['o', '-', '-'], grid=True)
ax.set_title('Fully vaccinated ensemble vs. divide-by-two strategy')

fig = ax.get_figure()
fig.tight_layout()
fig.savefig('data/comparison-ensemble-vs-divbytwo.png', dpi=300)
