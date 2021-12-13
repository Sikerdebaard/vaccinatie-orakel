import tweepy
import os
import json
from pathlib import Path
from tweets import basictweet
import pandas as pd
import pytz
from datetime import datetime, time


tz = pytz.timezone('Europe/Amsterdam')
ams_now = datetime.now(tz)
if ams_now.time() < time(hour=20, minute=30):
    print('Its not past 20:30 yet in AMS')
    raise SystemExit(0)

if pd.to_datetime('today').date() > pd.to_datetime('2021-12-19').date():
    print('Bot shutdown, please disable github actions')
    raise SystemExit(100)


tweetscachefile = Path('data/oracle-tweets.json')

if tweetscachefile.exists():
    with open(tweetscachefile, 'r') as fh:
        tweetscache = json.load(fh)
else:
    tweetscache = {}


if 'latest-tweet' in tweetscache:
    #threshold = pd.to_datetime(datetime.now()) - pd.Timedelta(hours=2)
    #if pd.to_datetime(tweetscache['latest-tweet']['timestamp']) > threshold:
    if pd.to_datetime(tweetscache['latest-tweet']['timestamp']).date() == pd.to_datetime(datetime.now()).date():
        print('Exiting, tweet already generated')
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

with open(tweetscachefile, 'w') as fh:
    json.dump(tweetscache, fh)

if len(tweets) > 1:
    for i in range(1, len(tweets)):
        tweet = api.update_status(tweets[i], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
