import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
from babel.numbers import format_decimal
from utils.formatting import fnum


mpl.rcParams['figure.dpi']= 300

def _set_sns():
    sns.set_theme('talk')
    sns.set_style("whitegrid")
    
def _reset_sns():
    sns.reset_orig()
    mpl.rc_file_defaults()
    mpl.rcParams['figure.dpi'] = 300
    

def pie_for_pct(pct, labels, fileoutpath, title=None, subtitle=None, colors=['yellowgreen', 'lightcoral'], decimals=2):
    _set_sns()

    if len(labels) != 2:
        raise SystemExit('len labels != 2, please provide exactly two labels')
    
    formatpiechart = lambda x: f"{fnum(x, decimals)}%"

    data = {
        labels[0]: pct,
        labels[1]: 100.0 - pct,
    }

    fig, ax = plt.subplots(figsize=[10,6])
    labels = data.keys()
    fig.set_facecolor('white')
    plt.pie(x=data.values(), autopct=formatpiechart, explode=[0.01, 0.01], colors=colors, labels=labels, pctdistance=0.5, startangle=-270, counterclock=False)

    if title:
        mid = (fig.subplotpars.right + fig.subplotpars.left)/2
        plt.suptitle(title, x=mid, fontsize=16)

    if subtitle:
        if len(subtitle.splitlines()) == 2:
            ax.set_title(subtitle, fontsize=12, y=0.98)
        else:
            ax.set_title(subtitle, fontsize=12)

    
    fig.savefig(fileoutpath, bbox_inches='tight')

    # reset back to defaults
    _reset_sns()
    
