import tweepy
from tweepy import OAuthHandler

consumer_key = 'CONSU<ERKEY'
consumer_secret = 'SECRET'
access_token = 'TOKEN'
access_secret = 'SECERET'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
