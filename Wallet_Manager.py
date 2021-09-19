import os.path
from binance.client import Client
from currency_converter import CurrencyConverter
import pandas as pd
import json
import pickle

from CoinTools import CoinTools 

class bcolors:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    HEADER = "\033[95m"

    BOLD = "\033[1m"

ct = CoinTools()
# API DETAILS
api_key = os.environ.get('api_key')
api_secret = os.environ.get('api_secret')

# INIT CLIENT
client = Client(api_key, api_secret)

 # Save/Load Data
def saveHoldings(obj):
    try:
        if not os.path.isdir("saves"):
            os.makedirs("saves")
        with open("./saves/holdings.pickle", "wb") as f:
            pickle.dump(obj, f)
    except:
        print("Could not save Data")

def loadHoldings():
    try:
        with open("./saves/holdings.pickle", "rb") as f:
            obj = pickle.load(f)
            return obj
    except:
        print("Could not load data")

class Wallet():
    def __init__(self):
        # Placeholders
        self.holdings = {}

    # Setters/Getters
    def displayWallet(self):
        print(bcolors.BOLD + "   COIN     S_AMT   S_PRICE    CUR_VAL\n ========================================" + bcolors.RESET)
        for key, item in self.holdings.items():
            start_amount = float(item[0])
            start_price = float(item[1])

            cur_val = round((start_amount / start_price) * float(ct.getPrice(key)),3)
            if cur_val < start_amount:
                cur_val = bcolors.RED + str(cur_val)
            elif cur_val > start_amount:
                cur_val = bcolors.GREEN + str(cur_val)
            print(" | {} - {}    | {} \033[0m|".format(key, item, cur_val))

    # Edit Holdings
    def addHolding(self, coin, in_amount):
        self.holdings[coin] = [in_amount, round(float(ct.getPrice(coin)),3)]

    def addHoldingManual(self, in_amount, coin, price):
        self.holdings[coin] = [in_amount, price]

    def removeHolding(self, coin):
        self.holdings.pop(coin)

if __name__ == "__main__":
    wallet = loadHoldings()

    should_continue = True
    while should_continue:
        try:
            choice = int(input("""
            -- WALLET MANAGER --
            
            >1. View Holdings
            >2. Add Holding
            >3. Add Holding manually
            >4. Remove Holding
            >0. Exit
            >9. Exit without saving
            
            Choose here: """))

            if choice == 1:
                print("opt 1")
                wallet.displayWallet()
            elif choice == 2:
                coin = input("Enter coin symbol: ")
                in_amount = input("Enter amount put in (USDT): ")
                wallet.addHolding(coin, in_amount)
            elif choice == 3:
                coin = input("Enter coin symbol: ")
                in_amount = input("Enter amount put in (USDT): ")
                price = input("Enter price at purchase (USDT): ")
                wallet.addHolding(coin, in_amount)
            elif choice == 4:
                coin = input("Enter coin symbol: ")
                wallet.removeHolding(coin)
            elif choice == 0:
                saveHoldings(wallet)
                print("Wallet saved. Goodbye!")
                should_continue = False
            elif choice == 9:
                print("Exiting without saving...")
                should_continue = False
            
        except ValueError:
            print("Please give an integer value")

