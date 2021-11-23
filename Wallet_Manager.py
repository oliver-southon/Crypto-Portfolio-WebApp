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
        print("No wallet found. Created new one.")

# Utility for Duplicates
def addDupe(key_val, key_name):
    new_key_name = key_name
    dupes = 0
    for key in key_val:
        if key_name in key:
            dupes += 1
    if dupes > 0:
        new_key_name = key_name + str(dupes)
    return new_key_name

class Wallet():
    def __init__(self):
        # Placeholders
        self.holdings = {}
        self.sells = {}

    # Setters/Getters
    def displayWallet(self):
        tot_start_amount = 0
        tot_difference = 0

        print(bcolors.BOLD + "   COIN     S_AMT   S_PRICE    CUR_VAL\n ========================================" + bcolors.RESET)
        for key, item in self.holdings.items():
            start_amount = float(item[0])
            start_price = float(item[1])

            cur_val = round((start_amount / start_price) * float(ct.getPrice(''.join([i for i in key if not i.isdigit()]))),3)
            difference = cur_val - start_amount
            percent_change = str(round((((difference)/ start_amount) * 100),2)) + "%"
            if cur_val < start_amount:
                cur_val = bcolors.RED + str(cur_val) + " " + percent_change
            elif cur_val > start_amount:
                cur_val = bcolors.GREEN + str(cur_val) + " " + percent_change

            tot_start_amount += start_amount
            tot_difference += difference
          
            print(" | {} - {}    | {} \033[0m|".format(key, item, cur_val))


        if tot_difference < 0:
            tot_difference = bcolors.RED + str(tot_difference) + bcolors.RESET
        elif tot_difference > 0:
            tot_difference = bcolors.GREEN + str(tot_difference) + bcolors.RESET
        print("TOTAL P/L: {}".format(tot_difference))

    def displaySells(self):
        print(bcolors.BOLD + "   COIN     PROFIT    \n =====================" + bcolors.RESET)
        for key, item in self.sells.items():
            if item > 0:
                item = bcolors.GREEN + str(item)
            elif item < 0:
                item = bcolors.RED + str(item)
            print(" | {} - {} \033[0m|".format(key, item))

    # Edit Holdings/Sells
    def addHolding(self, coin, in_amount):
        key = addDupe(self.holdings, coin)
        self.holdings[key] = [in_amount, round(float(ct.getPrice(coin)),3)]
    def addHoldingManual(self, coin, in_amount, price):
        key = addDupe(self.holdings, coin)
        self.holdings[key] = [in_amount, price]

    def removeHolding(self, coin):
        self.holdings.pop(coin)

    def addSell(self, coin, before, after):
        p_l = float(after) - float(before)
        key = addDupe(self.sells, coin)
        wallet.sells[key] = p_l

if __name__ == "__main__":
    wallet = loadHoldings()
    if not wallet:
        wallet = Wallet()
    should_continue = True
    while should_continue:
        try:
            choice = int(input("""
            -- WALLET MANAGER --
            
            >1. View Holdings
            >2. Add Holding
            >3. Add Holding manually
            >4. Remove Holding
            
            >5. Add sell
            >6. View sells

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
                wallet.addHoldingManual(coin, in_amount, price)

            elif choice == 4:
                coin = input("Enter coin symbol: ")
                wallet.removeHolding(coin)

            elif choice == 5:
                coin = input("Enter coin symbol: ")
                before = input("Enter amount put in: ")
                after = input("Enter amount sold for: ")
                wallet.addSell(coin, before, after)

            elif choice == 6:
                wallet.displaySells()

            elif choice == 0:
                saveHoldings(wallet)
                print("Wallet saved. Goodbye!")
                should_continue = False

            elif choice == 9:
                print("Exiting without saving...")
                should_continue = False
            
        except ValueError:
            print("Please give an integer value")

