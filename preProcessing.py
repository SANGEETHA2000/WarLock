import pandas as pd
import regex as re
from shutil import copyfile
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Reading the csv file
df = pd.read_csv('tweets.csv')

#Making a copy to store all preprocessed values
copyfile('tweets.csv', 'tweets1.csv')

#Extracting all required values into respective lists
tweets = df['Text']
tweetID = df['Tweet ID']
name = df['Username']
time = df['Time']
location = df['Location']

#STEP 1: Removing mentions and urs from tweet messages
tweets_without_mention = []
for message in tweets:
    tweets_without_mention.append(re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "",message))

#STEP 2: Removing consecutive non-ascii characters
tweets_without_non_ascii = []
for message in tweets_without_mention:
    tweets_without_non_ascii.append(re.sub(r'[^\x00-\x7F]+',' ', message))

#STEP 3: Tokenization and remove punctuations
tweets_tokens = []
for message in tweets_without_non_ascii:
    words = word_tokenize(message)
    words_without_punctuation = [word for word in words if word.isalnum()]
    tweets_tokens.append(words_without_punctuation)

#STEP 4: Removing stop words
stop_words = set(stopwords.words('english'))
tweets_without_stop_words = [] 
  
for i in tweets_tokens:
    temp = []
    for j in i:
        if j not in stop_words: 
            temp.append(j)
    tweets_without_stop_words.append(temp)

#STEP 5: Final processed tweet messages
processed_tweets= []
for message in tweets_without_stop_words:
    s = " "
    s = s.join(message)
    processed_tweets.append(s)

#Writing the cleaned messages and other relevant data into this file
with open("tweets1.csv",'w',encoding="utf-8") as tf:
    csvwriter=csv.writer(tf)
    for i in range(len(tweets_without_mention)):
        csvwriter.writerow([tweetID[i],processed_tweets[i],name[i],time[i],location[i]])

