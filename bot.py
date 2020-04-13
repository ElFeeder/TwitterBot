import tweepy
import time


def retrieveID(fileName):
    textFile = open(fileName, 'r')
    lastID = int(textFile.read().strip())
    textFile.close()
    return lastID


def storeID(lastID, fileName):
    textFile = open(fileName, 'w')
    textFile.write(str(lastID))
    textFile.close()
    return


def reply():
    # Retrieve the last seen tweet's ID
    lastID = retrieveID(fileName)

    #Uncomment next line for testing purposes
    #lastID = 1249479111891914752

    # Stores all mentions of user
    mentions = api.mentions_timeline(lastID)

    # Reverse to see first the older tweets
    for mention in reversed(mentions):
        print('Found mention: ' +  mention.text + '\n\tID: ' + str(mention.id))
        lastID = mention.id
        storeID(lastID, fileName)
        if('drena' in mention.text.lower()):
            print('found drena, responding')
            api.update_status('@' + mention.user.screen_name + ' That\'s the spirit!',
                mention.id)
        
        print('\n')


fileName = 'LastID.txt'

# You can find these keys in twitter developer
consumerKey = 'ux2xvOZ7cBc1vIGZSthjhw0KW'
consumerSecret = 'wZhFMH4zn1OjjERpkS1DW3FTGrf6ijWgIwBylP0p8oNHZYwP8K'
accessKey = '1249442524873146369-YGJLKzvqW4sNFpBcd8q87Du3kqa4V8'
accessSecret = '7jschEQbz3TSp4wlm2RkFVivwjWllWPQWiwSJJ9rPZpSj'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessKey, accessSecret)
api = tweepy.API(auth)

# Infinite loop, always responding (20 in 20 seconds)
while True:
    print('Checking for mentions...')
    reply()
    time.sleep(20)