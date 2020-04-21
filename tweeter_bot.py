import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import creadentials
import time
import json
import pandas as pd
import numpy as np
from textblob import TextBlob
import os

class TweeterDF():

    def __init__(self):
        self.auth = AuthenticationSystem().authenticate_tweeter_app()
        self.tweeter_client = API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    def load_df(self):
        for tweet in Cursor(self.tweeter_client.user_timeline).items():
            try:
                if tweet.id not in pd.read_csv('data/user_info.csv').values:
                    df = pd.DataFrame(data=[tweet.text for tweet in Cursor(self.tweeter_client.user_timeline).items()],columns=['Tweets'])
                    df['Tweet_ID'] = np.array([tweet.id for tweet in Cursor(self.tweeter_client.user_timeline).items()])
                    df.to_csv('data/user_info.csv')
            except pd.errors.EmptyDataError:
                    df = pd.DataFrame(data=[tweet.text for tweet in Cursor(self.tweeter_client.user_timeline).items()],columns=['Tweets'])
                    df['Tweet_ID'] = np.array([tweet.id for tweet in Cursor(self.tweeter_client.user_timeline).items()])
                    df.to_csv('data/user_info.csv')

class AuthenticationSystem():

    def authenticate_tweeter_app(self):
        auth = OAuthHandler(creadentials.API_key,creadentials.API_secret_key)
        auth.set_access_token(creadentials.Access_Token,creadentials.Access_Token_secret)
        return auth

class TweeterClient():

    def __init__(self):
        self.auth = AuthenticationSystem().authenticate_tweeter_app()
        self.tweeter_client = API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    def homeTimeline(self):
        # tweets = []
        for tweet in Cursor(self.tweeter_client.home_timeline,tweet_mode='extended').items():
            # tweets.append(tweet)
            print(tweet.full_text)
            with open('data/home_timeline.txt','a', encoding='utf-8') as f:
                f.write(tweet.full_text+'\n')
        # return tweets

    def userTimeline(self,username_tweeter=None):
        # tweets = []
        for tweet in Cursor(self.tweeter_client.user_timeline,id=username_tweeter,tweet_mode='extended').items():
            print(tweet.full_text)
            with open('data/user_timeline.txt','a', encoding='utf-8') as f:
                f.write(tweet.full_text+'\n')
        

class TweeterFollow():
    def __init__(self):
        self.auth = AuthenticationSystem().authenticate_tweeter_app()
        self.tweeter_client = API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    def followUser(self,username_tweeter):
        for follower in Cursor(self.tweeter_client.search_users,q=username_tweeter).items(1):
            print(follower.screen_name , " => " , follower.followers_count)
            print("Following......")
            follower.follow()
            print("Following : ",follower.name)

    def followBack(self):
        for follower in Cursor(self.tweeter_client.followers).items():
            # print(follower.following)
            if follower.following  == False:
                print(follower.screen_name , " => ", follower.followers_count)
                print("Following......")
                follower.follow()
                print("Following : ",follower.name)
            print('\n\n')

    def followHashtags(self,search_query):
        for follower in Cursor(self.tweeter_client.search,q=search_query).items():
            print(follower)
            # print("Following......")
            # follower.follow()
            # print("Following : ",follower.name)
            # print('\n\n')

class TweeterTweeting():
    def __init__(self):
        self.auth = AuthenticationSystem().authenticate_tweeter_app()
        self.tweeter_client = API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    def updateStatus(self,text,filename_of_files=None):
        print("Updating Status......")
        
        media_ids = []
        if filename_of_files != None:
            for filename in filename_of_files:
                res = self.tweeter_client.media_upload(filename)
                media_ids.append(res.media_id)
            self.tweeter_client.update_status(status = text, media_ids=media_ids)
        else:

            self.tweeter_client.update_status(status = text)
        # for tweet in Cursor(self.tweeter_client.user_timeline).items():
        #     with open('data/tweet_ids.txt','r') as f:
        #         if tweet.id is not f.read():
        #             print(f.read())
        #             with open('data/tweet_ids.txt','w') as f:
        #                 text = tweet.text+" => "+str(tweet.id)+"\n"
        #                 f.write(str(text))

        '''
            Only thing to note that we have to create a user_info.csv file to run this code successfully
        '''
        # for tweet in Cursor(self.tweeter_client.user_timeline).items():
        #     try:
        #         if tweet.id not in pd.read_csv('data/user_info.csv').values:
        #             df = pd.DataFrame(data=[tweet.text for tweet in Cursor(self.tweeter_client.user_timeline).items()],columns=['Tweets'])
        #             df['Tweet_ID'] = np.array([tweet.id for tweet in Cursor(self.tweeter_client.user_timeline).items()])
        #             df.to_csv('data/user_info.csv')
        #     except pd.errors.EmptyDataError:
        #             df = pd.DataFrame(data=[tweet.text for tweet in Cursor(self.tweeter_client.user_timeline).items()],columns=['Tweets'])
        #             df['Tweet_ID'] = np.array([tweet.id for tweet in Cursor(self.tweeter_client.user_timeline).items()])
        #             df.to_csv('data/user_info.csv')
        tweeter_df = TweeterDF()
        tweeter_df.load_df()
        print("Tweeted XD...\n")
    
    def deleteStatus(self,tweet_id):
        print("Deleting Status......")

        self.tweeter_client.destroy_status(tweet_id)

        df = pd.read_csv('data/user_info.csv')
        df = df[df.Tweet_ID != int(tweet_id)]
        print(df)

        df.to_csv('data/user_info.csv')
        print("Deleted the Tweet")

