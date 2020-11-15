import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import datetime
import csv

# This handles Twitter authetification and the connection to Twitter Streaming API
consumerKey = "OzNzNQ7J2nqXyQwTIUNHfLzLa"
consumerSecret = "RZVjQ1aij9O9Fx6dreD49v7esLUjphBBsAKsWLibaQr3poRaL8"
accessToken = "1327243608622202882-JCmI0IYN7SYdkS0w4MU1vLgOJ31nZM"
accessTokenSecret = "xu2c07oJ5IWOeHdLQ4bNOTtosN6nLfDo6P2qlrSdlTDNG"

auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

#This function checks for the date to be in specific date range
def date_range(start,end):
   current = start
   while (end - current).days >= 0:
      yield current
      current = current + datetime.timedelta(seconds=1)

# TWITTER STREAM LISTENER #
class TweetListener(StreamListener):
          
    def on_status(self, status):
        #Start date: 03/02/2020  and End date: 08/02/2020
        startDate = datetime.datetime(2020, 2, 3)
        stopDate = datetime.datetime(2020, 2, 8)
        countries=['India','Sweden','Canada','Pakistan','Norway','USA']
        for status.created_at in date_range(startDate,stopDate):
            try:
                #Check if the language of the tweet is English and user belongs to one of the above specified countries
                if(status.lang=="en" and (status.user).location in countries):
                    print(status.created_at)
                    with open("tweets.csv",'a',encoding="utf-8") as tf:
                        csvwriter=csv.writer(tf)
                        csvwriter.writerow([status.id_str,status.text,(status.user).name,str(status.created_at),(status.user).location]) #status.place.country])
                return True
            except BaseException as e:
                print("Error on_data %s" % str(e))

if __name__ == '__main__':
    with open("tweets.csv",'w') as tf:
        csvwriter=csv.writer(tf)
        csvwriter.writerow(['Tweet ID','Text','Username','Time','Location'])
        
    stream = Stream(auth, TweetListener(), secure=True)

    # This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=["Coronavirus", "COVID_19", "COVID19", "COVID19Pandemic", "Lockdown", "StayHomeSaveLives", "StayHome"])
    


            
