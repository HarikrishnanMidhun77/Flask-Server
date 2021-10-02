from flask import Flask, json, g, request,jsonify
from oauth2client import client
from flask_cors import CORS
import tweepy
import praw
import requests
import pandas as pd
from pymongo import MongoClient
mongo_url = 'mongodb+srv://harikrishnan_midhun2:DM_pswd@cluster0.iwigi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client=MongoClient(mongo_url)
db = client.DM_ASS2_DB
tweetsDoc = db.tweets
redditDoc=db.reddit
auth = tweepy.OAuthHandler("kXSwf71s8sYxp0pvorx6p8Kqq", "5Co7NohPFGtfRp9OuH4kBpwwZRAud7TStMuTF6DGK7ejrpBKRN")
auth.set_access_token("936707059-BUD3nl11XZpzYCIppB6hQ1NRWI5UTkYDGGjypbFJ", "3AiN2uztfJ6QvXhFlfSLO86z07FeFr9zRbaj35auxz87j")
    # Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index2():
    return "Hello from Flask's test environment"

@app.route("/postTweet", methods=["POST"])
def postTweet():
    tw = request.get_json()
    print(tw)
    api.update_status (status = tw["msg"])
    getTweets()
    return "Tweet posted"

def getTweets():
    tweets = api.user_timeline(screen_name="harikrishnanmid", 
                           # 200 is the maximum allowed count
                           count=10,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
   
    for info in tweets:
        dic2=dict([
            ("created_at" ,info.created_at),
            ("full_text",info.full_text)
        ])
        print(dic2)
        tweetsDoc.insert_one(dic2)
    return "timeline"



@app.route("/postReddit", methods=["POST"])
def postReddit():
    subr = 'DataMiningBDAT2021'
 
    reddit = praw.Reddit(client_id="-sjGBjRoUSz5sv75uR84_A",
                        client_secret="UnD-DOFU7Rg4DCJhjRn4qyT0IN41TQ",
                        user_agent="script by u/harikrishnan_midhun",
                        redirect_uri="http://127.0.0.1:4433/",
                        username="harikrishnan_midhun", password="HariReddit")
    
    subreddit = reddit.subreddit(subr)
    
    redDat = request.get_json()
    print(redDat)
    title=redDat["title"]
    selftext=redDat["selftext"]

    # title = 'Just Made My first Post on Reddit Using Python.'
    # selftext = '''
    # I am learning how to use the Reddit API with Python using the PRAW wrapper.
    # By following the tutorial on https://www.jcchouinard.com/post-on-reddit-with-python-praw/
    # This post was uploaded from my Python Script
    # '''
    
    subreddit.submit(title,selftext=selftext)
    getReddit()
    return "Reddit posted"





#@app.route("/getReddit", methods=["GET"])
def getReddit():
    subreddit = 'DataMiningBDAT2021'
    limit = 100
    timeframe = 'month' #hour, day, week, month, year, all
    listing = 'new' # controversial, best, hot, new, random, rising, top
    
    def get_reddit(subreddit,listing,limit,timeframe):
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
            print(base_url)
            request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        except:
            print('An Error Occured')
        return request.json()
    
    r = get_reddit(subreddit,listing,limit,timeframe)
    myDict = {}
    for post in r['data']['children']:
        myDict[post['data']['title']] = {'url':post['data']['url'],'text':post['data']['selftext'],'score':post['data']['score'],'comments':post['data']['num_comments']}
        redditDoc.insert_one(myDict[post['data']['title']])
    df = pd.DataFrame.from_dict(myDict, orient='index')
    print(get_results(r))
    return ("reddit fetched")

def get_results(r):
    myDict = {}
    for post in r['data']['children']:
        myDict[post['data']['title']] = {'url':post['data']['url'],'score':post['data']['score'],'comments':post['data']['num_comments']}
    df = pd.DataFrame.from_dict(myDict, orient='index')
    return myDict