from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import packages.CoinTools as ct
from model import HoldingForm
import datetime
import sqlite3 as sql

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)



@app.route('/foo')
def foo():
    id = request.args.get('id')
    print("ID IS: ",id)
    conn = sql.connect('trades.db')
    c = conn.cursor()
    c.execute("DELETE FROM trades WHERE holding_id={}".format(id))
    conn.commit()

@app.route('/', methods=['POST', 'GET'])
def index():
    conn = sql.connect('trades.db')
    c = conn.cursor()
    c.execute("SELECT * FROM trades")
    data = c.fetchall()

    form = HoldingForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        sbl = form.symbol.data
        epr = float(form.entry_price.data)
        emt = float(form.entry_amt.data)
        dte = str(datetime.datetime.now())

        with sql.connect('trades.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO trades(symbol, entry_price, entry_amt, date) VALUES (?,?,?,?);", (sbl, epr, emt, dte))
            conn.commit()
    return render_template('index2.html', form=form, data=data)

if __name__ == "__main__":
    app.run(debug=True)

# INSERT INTO trades
#             (symbol, entry_price, entry_amt, date) VALUES (?,?,?,?)