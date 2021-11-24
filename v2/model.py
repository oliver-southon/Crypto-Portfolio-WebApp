from flask_wtf import FlaskForm 
from wtforms import SubmitField, StringField, DecimalField, validators
from packages.CoinTools import CoinTools as ct

class HoldingForm(FlaskForm): # inherits 'Form' class from flask_wtf
    symbol = StringField('symbol', [validators.DataRequired()])
    entry_price = DecimalField('entry_price', [validators.DataRequired()])
    entry_amt = DecimalField('amt', [validators.DataRequired()])
    
    submit = SubmitField('Submit')