import cbsodata
import random
import pandas as pd
from utils.formatting import progressbar
from utils.plotting import pie_for_pct
import requests


def _latest_year_tweet():
    req = requests.get('https://raw.githubusercontent.com/Sikerdebaard/vaccination-booking-slots/main/latest-tweet.json')
    req.raise_for_status()

    tweetid = req.json()['id']

    message = f"""👇👇👇 https://twitter.com/covid_nl/status/{tweetid}"""

    return message

def generate():
    data = cbsodata.get_data('7461bev')
    df = pd.DataFrame(data)

    if df[df['Perioden'] == '2021'].shape[0] == 0:
        df = df[df['Perioden'] == '2020']
    else:
        df = df[df['Perioden'] == '2021']
        
    df = df[df['BurgerlijkeStaat'] == 'Totaal burgerlijke staat']
    df = df[df['Geslacht'] == 'Totaal mannen en vrouwen']
        
    ages = [f'{x} jaar' for x in range(0, 100)] + ['100 jaar of ouder']
    df = df[df['Leeftijd'].isin(ages)]
    df['Leeftijd'] = [int(x.split(' ')[0]) for x in df['Leeftijd'].values]

    popsize = df['Bevolking_1'].sum().astype(int)
    grownups = df[df['Leeftijd'] >= 18]['Bevolking_1'].sum().astype(int)
    children = df[df['Leeftijd'] < 18]['Bevolking_1'].sum().astype(int)

    assert (grownups + children) == popsize

    df_model = pd.read_csv('data/ensemble.csv', index_col=0)
    df_model.index = pd.to_datetime(df_model.index)
    df_model.sort_index(inplace=True)

    latest_idx = df_model['people_vaccinated'].index[-1]
    latest_people_vaccinated = df_model.loc[latest_idx]['people_vaccinated']
    latest_people_fully_vaccinated = df_model.loc[latest_idx]['people_fully_vaccinated']

    latest_people_vaccinated, latest_idx

    pct_vaccinated = latest_people_vaccinated / popsize * 100
    pct_grownups = latest_people_vaccinated / grownups * 100
    
    if pct_grownups > 100:
        pct_grownups = 100
    
    pct_fully_vaccinated = latest_people_fully_vaccinated / popsize * 100
    pct_fully_grownups = latest_people_fully_vaccinated / grownups * 100
    
    if pct_fully_grownups > 100:
        pct_fully_grownups = 100

    twitter_handles = ['@covid_nl', '@kalahiri', '@YorickB']
    two_random_handles = random.sample(twitter_handles, 2)
    headers = [
        f'🧙✨🔮 Het orakel kijkt diep in de kristallen bol en ziet daar een grafiek verschijnen.',
        f'🧙✨🔮 Rook, vuur en lasereffecten! Het orakel verschijnt.',
        f'🧙✨🔮 Het orakel kijkt diep in de kristallen bol. {two_random_handles[0]} denkt er zo over en {two_random_handles[1]} weer net wat anders.',
    ]
    
    tweet = f"""{random.choice(headers)}

Gevaccineerd met ten minste een dosis:
{progressbar(pct_vaccinated)} van de Nederlanders

{progressbar(pct_grownups)} van de volwassenen""".strip()
    
    tweet2 = f"""
Volledig gevaccineerd, alle doses van een vaccin ontvangen:
{progressbar(pct_fully_vaccinated)} van de Nederlanders

{progressbar(pct_fully_grownups)} van de volwassenen""".strip()
    
    return [tweet, tweet2, _latest_year_tweet(), 'https://twitter.com/vaccinorakel/status/1367747721671675910'], [[]]
