import cryptocompare as cc

def get_price(coin):
    return cc.get_price(coin, 'USD')[coin]['USD']

def get_cur_val(coin, entry_price, entry_amount):
    cur_val = round((entry_amount / entry_price) * float(get_price(coin)),2)
    return cur_val

def get_PL(coin, entry_price, entry_amount):
    cur_val = (entry_amount / entry_price) * float(get_price(coin))
    difference = round(cur_val - entry_amount,2)
    return difference

def get_PL_Percent(coin, entry_price, entry_amount):
    cur_val = (entry_amount / entry_price) * float(get_price(coin))
    difference = cur_val - entry_amount
    percent_change = round((((difference)/ entry_amount) * 100),2)
    return percent_change
    