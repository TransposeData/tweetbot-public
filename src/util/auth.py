from requests_oauthlib import OAuth1Session
import tweepy
import json


def update_access_token(botname: str):
    credentials = get_credentials(botname)
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"

    # Get request token
    oauth = OAuth1Session(
        credentials['apikey'],
        client_secret=credentials['apisecret']
    )
    try:
        r = oauth.fetch_request_token(request_token_url)
    except Exception as e:
        print(e)
        exit()

    # Get resource owner
    resource_owner_key = r.get('oauth_token')
    resource_owner_secret = r.get('oauth_token_secret')
    print("Got OAuth token: %s" % resource_owner_key)


    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        credentials['apikey'],
        client_secret=credentials['apisecret'],
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    credentials['access_token'] = oauth_tokens["oauth_token"]
    credentials['access_token_secret'] = oauth_tokens["oauth_token_secret"]
    store_credentials(botname, credentials)


def get_credentials_filename(botname: str):
    return './credentials/' + botname + '_credentials.json'


def get_credentials(botname: str):
    with open(get_credentials_filename(botname), mode='r') as f:
        return json.load(f)


def store_credentials(botname: str, credentials: dict):
    with open(get_credentials_filename(botname), mode='w') as f:
        json.dump(credentials, f)


def setup_client(botname: str):
    """ 
    Fetches new access token & secret from Twitter. Requires user input
    """
    credentials = get_credentials(botname)
    return tweepy.Client(
        consumer_key=credentials['apikey'],
        consumer_secret=credentials['apisecret'],                         
        access_token=credentials['access_token'], 
        access_token_secret=credentials['access_token_secret'])

def setup_api(botname: str):
    credentials = get_credentials(botname)
    auth = tweepy.OAuthHandler(credentials['apikey'], credentials['apisecret'])
    auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
    return tweepy.API(auth)

def create_tweet(botname: str, text: str):
    if len(text) > 280:
        raise ValueError("Tweet is too long!")

    client = setup_client(botname)
    client.create_tweet(text=text)

if __name__ == '__main__':
    botname = "gasbot"
    tweet = "tweetbot test 2"
    update_access_token(botname)