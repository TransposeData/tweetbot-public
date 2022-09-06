import statistics
import pandas as pd

from datetime import datetime, timedelta, timezone
from src.abstract_bot import AbstractBot
from transpose.extras import Plot


class GasBot(AbstractBot):
    """
    Gas Tracking Bot.
    """

    def __init__(self, name):
        super().__init__(name)
        data = self.load_data()
        if 'gas_price' not in data:
            self.update_data({
                "gas_price": 0.001,
                "last_hourly_post": datetime.now().isoformat()
            })
            self.last_gas_price_alerted = 0.001
        else:
            self.last_gas_price_alerted = self.load_data()['gas_price']
        
    def update(self):
        """
        Updates the bot.
        """
        print("Updating gas values...")
        
        # get all blocks from the last hour
        mined_after=(datetime.now() - timedelta(minutes=60)).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        historical_blocks = self.transpose.block.blocks_by_date(mined_after=mined_after, order="desc", limit=500)
                
        historical_base_gas_prices = [block.base_fee_per_gas / 1000000000 for block in historical_blocks]
        average_gas_prices = (statistics.mean(historical_base_gas_prices))
        last_block_gas_price = historical_base_gas_prices[0]
        percent_change = ((last_block_gas_price - average_gas_prices) / average_gas_prices) * 100
        percent_change_from_storage = ((last_block_gas_price - self.last_gas_price_alerted) / self.last_gas_price_alerted) * 100

        # calculate moving average for smoothing graph
        historical_base_gas_prices = pd.Series(historical_base_gas_prices).rolling(20).mean().tolist()
        
        # if timedifference between now and last storage value > 1 hour
        if datetime.fromisoformat(self.load_data()['last_hourly_post']) + timedelta(hours=1) < datetime.now():
            self.update_data({
                "gas_price": self.load_data()['gas_price'],
                "last_hourly_post": datetime.now().isoformat()
            })

            chart = Plot(title="Hourly Gas Prices on Ethereum")
            chart.add_data(
                data={
                    "x": pd.date_range(historical_blocks[0].timestamp, historical_blocks[-1].timestamp, periods=len(historical_base_gas_prices)),
                    "y": historical_base_gas_prices,
                    "x_axis": "Time",
                    "y_axis": "Gas Price (Gwei)",
                },
                smoothing=1,
                type="bar")
            chart.render("./images/gas_price_hourly.png")

            # self.tweet_image("Hourly #Ethereum Gas Price Summary\n\n⛽ Average Price: {:0.2f} Gwei\n🤑Current Price: {:0.2f} Gwei\n\nFollow me for #ETH gas price alerts!".format(average_gas_prices, last_block_gas_price), 
                            #  "./images/gas_price_hourly.png")
            
        
        if (percent_change >= 30 or percent_change <= -25) and abs(percent_change_from_storage) >= 15:
            # update the storage
            self.update_data({
                "gas_price": last_block_gas_price,
                "last_hourly_post": self.load_data()['last_hourly_post']
            })
            
            # Tweet the data
            tweet_text_content = '🚨 #Ethereum gas prices are {} {:0.2f}% in the last hour!\n\n⛽ Current Price: {:0.2f} Gwei\n\nFollow me for #ETH gas price alerts!'.format(
                "up" if percent_change > 0 else "down",
                percent_change, 
                last_block_gas_price
            )
            
            print(tweet_text_content)
            
            self.tweet(tweet_text_content)
