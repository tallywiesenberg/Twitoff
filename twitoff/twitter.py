'''Retrieve tweets, embeddings, and persist in the database'''
import tweepy
from decouple import config
from .model import DB, User, Tweet
import basilica

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET')) 
TWITTER = tweepy.API(TWITTER_AUTH)          

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def get_user_tweets(username):
    '''Retrieve tweets of user, embed them, and store in database'''
    #All user data pulled from twitter
    twitter_user = TWITTER.get_user(username)
    #200 tweets pulled from one user
    tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')
    #User profile created for app
    db_user = User(id=twitter_user.id, username=twitter_user.screen_name, newest_tweet_id=tweets[0].id)
    for tweet in tweets:
        #Embed tweets with basilica
        embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
        #Prepare each tweet for the database
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
        #Store tweets in database
        DB.session.add(db_tweet)
        db_user.tweets.append(db_tweet)
    #Store user in database
    DB.session.add(db_user)
    DB.session.commit()