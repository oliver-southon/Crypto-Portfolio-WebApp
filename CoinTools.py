import os
from binance.client import Client
from currency_converter import CurrencyConverter
import pandas as pd
import json

# API DETAILS
api_key = os.environ.get('api_key')
api_secret = os.environ.get('api_secret')

# INIT CLIENT
client = Client(api_key, api_secret)

# get account details
# print(client.get_account()) 


class CoinTools():

    def getPrice(self, coin):
        price_dict = client.get_symbol_ticker(symbol=coin+"USDT")
        return price_dict.get("price")

    def getBalance(self, coin):
        balance_dict = client.get_asset_balance(asset=coin)
        return balance_dict.get("locked")

    def convertAUD(self, coin):
        price = self.getPrice(coin)
        bal = self.getBalance(coin)
        total = float(price) * float(bal)
        c = CurrencyConverter()
        return c.convert(total, "USD", "AUD")

    def getHistory(self, coin, option="csv", short=True):
        # get timestamp fo earliest date
        earliest_timestamp = client._get_earliest_valid_timestamp(coin+'USDT', '1d')
        # request klines data
        bars = client.get_historical_klines(coin+'USDT', '1d', earliest_timestamp, limit=1000) # default limit will be 500

        # remove ignore column
        for line in bars:
            del line[11:]

        if option == "csv":
            #  SAVE TO PANDAS DF
            # get first 5 cols
            if short == True:
                for line in bars:
                    del line[5:]
            coin_df = pd.DataFrame(bars, columns=['date', 'open' , 'high', 'low', 'close'])
            coin_df.set_index('date', inplace=True)
            print(coin_df.head())

            # EXPORT TO CSV
            save_path = './data/'+coin+'_bars.csv'
            if os.path.exists(save_path):
                os.remove(save_path)
            coin_df.to_csv(save_path)

            return coin_df

        if option == "json":
            with open(coin+"_bars.json", 'w') as e:
                            json.dump(bars, e)

def main():
    coinPrompt = "Enter your coin symbol: "
    shouldContinue = True
    coin = input(coinPrompt)
    while shouldContinue:
        print("""
        -- {:s} --

         >1. Get price
         >2. Get balance
         >3. Create data (csv)   
         >4. Choose different coin
         >0. Exit
        """.format(coin))
        opt = input("\nChoose an option: ")
        ct = CoinTools()
        if opt == "1":
            print("USD --", ct.getPrice(coin))
            c = CurrencyConverter()
            print("AUD --", c.convert(ct.getPrice(coin), "USD", "AUD"))
        elif opt == "2":
            print(coin, "--", ct.getBalance(coin))
            print("AUD", "--", ct.convertAUD(coin))
        elif opt == "3":
            try:
                ct.getHistory(coin)
                print("File created!")
            except:
                print("Error in making file")
        elif opt == "4":
            coin = input(coinPrompt)
        elif opt == "0":
            shouldContinue = False
        else:
            print("Invalid option. Please choose from the selection menu.")


if __name__ == "__main__":
    main()
