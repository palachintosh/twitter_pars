import tweepy
import time
import datetime
from db_work import SaveTweets


class TwitterInteraction:
    def __init__(self, api_key=None, api_key_secret=None, access_token=None, access_token_secret=None, log=False):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.log = log

    def twee_auth(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(auth, retry_count=3, retry_delay=60, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        #print(api.me())

        try:
            api.verify_credentials()
            print("200 Authorization OK")
            exit_query = False
        except:
            print("Authorization error!")
            raise SystemExit()

        
        while exit_query == False:
            try:
                tweets = tweepy.Cursor(api.home_timeline, tweet_mode='extended').items(limit=10)

            except tweepy.RateLimitError:
                print("Rate limiting error. Waiting to response..")
                time.sleep(901)
            
            data = []
            insert_data = ()
            db = SaveTweets()
            returned_time = db.select_time_from_db()

            for tweet in tweets:
                if returned_time != tweet.created_at:
                    insert_data = (tweet.created_at, tweet.user.screen_name, str(tweet.geo), tweet.full_text)
                    data.append(insert_data)
                    print("Here")
                else:
                    break
            
            if data:
                data.reverse()
                if db.add_to_db(data):
                    if self.log:
                        with open('/home/lesha/Python/django_project/request_log/twitter.log', "w") as f:
                            print("Successful", datetime.datetime.now(), file=f)
                    time.sleep(1)

            else:
                import sys
                print("Collecting tweets..")
                for i in range(10):
                    sys.stdout.write("\r[%s%s]" % ('#' * i, '.' * (10-i)))
                    time.sleep(10)
                print()
            #exit_query = True


if __name__ == "__main__":
    t = TwitterInteraction()
    t.twee_auth()
    