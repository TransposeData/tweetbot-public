from datetime import datetime, timedelta
import re

from src.util.word_freq import check_word_freq
from src.abstract_bot import AbstractBot


BANNED_NAMES = ["rape"]


class ENSBot(AbstractBot):
    """
    ENS Expiring Names Bot.
    """

    def __init__(
        self, 
        name, 
        expired_messages={
            "15.62": "🚨 RARE #ENS NAME UNDER $2000! 🚨\n\n{}.eth's premium fee has fallen under $2000!\nRegister now: https://app.ens.domains/name/{}.eth/register!", 
            "16.62": "🚨 RARE #ENS NAME UNDER $1000! 🚨\n\n{}.eth's premium fee has fallen under $1000!\nRegister now: https://app.ens.domains/name/{}.eth/register!", 
            "17.62": "🚨 RARE #ENS NAME UNDER $500! 🚨\n\n{}.eth's premium fee has fallen under $500!\nRegister now: https://app.ens.domains/name/{}.eth/register!",
            "21": "🚨 RARE #ENS NAME AVAILABLE! 🚨\n\n{}.eth is now available without a premium fee!\nRegister now: https://app.ens.domains/name/{}.eth/register!"
        }):
        super().__init__(name)
        self.expired = self.load_data()
        self.expired_messages = expired_messages
        for day in expired_messages.keys():
            if type(float(day)) is float and day not in self.expired.keys():
                self.expired[day] = []


    def is_interesting(self, ens_name):
        """
        Return true if name should be posted
        """
        return (re.match(r'^[a-zA-Z0-9]{1,4}$', ens_name) or check_word_freq(ens_name, 0.4)) and ens_name not in BANNED_NAMES



    def unmarked_expired(self, extra_days: str = "0"):
        """
        Returns a list of names that are expiring.
        """
        names_to_tweet = []
        days_float = float(extra_days)
        premium_period_ends = datetime.now() - timedelta(days=90+days_float)
        
        # Get names that are expiring
        records = self.transpose.ens.records_by_date(type='expiration', order='desc', limit=50, timestamp_before=premium_period_ends)
        for record in records:
            ens_name = record.ens_name[:-4]

            # Check if the name short & has not been tweeted
            if self.is_interesting(ens_name) and ens_name not in self.expired[extra_days]:
                names_to_tweet.append(ens_name)
        return names_to_tweet


    def update(self):
        """
        Updates the bot.
        """
        print("Updating ENS bot...")

        # check each desired timerange
        for check_day in self.expired.keys():
            print("\tChecking for expired names on day " + check_day)
            names_to_tweet = self.unmarked_expired(extra_days=check_day)

            # check each name to see if it matches criteria and hasn't yet been tweeted
            for name in names_to_tweet:
                if name not in self.expired[check_day]:

                    # tweet the name!
                    tweet = self.expired_messages[check_day].format(name, name)
                    self.expired[check_day].append(name)
                    print("\tTweeting: {}".format(tweet))
                    self.tweet(tweet)

        self.update_data(self.expired)
        print("Done updating ENS bot.") 
