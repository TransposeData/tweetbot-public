import os
import json

from abc import abstractmethod
from transpose import Transpose
from dotenv import load_dotenv
from tweepy.errors import Forbidden

from src.util.auth import setup_client, setup_api, update_access_token


# Get TRANSPOSE_KEY from dotenv
env = load_dotenv()
TRANSPOSE_KEY = os.environ.get('TRANSPOSE_KEY')
DATA_DIR = 'data/'


class AbstractBot():
    """
    Abstract class for bots.
    """

    def __init__(self, name):
        self.name = name
        self.client = setup_client(name)
        self.api = setup_api(name)
        self.transpose = Transpose(TRANSPOSE_KEY)
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(DATA_DIR+self.name+'.json'):
            self.update_data({})
    

    def update_data(self, data):
        """
        Updates the data.
        """
        with open(DATA_DIR + self.name + '.json', 'w') as f:
            json.dump(data, f)


    def load_data(self):
        """
        Loads the data.
        """
        with open(DATA_DIR + self.name + '.json', 'r') as f:
            return json.load(f)


    def update_access_token(self):
        """
        Updates the access token.
        """
        update_access_token(self.name)


    def tweet(self, tweet):
        """
        Tweets the tweet.
        """
        self.client.create_tweet(text=tweet)
        
    def tweet_image(self, tweet, filename):
        """
        Tweets the tweet with an image.
        """
        try:
            self.api.update_status_with_media(status=tweet, filename=filename)
        except Forbidden as e:
            print(e)

    @abstractmethod
    def update(self):
        """
        Generic update function. This should be overriden in inheriting bots.
        """
        raise NotImplementedError("update() not implemented")