class TweeterReply():
    def __init__(self):
        self.auth = AuthenticationSystem().authenticate_tweeter_app()
        self.tweeter_client = API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    def retrieve_last_seen_id(self,filename):
        with open('data/'+filename,'r') as f:
            user_id = f.read()
        return user_id

    def store_last_seen_id(self,last_seen_id,filename):
        with open('data/'+filename,'w') as f:
            f.write(str(last_seen_id))
    '''
        The user_ids.txt file must created before the code executes
    '''
    def mentionReply(self):
        last_seen_id = self.retrieve_last_seen_id('user_ids.txt')
        mentions = self.tweeter_client.mentions_timeline(since_id=last_seen_id,tweet_mode='extended')
        tweeter_df = TweeterDF()
        tweeter_df.load_df()
        if mentions:
            for mention in reversed(mentions):
                last_seen_id = mention.id
                self.store_last_seen_id(last_seen_id,'user_ids.txt')   
                self.tweeter_client.update_status(f'@{mention.user.screen_name} Thank you so much',mention.id)  
                print(f'Replying to --------> {mention.user.screen_name}\n')
                mention.favorite()    
        else:
            print("No tweets to reply to...\n")


class TweeterTimeline():
    def __init__(self):
        self.auth = AuthenticationSystem().authenticate_tweeter_app()
        self.tweeter_client = API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        

    

   


    
    def newsfeed_scroll(self):
        count = 0
        # last_seen_id = self.retrieve_last_seen_id('visited_tweet.txt')
        for tweet in Cursor(self.tweeter_client.home_timeline,tweet_mode = 'extended').items():
            # tweets.append(tweet)
            # last_seen_id = tweet.id
            # self.store_last_seen_id(last_seen_id,'visited_tweet.txt')
            print(f'\n{tweet.user.name} Posted something, --> {tweet.user.followers_count}')
            # try:
                
            # if(tweet.id not in pd.read_csv('data/visited_tweet.csv').values):
            if(self.tweeter_client.show_friendship(target_id=tweet.user.id) and count<3):
                try:
                    # df = pd.DataFrame(data=[tweet.user.id],columns=['Tweet ID'])
                    # df_read = df.append(df)
                    # df_read.to_csv('data/visited_tweet.csv')
                    # self.tweeter_client.create_favorite(id = tweet.id)

                    tweet.favorite()
                    print("******  L  I  K  I  N  G  ******")
                    # print(tweet.id)
                    blob = TextBlob(tweet.full_text)
                    print(f'The polarity of the post is : {blob.sentiment.polarity}')
                    if blob.sentiment.polarity >= 0.3:
                        self.retweet(tweet.id)
                    count = count + 1
                except tweepy.error.TweepError:
                    print("Already liked......\n")
                    continue
            # print(tweet)
            else:
                print("He is not a friend....or.....its time to check any mentions")
                return
            # else:
                # continue
            # except pd.errors.EmptyDataError:
            #     if(self.tweeter_client.show_friendship(target_id=tweet.user.id) and count<3):
            #             try:
            #                 df = pd.DataFrame(data=[tweet.user.id],columns=['Tweet ID'])
            #                 df.to_csv('data/visited_tweet.csv')
            #                 self.tweeter_client.create_favorite(id = tweet.id)
            #                 print("He is friend.....")
            #                 count = count + 1
            #             except tweepy.error.TweepError:
            #                 continue
            #         # print(tweet)
            #     else:
            #         print("He is not a friend....or.....its time to check any mentions")
            #         return
                

    def retweet(self,tweet_id):
        try:
            self.tweeter_client.retweet(tweet_id)
            print("Retweeted\n")
            tweeter_df = TweeterDF()
            tweeter_df.load_df()
            # for tweet in Cursor(self.tweeter_client.user_timeline).items():
            #     try:
            #         if tweet.id not in pd.read_csv('data/user_info.csv').values:
            #             df = pd.DataFrame(data=[tweet.text for tweet in Cursor(self.tweeter_client.user_timeline).items()],columns=['Tweets'])
            #             df['Tweet_ID'] = np.array([tweet.id for tweet in Cursor(self.tweeter_client.user_timeline).items()])
            #             df.to_csv('data/user_info.csv')
            #     except pd.errors.EmptyDataError:
            #             df = pd.DataFrame(data=[tweet.text for tweet in Cursor(self.tweeter_client.user_timeline).items()],columns=['Tweets'])
            #             df['Tweet_ID'] = np.array([tweet.id for tweet in Cursor(self.tweeter_client.user_timeline).items()])
            #             df.to_csv('data/user_info.csv')
        except tweepy.error.TweepError:
            print("Already Retweeted...")
        

