import numpy as np
import cryptocompare as cc
import time
from pycoingecko import CoinGeckoAPI


class Position():
    def __init__(self, inID, inSymbol, inEntryPrice, inEntryAmount, date='-', dbID=''):
        self.cg = CoinGeckoAPI()
        self.coin_id = inID
        self.symbol = inSymbol
        self.entry_price = inEntryPrice
        self.entry_amount = inEntryAmount
        self.current_price = self.get_price()
        self.current_value = self.get_cur_val()
        self.pl = self.get_PL()
        self.pl_percent = self.get_PL_Percent()
        self.date = date
        self.dbID = dbID

    def get_price(self):
        return self.cg.get_price(ids=self.coin_id.lower(), vs_currencies="usd")[self.coin_id.lower()]["usd"]

    def get_cur_val(self):
        cur_val = round(((self.entry_amount / self.entry_price) * self.current_price),2)
        return cur_val

    def get_PL(self):
        difference = round(self.current_value - self.entry_amount,2)
        return difference

    def get_PL_Percent(self):
        percent_change = round((((self.pl)/ self.entry_amount) * 100),2)
        return percent_change

    def __str__(self):
        return f'{self.dbID} - {self.symbol}: | {self.entry_price} | {self.entry_amount} | {self.current_price} | {self.current_value} | {self.pl} | {self.pl_percent} | {self.date}'

class Positions():
    def __init__(self):
        self.positions = []
        self.money_in = 0

    def add(self, inID, inSymbol, inEntryPrice, inEntryAmount, date='-', dbID=''):
        start = time.time()
        self.money_in += inEntryAmount # Increment Money put into portfolio
        position = Position(inID, inSymbol, inEntryPrice, inEntryAmount, date, dbID)
        self.positions.append(position)
        np.append(self.positions, position)
        end = time.time()
        print(f'{end-start} seconds to add holding.')
    
    def display(self):
        positions = np.asarray(self.positions)
        for position in positions:
            print(position)

    def get_cumulative_value(self):
        try:
            cumulative_value = 0
            positions = np.asarray(self.positions)
            for position in positions:
                cumulative_value += position.current_value
            return round(cumulative_value,2)
        except ZeroDivisionError:
            return 0

    def get_cumulative_pl(self):
        try:
            pl = round((self.get_cumulative_value() - self.money_in),2)
            return pl
        except ZeroDivisionError:
            return 0

    def get_cumulative_pl_percent(self):
        try:
            pl_percent = ((self.get_cumulative_value() / self.money_in - 1)) * 100
            return round(pl_percent,2)
        except ZeroDivisionError:
            return 0

class PreviousPosition():
    def __init__(self, inID, inSymbol, inEntryPrice, inEntryAmount, inExitPrice, date='-', inExitDate='-', dbID=''):
        self.coin_id = inID
        self.symbol = inSymbol
        self.entry_price = inEntryPrice
        self.entry_amount = inEntryAmount
        self.date = date
        self.exit_price = inExitPrice
        self.exit_date = inExitDate
        self.dbID = dbID

        self.value_sold = self.get_value_sold()
        self.pl = self.get_PL()
        self.pl_percent = self.get_PL_Percent()

    def get_value_sold(self):
        sold_val = round(((self.entry_amount / self.entry_price) * self.exit_price),2)
        return sold_val

    def get_PL(self):
        difference = round(self.value_sold - self.entry_amount,2)
        return difference

    def get_PL_Percent(self):
        percent_change = round((((self.pl)/ self.entry_amount) * 100),2)
        return percent_change

    def __str__(self):
        return f'{self.symbol}: | {self.entry_price} | {self.entry_amount} | {self.current_price} | {self.current_value} | {self.pl} | {self.pl_percent} | {self.date}'

class PreviousPositions():
    def __init__(self):
        self.previous_positions = []
        self.money_in = 0

    def add(self, inID, inSymbol, inEntryPrice, inEntryAmount, inExitPrice, inExitDate='-', date='-', dbID=''):
        start = time.time()
        self.money_in += inEntryAmount # Increment Money put into portfolio
        position = PreviousPosition(inID, inSymbol, inEntryPrice, inEntryAmount, inExitPrice, date, inExitDate, dbID)
        self.previous_positions.append(position)
        np.append(self.previous_positions, position)
        end = time.time()
        print(f'{end-start} seconds to add holding.')
    
    def display(self):
        positions = np.asarray(self.positions)
        for position in positions:
            print(position)

    def get_cumulative_value(self):
        try:
            cumulative_value = 0
            positions = np.asarray(self.previous_positions)
            for position in positions:
                cumulative_value += position.value_sold
            return round(cumulative_value,2)
        except ZeroDivisionError:
            return 0

    def get_cumulative_pl(self):
        try:
            pl = round((self.get_cumulative_value() - self.money_in),2)
            return pl
        except ZeroDivisionError:
            return 0

    def get_cumulative_pl_percent(self):
        try:
            pl_percent = ((self.get_cumulative_value() / self.money_in - 1)) * 100
            return round(pl_percent,2)
        except ZeroDivisionError:
            return 0