## This code imports some of Donald Trumps most recent tweets, checks whether he has said any form
## of the word SAD in the last 24hrs and prints the results in a window
import secrets
import tweepy
import datetime
import tkinter as tk

#Variables that contains the user credentials to access Twitter API
#Figure out how to hide these
access_token = secrets.ACC_TOK
access_token_secret = secrets.ACC_TOK_SEC 
consumer_key = secrets.CON_KEY
consumer_secret = secrets.CON_SEC

#Get tweets and save them
def get_all_tweets(screen_name):
    #source for this function: https://gist.github.com/yanofsky/5436496
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=20)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(alltweets) < 30:
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
            #save most recent tweets
            alltweets.extend(new_tweets)
        
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
        
            #print ("...%s tweets downloaded so far" % (len(alltweets)))

    #Record all tweets and times in lists
    outtweets = [tweet.text for tweet in alltweets]
    outtweetstime = [tweet.created_at for tweet in alltweets]
    return outtweets, outtweetstime

#Find if words are in tweets
def find_word(mystring, words):
    for oneword in words:
        if oneword in mystring:
            return True 

        
if __name__ == '__main__':
    #pass in the username of the account you want to download, save tweets to 'outtweets'
    outtweets, outtweetstime = get_all_tweets("realDonaldTrump")

    #Find today's date and yesterday
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    #Set up new lists
    newtime = [] 
    newtext = []
    #Find tweets that occured in the last 24hrs
    for num,tweet in enumerate(outtweetstime):
        if (outtweetstime[num] >= yesterday and outtweetstime[num] <= today):
            newtime.append(tweet)
            newtext.append(outtweets[num])

    savedtweetsad = []
    savedtweethappy = []
    #Search for the word sad in the tweets from the last day
    words = ['sad', 'Sad', 'SAD','Sad!','Sad.','sad.','sad!']
    for tweet in newtext:
        if find_word(tweet, words):
            savedtweetsad.append(tweet)
        else:
            savedtweethappy.append(tweet)

#Create the GUI
    root = tk.Tk()

    #This is what happens when you click the button
    def redisplay_window(savedtweetsad, savedtweethappy):
        new_button.destroy()
        T = tk.Text(root, height=100, width=60)
        T.pack()
        if not savedtweetsad:
            T.insert('1.0', "\nHe's not sad today! Here's what he's thinking about instead: \n")
            for t in savedtweethappy:
                T.insert('end', "\n %s \n" % t)
        else:
            T.insert('1.0', "\nHe's sad today because:\n")
            for t in savedtweetsad:
                T.insert('end', "\n %s \n" % t) 
        T.pack()

    #Create label
    label = tk.Label(root, text = "Is @realDonaldTrump feeling sad today?")
    label.pack()

    #create button
    new_button = tk.Button(root, text = "FIND OUT!", command = lambda: redisplay_window(savedtweetsad, savedtweethappy))
    new_button.pack()


    root.mainloop()

    

