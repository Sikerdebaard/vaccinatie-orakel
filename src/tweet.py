import tweepy
import os
import json
from pathlib import Path
from tweets import basictweet
from datetime import datetime
import pandas as pd


tweetscachefile = Path('data/oracle-tweets.json')

if tweetscachefile.exists():
    with open(tweetscachefile, 'r') as fh:
        tweetscache = json.load(fh)
else:
    tweetscache = {}


if 'latest-tweet' in tweetscache:
    threshold = pd.to_datetime(datetime.now()) - pd.Timedelta(hours=2)
    if pd.to_datetime(tweetscache['latest-tweet']['timestamp']) > threshold:
        print('Exiting, last tweet generated < 2 hrs ago')
        raise SystemExit(0)

secrets = json.loads(os.environ['TWEEPY_SECRETS'])

auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])

api = tweepy.API(auth)

tweets, media = basictweet.generate()

tweet = api.update_status(tweets[0])
tweetscache['latest-tweet'] = {
    'id': tweet.id,
    'timestamp': str(pd.to_datetime(datetime.now())),
}
