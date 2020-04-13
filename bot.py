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
    # this is to prevent bot detection
    phrase = 0

    # Retrieve the last seen tweet's ID
    lastNice = retrieve(niceFileName)

    # Retrieve number of nices to this point
    numberNices = retrieve(niceCountFileName)

    nices = api.search(q = '#nice', since_id = lastNice)

    # Reverse to see first the older tweets
    for nice in reversed(nices):
        print('Found #nice: ' + nice.text + '\n\tID: ' + str(nice.id)
            + '\nResponding...')
        lastNice = nice.id
        store(lastNice, niceFileName)

        if(phrase == 0):
            api.update_status('@' + nice.user.screen_name +
            ' Your nice hashtag was the ' + str(numberNices) +
            'th since 13/04/2020! Nice!', nice.id)
        elif(phrase == 1):
            api.update_status('@' + nice.user.screen_name +
            ' Since 13/04/2020, there has been ' + str(numberNices - 1) +
            '. Yours was ' + str(numberNices) + '. Nice!', nice.id)
        elif(phrase == 2):
            api.update_status('@' + nice.user.screen_name +
            ' With your nice hashtag, the number of nices said ince 13/04/2020 has inscreased to ' +
            str(numberNices) + '. Nice!', nice.id)

        numberNices = numberNices + 1
        phrase = phrase + 1
        if(phrase == 3):
            phrase = 0

        print('\n')
    store(numberNices, niceCountFileName)


mentionsFileName = 'MentionsID.txt'
niceFileName = 'NiceID.txt'
niceCountFileName = 'NiceCount.txt'

# You can find these keys in twitter developer
consumerKey = 'ux2xvOZ7cBc1vIGZSthjhw0KW'
consumerSecret = 'wZhFMH4zn1OjjERpkS1DW3FTGrf6ijWgIwBylP0p8oNHZYwP8K'
accessKey = '1249442524873146369-Zfpo4dTW6qr0o5H3wROuFywhtfZeSF'
accessSecret = 'YkdQU8bGgP2DXLYU0A2FJToIiVvaO5qb3Z55NSVabdp1a'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessKey, accessSecret)
api = tweepy.API(auth)

# Infinite loop, always responding (40 in 40 seconds)
while True:
    #print('Checking for mentions...')
    #reply()

    print('Checking for #nice...')
    search()
    print('Waiting 40 seconds')
    time.sleep(40)