# Python3
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


def search():
    global phrase
    # Retrieve the last seen tweet's ID
    lastNice = retrieve(niceFileName)

    # Retrieve number of nices to this point
    numberNices = retrieve(niceCountFileName)

    nices = api.search(q = '#nice', since_id = lastNice)

    # Reverse to see first the older tweets
    for nice in reversed(nices):
        print('Found #nice: ' + nice.text + '\n\tID: ' + str(nice.id)
            + '\n\tUsername: ' + nice.user.screen_name + '\nResponding...')
        lastNice = nice.id
        store(lastNice, niceFileName)

        # This is here because of bot prevention
        numberNices = numberNices + 1
        store(numberNices, niceCountFileName)
		
        if(phrase == 0):
            api.update_status('@' + nice.user.screen_name +
            ' Your nice hashtag was the ' + str(numberNices) +
            'th since 13/04/2020 13:08! Nice!', nice.id)
        elif(phrase == 1):
            api.update_status('@' + nice.user.screen_name +
            ' Since 13/04/2020 13:08, there has been ' + str(numberNices - 1) +
            ' nice hashtags. Yours was ' + str(numberNices) + '. Nice!', nice.id)
        elif(phrase == 2):
            api.update_status('@' + nice.user.screen_name +
            ' With your nice hashtag, the number of nices said since 13/04/2020 13:08 has increased to ' +
            str(numberNices) + '. Nice!', nice.id)

        phrase = phrase + 1
        if(phrase == 3):
			phrase = 0

        print('\n')


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

# This is to prevent bot detection
global phrase
phrase = 0

# Infinite loop, always responding
while True:
    print('Checking for #nice...')
    search()
    print('Waiting 60 seconds')
    time.sleep(60)