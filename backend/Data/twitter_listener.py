import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import socket
import json

#Twitter Confidentials
consumer_key='ScZwjSAdZlYMgDMoiV4tZCtdp'
consumer_secret='oao2tSoTOCqgLtfM7Jukadu3uVGKaFrxBL5n9J4dfoh8IOtIq1'
access_token ='1357024029912174593-ivjatWOJpcZb0fK6VxtVbVU8a0pDsC'
access_secret='InbUYLFIQz4gOdQphkr1EIea2ffZHAhBfrpSwOOX9aPgC'

class TweetsListener(StreamListener):
  # tweet object listens for the tweets
    def __init__(self, csocket):
        self.client_socket = csocket
    def on_data(self, data):
        try:  
            msg = json.loads( data )
            print("\nnew message:")
      # if tweet is longer than 140 characters
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
                    self.client_socket.send(str(tweet+"t_end").encode('utf-8'))          
                    print(tweet)
                else:
                # add at the end of each tweet "t_end" 
                    tweet = msg['text']
                    self.client_socket.send(str(tweet+"t_end").encode('utf-8'))  
                    print(tweet)
            return True
    
        except BaseException as e:
            
            print("Error on_data: %s" % str(e))
        return True
   
    def on_error(self, status):
        print(status)
        return True
    
def sendData(c_socket, keyword):
    print('start sending data from Twitter to socket')
    # authentication based on the credentials
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # start sending data from the Streaming API 
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track = keyword, languages=["en"])
    
if __name__ == "__main__":
    # server (local machine) creates listening socket
    s = socket.socket()
    host = "0.0.0.0"    
    port = 5555
    s.bind((host, port))
    print('socket is ready')
    # server (local machine) listens for connections
    s.listen(4)
    print('socket is listening')
    # return the socket and the address on the other side of the connection (client side)
    c_socket, addr = s.accept()
    print("Received request from: " + str(addr))
    # select here the keyword for the tweet data
    sendData(c_socket, keyword = ['coronavirus'])