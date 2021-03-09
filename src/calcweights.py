import pandas as pd

df_metrics = pd.read_csv('data/metrics.csv', index_col=0).round(3)
df_metrics

df_ne_metrics = df_metrics.drop(index='ensemble').copy()

cols_smaller_is_better = ['mean_squared_log_error', 'MAE', 'MSE', 'RMSE']
cols_larger_is_better = ['explained_variance', 'r2']
ignore = ['count_datapoints']

# make sure that all columns are defined
assert all(col in cols_smaller_is_better + cols_larger_is_better + ignore for col in df_ne_metrics.columns)

df_weights = pd.DataFrame(index=df_ne_metrics.index)

# # first smaller is better
# for col in cols_smaller_is_better:
#     df_ne_metrics = df_metrics[col].drop(index='ensemble').to_frame()
#     df_weights[col] = (df_ne_metrics.sum() / df_ne_metrics) / (df_ne_metrics.sum() / df_ne_metrics).sum()
    
# secondly larger is better
for col in cols_larger_is_better:
    df_ne_metrics = df_metrics[col].drop(index='ensemble').to_frame()
    df_weights[col] = df_ne_metrics / df_ne_metrics.sum()

    
df_weights = df_weights.mean(axis=1).rename('weights').to_frame()
assert df_weights['weights'].sum() == 1  # make sure the weights add up to 100%

df_weights.to_csv('data/weights.csv')
