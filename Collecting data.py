import tweepy
from config import api,auth
from tweepy import Stream
from tweepy.streaming import StreamListener

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])




# def process_or_store(tweet):
#     print(json.dumps(tweet))

# for status in tweepy.Cursor(api.home_timeline).items(2):
#     # Process a single status
#         process_or_store(status._json) 