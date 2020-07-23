import tweepy
import time
import os

from dotenv import load_dotenv


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

    nices = api.search(q = '#nice', since_id = lastNice)

    try:
        for nice in reversed(nices):    # Reverse to see first the older tweets
            print('Found #nice: ' + nice.text + '\n\tID: ' + str(nice.id)
                  + '\n\tUsername: ' + nice.user.screen_name + '\nResponding...')
            lastNice = nice.id

            # Storing now because it's safer
            store(lastNice, niceFileName)
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
    except:
        print("Error found, code = " + str(tweepy.TweepError))
        if(str(tweepy.TweepError) == 385):  # 385 is "Deleted tweet"
            print("Can continue")
        else:
            print("Waiting 20m...")
            time.sleep(60*19)               #19m plus the 1 in the infinite loop


niceFileName = 'NiceID.txt'
niceCountFileName = 'NiceCount.txt'

load_dotenv(encoding = "utf8")

# You can find these keys in twitter developer
APIKey = os.getenv("API_KEY")
APISecret = os.getenv("API_SECRET_KEY")
accessToken = os.getenv("ACCESS_TOKEN")
accessSecret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(APIKey, APISecret)
auth.set_access_token(accessToken, accessSecret)
api = tweepy.API(auth)

global phrase   # Prevent bot detection
phrase = 0

while True:     # Infinite loop, always responding
    print('Checking for #nice...')
    search()
    print('Waiting 60 seconds')
    time.sleep(60)
