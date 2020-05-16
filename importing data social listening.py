# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:29:33 2019

@author: david
"""

#setting credentials and n (number of iterations to make)
API_KEY = '0PABlkuTi8NfDCf7OOaWXfCUq'
API_SECRET_KEY = 'pMG7Rh9upJxysFF17vJ9oue2DPzQ5yAxwtiRVLynludMFMGBbh'
ACCESS_TOKEN = '2891305923-OeYVUwyCxCvfBJosHwFFRRfqtLZgjewrUdPTdFa'
ACCESS_TOKEN_SECRET = '4v6eTUQnsBqtPjLx7ZNzfWsF45xxtO7nWXklYTvbVZxJ4'
screen_name = "@Princeton"
direccion = r"direccion"
n = 100
# importing the packages
import os
import re
import tweepy
import pandas as pd
import csv
import sqlite3
import re
import nltk.tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from unicodedata import normalize
# creating  function to clen the databse
def cleaning(sentence, language):
    sentence = re.sub(r'@[^\s]+',"",sentence)
    sentence = re.sub(r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*","",sentence)
    sentence = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", sentence), 0, re.I
    )
    sentence = normalize( 'NFC', sentence)
    #sentence = deEmojify(sentence)
    ListStopWords =stopwords.words(language)
    ListStopWords.append(screen_name)
    return re.sub(r'[^\w\s]','',' '.join([ token for token in word_tokenize(sentence) if token.lower() not in stopwords.words(language) ]))

# setting the information
os.chdir(direccion)
auth  = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
statuses =[]
#setting the neccesary things to get the other stuff

ColumnID =[]
ColumnTweet=[]
ColumnTime = []
ColumnPlace = []
ColumnUser = []
Columnin_reply_to_screen_name = []
ColumnPlacecoordinates = []
ColumnPlacePais = []
ColumnPlaceNombre = []
ColumnRetweetCount = []
ColumnSource = []
ColumnUserDescription = []
ColumnUserFavoritesCount = []
ColumnUserFollowersCount = []
ColumnUserFriendsCount = []
ColumnUserLocation = []
ColumnUserStatusesCount = []
ColumnUserCreationTime = []
ColumnUserVerified = []
ColumnUserProtected = []
Columnin_reply_to_status_id = []
df = pd.DataFrame()

# Taking the tweets
tweets = tweepy.Cursor(api.search,
              q=screen_name).items(n)
# Loopining through the tweets and getting the information
for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items(n):
    if hasattr(tweet,'in_reply_to_status_id') and getattr(tweet, 'in_reply_to_status_id') !="":
        try:
            tweet = api.get_status(tweet.in_reply_to_status_id,tweet_mode="extended")
            ColumnID.append(tweet.id_str)
            ColumnTweet.append(cleaning(tweet.full_text,'spanish'))
            ColumnTime.append(tweet.created_at)
            ColumnPlace.append(tweet.user.location)
            ColumnUser.append(tweet.user.screen_name)
            if hasattr(getattr(tweet,'place'), 'bounding_box') and getattr(tweet, 'place') !="":
                ColumnPlacecoordinates.append(tweet.place.bounding_box.coordinates)
                ColumnPlacePais.append(tweet.place.country)
                ColumnPlaceNombre.append(tweet.place.name)
            else:
                ColumnPlacecoordinates.append(0)
                ColumnPlacePais.append(0)
                ColumnPlaceNombre.append(0)
            ColumnRetweetCount.append(tweet.retweet_count)
            ColumnSource.append(tweet.source)
            if tweet.user.description != "":
                ColumnUserDescription.append(cleaning(tweet.user.description,'spanish'))
            else:
                ColumnUserDescription.append(0)
            ColumnUserFavoritesCount.append(tweet.user.favourites_count)
            ColumnUserFollowersCount.append(tweet.user.followers_count)
            ColumnUserFriendsCount.append(tweet.user.friends_count)
            ColumnUserLocation.append(tweet.user.location)
            ColumnUserStatusesCount.append(tweet.user.statuses_count)
            ColumnUserCreationTime.append(tweet.user.created_at)
            ColumnUserVerified.append(tweet.user.verified)
            ColumnUserProtected.append(tweet.user.protected)
        except:
            pass
# adding the information to the dataset
df = pd.DataFrame()
df['id_str']=ColumnID
df['created_at']=ColumnTime
df['text.encode("UTF-8")']=ColumnTweet
df['user.location']=ColumnPlace
df['user.screen_name']=ColumnUser
#df['in_reply_to_screen_name'] = Columnin_reply_to_screen_name
df['place.bounding_box.coordinates']=ColumnPlacecoordinates
df['place.country']=ColumnPlacePais
df['place.name']=ColumnPlaceNombre
df['RetweetCount']=ColumnRetweetCount
df['retweet_count']=ColumnRetweetCount
df['source']=ColumnSource
df['user.description']=ColumnUserDescription
df['user.favourites_count']=ColumnUserFavoritesCount
df['user.followers_count']=ColumnUserFollowersCount
df['user.friends_count']=ColumnUserFriendsCount
df['user.location']=ColumnUserLocation
df['user.statuses_count']=ColumnUserStatusesCount
df['user.created_at']=ColumnUserCreationTime
df['user.verified']=ColumnUserVerified
df['tweet.user.protected']=ColumnUserProtected

# saving the dataset
df.to_csv('tweetsCollected.csv')

