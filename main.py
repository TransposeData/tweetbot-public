import time
import importlib
import inspect
import os
import traceback

from src.util.auth import *
from src.abstract_bot import AbstractBot


def initialize_bots():
    """
    Collects and initializes bots in src/bots.
    """
    bots = {}

    # Get list of files in bot dir
    bot_path = "src/bots"
    py_files = [f[:-3] for f in os.listdir(bot_path) if f.endswith('.py') and f != '__init__.py']

    # go through every file
    for py_file in py_files:

        try:
            # import the module
            bot_module = importlib.import_module(bot_path.replace('/', '.') + "." + py_file)

            # get all classes in the module
            for name, obj in inspect.getmembers(bot_module):
                if inspect.isclass(obj) and issubclass(obj, AbstractBot) and obj != AbstractBot:
                    bots[obj.__name__] = obj(obj.__name__)
        except Exception as e:
            print("Error importing bot (Alex shit himself): {}".format(py_file))
            traceback.print_exc()
            print(e)
 
    print("Found {} bots".format(len(bots)))
    return bots


def run_bot_updates(seconds):
    """
    Runs the bot updates.
    """
    while True:
        
        # initialize bots, will allow for changes without restarting 
        # the entire script, as well as pick up crashed bots
        bots = initialize_bots()
        
        print("Running bot updates: {}".format(time.strftime("%H:%M:%S")))
        for bot in bots.values():
            try:
                bot.update()
            except Exception as e:
                print("Error updating bot: {}".format(bot.name))
                print(e)

        print("Updates complete, sleeping for {} seconds".format(seconds))
        time.sleep(seconds)


if __name__ == '__main__':
    run_bot_updates(seconds=1200)