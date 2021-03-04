import tweepy
import os
import json

secrets = json.loads(os.environ['TWEEPY_SECRETS'])

auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])

api = tweepy.API(auth)

api.update_status('test')
