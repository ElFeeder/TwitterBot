import tweepy
import time
#import os
import random

#from dotenv import load_dotenv


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

    lastNice = retrieve(niceFileName)           # Retrieve last seen tweet's ID
    numberNices = retrieve(niceCountFileName)   # Retrieve number of nices

    nices = api.search_tweets(q = '#nice -filter:retweets', since_id = lastNice)

    try:
        for nice in reversed(nices):    # Reverse to see first the older tweets
            print('Found #nice: ' + nice.text + '\n\tID: ' + str(nice.id)
                  + '\n\tUsername: ' + nice.user.screen_name + '\nResponding...')
            lastNice = nice.id

            # Storing now because it's safer
            store(lastNice, niceFileName)
            numberNices = numberNices + 1
            store(numberNices, niceCountFileName)

            phrase = random.randint(0, 3)   # Prevent bot detection

            if(phrase == 0):
                api.update_status(status = '@' + nice.user.screen_name +
                ' Your nice hashtag was number ' + str(numberNices) +
                ' since 28/01/2022! Nice!', in_reply_to_status_id = nice.id)
            elif(phrase == 1):
                api.update_status(status = '@' + nice.user.screen_name +
                ' Since 28/01/2022, there have been ' + str(numberNices - 1) +
                ' nice hashtags. Yours was number ' + str(numberNices) + '. Nice!', in_reply_to_status_id = nice.id)
            elif(phrase == 2):
                api.update_status(status = '@' + nice.user.screen_name +
                ' With your nice hashtag, the number of nices said since 28/01/2022 has increased to ' +
                str(numberNices) + '. Nice!', in_reply_to_status_id = nice.id)
            elif(phrase == 3):
                api.update_status(status = '@' + nice.user.screen_name +
                ' Before you, ' + str(numberNices - 1) + ' people tweeted a nice hashtag. Now there are ' +
                str(numberNices) + ' nice hashtags in Twitter. Nice!', in_reply_to_status_id =  nice.id)
            elif(phrase == 4):
                api.update_status(status = '@' + nice.user.screen_name +
                ' Thank you for being Nice! Since 28/01/2022, ' + str(numberNices - 1) + ' people tweeted a nice hashtag. Including you, that\'s ' +
                str(numberNices) + ' nice hashtags!', in_reply_to_status_id =  nice.id)

            print('\n')
    except:
        numberNices = numberNices - 1
        print("Error found, code = " + str(tweepy.TweepyException))
        if(str(tweepy.TweepyException) == "385"):  # 385 is "Deleted tweet"
            print("Can continue")
        else:
            print("Waiting 20m...")         # Maybe bot detection
            time.sleep(60*19)               # 19m plus the 1 in the infinite loop


niceFileName = 'NiceID.txt'
niceCountFileName = 'NiceCount.txt'

#load_dotenv(encoding = "utf8")

# You can find these keys in twitter developer
# Ye this should be in and .env but Windows sucks
APIKey = "6dEsiehLbX7kQUZvysRA169IF"
APISecret = "9HyxU5eeQnKOzlpOkRF1AC7H6XZvzAuHWWY9jBM6OIjv9u2aeN"
accessToken = "1249442524873146369-kUvmjcHsK5yJKOcnm3ikonbkgVB9gF"
accessSecret = "BorvGN4C85u0OMYDdZ4GSEQIb1O9THfOlXn3KdljDUIVL"

auth = tweepy.OAuthHandler(APIKey, APISecret)
auth.set_access_token(accessToken, accessSecret)
api = tweepy.API(auth)

while True:     # Infinite loop, always responding
    print('Checking for #nice...')
    search()
    print('Waiting 60 seconds')
    time.sleep(60)