class TweeterStreamer():

    def __init__(self):
        self.auth = AuthenticationSystem().authenticate_tweeter_app()
    
    def stream_particular_tweets(self,hashtag):
        listener = TweeterListener()
        stream = Stream(self.auth,listener)
        stream.filter(track=hashtag)

class TweeterListener(StreamListener):
    
    def on_data(self,data):
        try:
            json_data = json.loads(data)
            tweet_data = {'text':json_data['text']}
            with open('TweeterListener on_data.txt','a') as f:
                f.write(json_data['text']+'\n')
            print(tweet_data['text'])
            return True
        except BaseException as e:
            print('BaseException Occured : \n',e)

    def on_error(self,status):
        if status==420:
            return False
        print(status)

    
if __name__=='__main__':

    # auth = OAuthHandler(creadentials.API_key,creadentials.API_secret_key)
    # auth.set_access_token(creadentials.Access_Token,creadentials.Access_Token_secret)

    # listener = TweeterListener()
    # stream = Stream(auth,listener)
    # stream.filter(track=['Narendra Modi','Bhuvan Bam','bb ki vines','Zakir Khan'])

    # streamer = TweeterStreamer()
    # streamer.stream_particular_tweets(['Narendra Modi','Bhuvan Bam','bb ki vines','Zakir Khan'])

    # home_timeline = TweeterClient()
    # home_timeline.homeTimeline()
    # home_timeline.userTimeline('narendramodi')

    # follow = TweeterFollow()
    # follow.followUser('bhuvan bam')
    # follow.followBack()
    # follow.followHashtags('#CoronaVirus')

    # tweet = TweeterTweeting()
    # tweet.updateStatus(input("Enter Your Tweet : "))
    # tweet.deleteStatus(input("Enter Tweet ID to delete : "))

    # mentions = TweeterReply()
    # while(True):
    #     scroll = TweeterTimeline()
    #     scroll.newsfeed_scroll()
    #     mentions.mentionReply()
    #     print("Waiting for 30 seconds.....")
    #     time.sleep(30)

    # mentions = TweeterTimeline()
    # mentions.retweet(1242458807198003202)
    
    print("""
    1. Start Scrolling
    2. Follow a particular User 
    3. Follow back Users
    4. Update or Delete Post
    5. Stream A particular profile""")
    choice = int(input("Enter Choice : "))
     
    if choice == 1:
        while(True):
            mentions = TweeterReply()
            while(True):
                scroll = TweeterTimeline()
                scroll.newsfeed_scroll()
                mentions.mentionReply()
                print("Waiting for 30 seconds.....")
                time.sleep(30)

    elif choice == 2:
        follow = TweeterFollow()
        follow.followUser(input("Enter User : "))
    
    elif choice == 3:
        follow = TweeterFollow()
        follow.followBack()

    elif choice == 4:
        tweet = TweeterTweeting()
        choice_update = int(input("Do want update status (0/1) : "))
        if choice_update == 1:
            if int(input("Do You want to upload any media (0/1) : ")) == 1: 
                n = int(input("How many files u wan to upload (MAX 4) :"))
                filenames = []
                abs_path = os.path.abspath(__file__)
                len_abs_path = len(abs_path)-14
                abs_path = abs_path[:len_abs_path]
                print(abs_path)
                for filename in range(n):
                    filenames.append(abs_path+'media\\'+input("Enter file path ; "))
                # print(os.path.abspath(__file__),'\\data\\',filename)
                print(filenames)
                tweet.updateStatus(input("Enter Your Tweet : "),filenames)
            else:
                tweet.updateStatus(input("Enter Your Tweet : "))

        else:
            df = pd.read_csv('data/user_info.csv')
            print(df)
            tweet.deleteStatus(input("Enter Tweet ID to delete : "))


    elif choice == 5:
        home_timeline = TweeterClient()
        # home_timeline.homeTimeline()
        home_timeline.userTimeline(input("Enter User : "))