import tweepy
import time



def retrieve(fileName):
    textFile = open(fileName, 'r')
    ID = int(textFile.read().strip())
    textFile.close()
    return ID


def store(ID, fileName):
    textFile = open(fileName, 'w')
    textFile.write(str(ID))
    textFile.close()
    return


def reply():
    # Retrieve the last seen tweet's ID
    lastID = retrieve(mentionsFileName)

    #Uncomment next line for testing purposes
    #lastID = 1249479111891914752

    # Stores all mentions of user
    mentions = api.mentions_timeline(lastID)

    # Reverse to see first the older tweets
    for mention in reversed(mentions):
        print('Found mention: ' +  mention.text + '\n\tID: ' + str(mention.id))
        lastID = mention.id
        store(lastID, mentionsFileName)
        if('drena' in mention.text.lower()):
            print('found drena, responding')
            api.update_status('@' + mention.user.screen_name + ' That\'s the spirit!',
                mention.id)
        
        print('\n')


def search():
    # Retrieve the last seen tweet's ID
    lastNice = retrieve(niceFileName)

    # Retrieve number of nices to this point
    numberNices = retrieve(niceCountFileName)

    nices = api.search(q = '#nice', since_id = lastNice)
    for nice in reversed(nices):
        print('Found #nice: ' + nice.text + '\n\tID: ' + str(nice.id)
            + '\nResponding...')
        lastNice = nice.id
        store(lastNice, niceFileName)
        api.update_status('@' + nice.user.screen_name + ' Your nice hashtag was the '
            + str(numberNices) + 'th since 13/04/2020 13:08! Nice!', nice.id)

        numberNices = numberNices + 1
        print('\n')
    store(numberNices, niceCountFileName)


mentionsFileName = 'MentionsID.txt'
niceFileName = 'NiceID.txt'
niceCountFileName = 'NiceCount.txt'

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
    #print('Checking for mentions...')
    #reply()

    print('Checking for #nice...')
    search()
    time.sleep(20)