import pandas as pd
import argparse

def main(model, outfile, title=None, subtitle=None):
    df_estimates = pd.read_csv(model, index_col=0)
    df_estimates.index = pd.to_datetime(df_estimates.index)

    cols = ['people_vaccinated', 'people_fully_vaccinated', 'total_vaccinations']
    df_estimates = df_estimates[cols]
    
    ax = df_estimates.plot()
    if title:
        ax.set_title(title)

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(outfile, dpi=300)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots a model')

    parser.add_argument('--model', required=True, help='Model CSV input')
    parser.add_argument('--outfile', required=True, help='Output image file')

    parser.add_argument('--title', required=False, default=None, help='Chart title.')
    #parser.add_argument('--subtitle', required=False, default=None, help='Chart subtitle.')

    args = parser.parse_args()
    main(**vars(args))
