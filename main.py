import os
from google.cloud import language_v1
import tweepy
import pandas as pd


class CryptoSentimentAnalysisBase():
    MAX_ID = -1
    TWEET_COUNT = 0
    HASHTAG = '#Ethereum'
    MAX_TWEETS = 100
    TWEETS_PER_QUERY = 100

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret,
                 key_word,
                 tweets_per_query,
                 tweet_count,
                 max_tweets,
                 max_id,
                 ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        if key_word is None:
            self.key_word = CryptoSentimentAnalysisBase.HASHTAG
        if tweets_per_query is None:
            self.tweets_per_query = CryptoSentimentAnalysisBase.TWEETS_PER_QUERY,
        if tweet_count is None:
            self.tweet_count = CryptoSentimentAnalysisBase.TWEET_COUNT
        if max_tweets is None:
            self.max_tweets = CryptoSentimentAnalysisBase.MAX_TWEETS
        if max_id is None:
            self.max_id = CryptoSentimentAnalysisBase.MAX_ID

    def authenticate_user(self):
        authenticate = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        return authenticate

    def set_access_token(self):
        access_token = self.authenticate_user().set_access_token(self.access_token, self.access_token_secret)
        return access_token

    def api_call(self):
        api = tweepy.API(self.authenticate_user(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api

    def generate_results(self):
        twitter_posts = []
        while self.tweet_count < self.max_tweets:
            if self.max_id <= 0:
                new_tweets = self.api_call().search(q=self.key_word,
                                                    count=self.tweets_per_query,
                                                    result_type='recent',
                                                    tweet_mode='extended')
            else:
                new_tweets = self.api_call().search(q=self.key_word,
                                                    count=self.tweets_per_query,
                                                    max_id=str(self.max_id -1),
                                                    result_type='recent',
                                                    tweet_mode='extended')
            if not new_tweets:
                break

            for tweet in new_tweets:
                result = {}
                result['text'] = tweet.full_text.encode('utf-8')

            self.tweet_count += len(new_tweets)
            self.max_id = new_tweets[-1].id
