import os
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import requests
from flask_bootstrap import Bootstrap
import packages.CoinTools as ct
from model import HoldingForm
from datetime import date
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from packages.CoinTools import CoinTools 

# >1. CONFIGURATIONS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trades.db'
app.config['SECRET_KEY'] = str(os.environ.get('DB_DK'))
Bootstrap(app)
db = SQLAlchemy(app)

ct = CoinTools()

# >2. DATABASE SETUP
class Holding(db.Model):
    holding_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    entry_amt = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return "<Symbol '{}'>\n<Entry_Price {}>".format(self.symbol, str(self.entry_price))

class Prev_Holding(db.Model):
    prev_holding_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    entry_amt = db.Column(db.Float, nullable=False)
    entry_date = db.Column(db.DateTime)
    close_price = db.Column(db.Float, nullable=False)
    close_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Symbol '{}'>\n<Entry_Price {}>\n<Close_Price {}>".format(self.symbol, str(self.entry_price), str(self.close_price))

# >3. FLASK ROUTES


@app.route('/remove_prev,<int:prev_id>', methods=['POST', 'GET'])
def remove_prev(prev_id):
    print("Yaa")
    Prev_Holding.query.filter_by(prev_holding_id=prev_id).delete()
    db.session.commit()
    return redirect(url_for('prev_trades'))

@app.route('/delete_holding,<int:id>', methods=['POST', 'GET'])
def delete_holding(id):
    # htd = holding to delete
    # npv = new previous holding
    print("naaa")
    htd = Holding.query.filter_by(holding_id=id).one()
    db.session.add(Prev_Holding(symbol=htd.symbol, entry_price=htd.entry_price, entry_amt=htd.entry_amt, entry_date=htd.date, close_price=ct.getPrice(htd.symbol), close_date=date.today()))
    Holding.query.filter_by(holding_id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    form = HoldingForm()
    if form.validate_on_submit():
        sbl = form.symbol.data
        epr = float(form.entry_price.data)
        amt = float(form.entry_amt.data)
        dte = date.today()

        new_holding = Holding(symbol=sbl, entry_price=epr, entry_amt=amt, date=dte)
        db.session.add(new_holding)
        db.session.commit()
    
    data = Holding.query.order_by(Holding.date)
    display_data = []
    cum_pl = 0
    cum_pl_perc = 0
    money_in = 0
    for row in data:
        display_data_row = []
        money_in += row.entry_amt

        value = ct.getCurVal(row.symbol, row.entry_price, row.entry_amt)
        pl = ct.getPL(row.symbol, row.entry_price, row.entry_amt)
        cum_pl += pl
        pl_percent = ct.getPLPercent(row.symbol, row.entry_price, row.entry_amt)

        display_data_row.append(row.holding_id) #               0 - INDEX NUMBER
        display_data_row.append(value) #                        1 - CUR VALUE
        display_data_row.append(pl) #                           2 - PL
        display_data_row.append(pl_percent) #                   3 - PL percent
        display_data_row.append(row.symbol) #                   4 - Coin Name
        display_data_row.append(ct.getPrice(row.symbol)) #      5 - Current Price
        display_data_row.append(row.entry_price) #                6 - Entry Price
        display_data_row.append(row.entry_amt) #              7 - Entry Amt
        display_data_row.append(row.date) #                     8 - Date

        display_data.append(display_data_row)
        

    BTC = f'{round(ct.getPrice("BTC"),2):,}'
    ETH = f'{round(ct.getPrice("ETH"),2):,}'
    cum_pl_perc = round((cum_pl / money_in) * 100)  

    fg = requests.get("https://api.alternative.me/fng/").json().get("data")[0]
    fg_num = fg['value']
    fg_class = fg['value_classification']

    return render_template('index2.html', form=form, holdings=display_data, cum_pl=round(cum_pl,2), cum_pl_perc=round(cum_pl_perc,2), BTC=BTC, ETH=ETH, fg_num=fg_num, fg_class=fg_class)

@app.route('/prev_trades', methods=['POST', 'GET'])
def prev_trades():
    BTC = f'{round(ct.getPrice("BTC"),2):,}'
    ETH = f'{round(ct.getPrice("ETH"),2):,}'

    fg = requests.get("https://api.alternative.me/fng/").json().get("data")[0]
    fg_num = fg['value']
    fg_class = fg['value_classification']

    display_data_prev = []
    cum_pl_prev = 0
    cum_pl_perc_prev = 0
    data = Prev_Holding.query.order_by(Prev_Holding.close_date)
    for row in data:
        display_data_prev_row = []
        
        value_prev = round(row.entry_amt / row.entry_price,2)

        value_total = round((value_prev) * float(row.close_price),2)
        pl_prev = round((value_total - row.entry_amt),2)
        cum_pl_prev += pl_prev
        pl_percent_prev = round((((pl_prev)/ row.entry_amt) * 100),2)
        cum_pl_perc_prev += pl_percent_prev
        
        display_data_prev_row.append(row.prev_holding_id) # 0 - INDEX NUMBER
        display_data_prev_row.append(value_total) # 1 - TOTAL VALUE
        display_data_prev_row.append(pl_prev) # 2 - PL
        display_data_prev_row.append(pl_percent_prev) # 3 - PL Percent
        display_data_prev_row.append(row.symbol) # 4 - Coin Name
        display_data_prev_row.append(row.close_price) # 5 - Sell Price
        display_data_prev_row.append(row.entry_price) # 6 - Entry Price
        display_data_prev_row.append(row.entry_amt) # 7 - Entry Amt
        display_data_prev_row.append(row.entry_date) # 8 - Buy Date
        display_data_prev_row.append(row.close_date) # 9 - Sell Date

        display_data_prev.append(display_data_prev_row)


    return render_template('prev_trades.html', BTC=BTC, ETH=ETH , prev_holdings=display_data_prev, cum_pl_prev=round(cum_pl_prev,2), cum_pl_perc_prev=round(cum_pl_perc_prev,2), fg_num=fg_num, fg_class=fg_class)

# >4. MAIN
if __name__ == "__main__":
    app.run(debug=True)

