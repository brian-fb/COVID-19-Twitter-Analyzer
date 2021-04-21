import time
import tweepy
import json
from tweepy import OAuthHandler
import pprint
pp = pprint.PrettyPrinter(indent=2)

class Tweet_fetcher():

    def __init__(self):
        consumer_key='ScZwjSAdZlYMgDMoiV4tZCtdp'
        consumer_secret='oao2tSoTOCqgLtfM7Jukadu3uVGKaFrxBL5n9J4dfoh8IOtIq1'
        access_token ='1357024029912174593-ivjatWOJpcZb0fK6VxtVbVU8a0pDsC'
        access_secret='InbUYLFIQz4gOdQphkr1EIea2ffZHAhBfrpSwOOX9aPgC'

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def get_tweets(self, user_id = '759251', time='2017-12-27'):

        tweet_dict = dict()
        for tweet in tweepy.Cursor(self.api.user_timeline, id=user_id, since=time).items():

            msg = tweet._json
            # pp.pprint(msg)
            user_name = msg['user']['name']
            send_time = msg['created_at']
            if 'retweeted_status' in msg:
                try:
                    tweet = msg['retweeted_status']['extended_tweet']['full_text']
                    print(tweet)
                except:
                    tweet = msg['retweeted_status']['text']
                    print(tweet)

            else:

                if "extended_tweet" in msg:
                    # add at the end of each tweet "t_end"
                    tweet = msg['extended_tweet']['full_text']
                    print(tweet)
                else:
                    # add at the end of each tweet "t_end"
                    tweet = msg['text']
                    print(tweet)

            if tweet_dict.get(user_name) is None:
                tweet_dict[user_name] = list()
            tweet_dict[user_name].append({'time': send_time, 'content': tweet})

        return tweet_dict

if __name__ == '__main__':

        F = Tweet_fetcher()