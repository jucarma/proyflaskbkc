from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, HiddenField, SelectField, IntegerField, DecimalField, FloatField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from wtforms.widgets import Select
from .dft import cartera


CHOICES = (('EUR', 'Euros'), ('BTC', 'Bitcoin'), ('LTC', 'Litecoin'), ('XRP', 'XRP'), ('XLM', 'Stellar'), ('USDT', 'Tether'), ('ETH', 'Ethereum'), ('EOS', 'EOS'), ('BCH', 'Bitcoin Cash'), ('BNB', 'Binance Coin'), ('TRX', 'Tron'), ('ADA', 'Cardano'), ('BSV', 'Bitcoin SV'))

CRYPTOS = dict(CHOICES)

MONEDAS = {'EUR': 0, 'BTC': 0, 'LTC': 0, 'XRP': 0, 'XLM': 0, 'USDT': 0, 'ETH': 0, 'EOS': 0, 'BCH': 0, 'BNB': 0, 'TRX': 0, 'ADA': 0, 'BSV': 0}


def cantidad_disp(form, field):
    disponible = cartera()
    if form.desde.data == 'BTC' and form.convertir_a.data != 'EUR':
        if disponible[0][form.desde.data] < form.cuantia.data:
            raise ValidationError('No tienes BTC')
    if form.desde.data != 'EUR':
        if disponible[0][form.desde.data] < form.cuantia.data:
            raise ValidationError('No tienes las monedas necesarias')
    if disponible == True:
        raise ValidationError('DB ERROR, try again.')

    
def error_igual(form, field):
    if form.convertir_a.data == form.desde.data:
        raise ValidationError('From y To han de ser distintos')


def error_quantity(form, field):
    if form.cuantia.errors:
        raise ValidationError('Solo acepta numeros')


def error_crypto(form, field):
    if form.desde.data != 'BTC' and form.convertir_a.data == 'EUR':
        raise ValidationError('A Euros solo se pueden cambiar los BTC')


def error_nobtc(form, field):
    if form.desde.data == 'EUR' and form.convertir_a.data != 'BTC':
        raise ValidationError('Con Euros solo se pueden comprar BTC')




class CryptoForm(FlaskForm):
    
    desde = SelectField('From', validators=[DataRequired(), error_igual, error_nobtc], choices=CHOICES, id="state")
    convertir_a = SelectField('To', validators=[DataRequired(), error_igual, error_crypto], choices=CHOICES)
    cuantia = DecimalField('Q', validators=[InputRequired(), error_quantity, cantidad_disp])
    
    calc = SubmitField('Calcular')
    
    ok = SubmitField('Ok')
    
    
    