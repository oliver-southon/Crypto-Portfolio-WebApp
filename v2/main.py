import os
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
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

# >3. FLASK ROUTES
@app.route('/<int:id>', methods=['POST', 'GET'])
def delete_holding(id):
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
    for row in data:
        display_data_row = []

        value = ct.getCurVal(row.symbol, row.entry_price, row.entry_amt)
        pl = ct.getPL(row.symbol, row.entry_price, row.entry_amt)
        pl_percent = ct.getPLPercent(row.symbol, row.entry_price, row.entry_amt)

        display_data_row.append(row.holding_id) #               0 - INDEX NUMBER
        display_data_row.append(value) #                        1 - CUR VALUE
        display_data_row.append(pl) #                           2 - PL
        display_data_row.append(pl_percent) #                   3 - PL percent
        display_data_row.append(row.symbol) #                   4 - Coin Name
        display_data_row.append(ct.getPrice(row.symbol)) #      5 - Current Price
        display_data_row.append(row.entry_amt) #                6 - Entry Price
        display_data_row.append(row.entry_price) #              7 - Entry Amt
        display_data_row.append(row.date) #                     8 - Date

        display_data.append(display_data_row)
        

    return render_template('index2.html', form=form, holdings=display_data)

# >4. MAIN
if __name__ == "__main__":
    app.run(debug=True)

