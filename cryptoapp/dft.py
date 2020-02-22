from cryptoapp import app
from requests import Request, Session, ConnectionError, Timeout, TooManyRedirects
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlite3
from sqlite3 import OperationalError



BASE_DATOS = './data/data.db'
MONEDAS = {'EUR': 0, 'BTC': 0, 'LTC': 0, 'XRP': 0, 'XLM': 0, 'USDT': 0, 'ETH': 0, 'EOS': 0, 'BCH': 0, 'BNB': 0, 'TRX': 0, 'ADA': 0, 'BSV': 0}
API_KEY= app.config['API_KEY']



def cartera():
    conn = sqlite3.connect(BASE_DATOS)
    cursor = conn.cursor()
    query = "SELECT * from movements;"
    try:
        filas = cursor.execute(query)
    except OperationalError:
        return True

    euros_invertidos = 0

    for fila in filas:
        if fila[3] == 'EUR' and fila[5] == 'BTC':
            MONEDAS['BTC'] += fila[6]
            euros_invertidos += fila[4]
        if fila[3] == 'BTC' and fila[5] == 'EUR':
            MONEDAS['BTC'] -= fila[4]
            euros_invertidos -= fila[6]
        if fila[3] == 'BTC' and fila[5] != 'EUR':
            MONEDAS['BTC'] -= fila[4]
            MONEDAS[fila[5]] += fila[6]
        if fila[3] != 'BTC' and fila[3] != 'EUR':
            MONEDAS[fila[3]] -= fila[4]
            MONEDAS[fila[5]] += fila[6]

    conn.close()

    return MONEDAS, euros_invertidos

def tablaCryptos():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

    parameters = {
        'symbol' : 'BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX'
    }

    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    if data['status']['error_message'] != None:
        return False
    else:
        conn = sqlite3.connect(BASE_DATOS)
        cursor = conn.cursor()
        try:
            query = "INSERT into cryptos (id, symbol, name) values(?, ?, ?);"
        except:
            return False
        for insert in data['data']:
            cursor.execute(query, (insert['id'], insert['symbol'], insert['name']))
        conn.commit()
        conn.close()
        return True
    
def consultaApi(desde, convertir_a, cuantia):
    url_consulta = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
    parametros = {'amount': cuantia, 'symbol': desde, 'convert': convertir_a}

    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    session = Session()
    session.headers.update(headers)
    
    try:
        respuesta = session.get(url_consulta, params=parametros)
        consulta = json.loads(respuesta.text)
    except(ConnectionError, Timeout, TooManyRedirects) as e2:
        print(e2)

    if consulta['status']['error_message'] != None:
        consulta = False

    return consulta

def inversion():
    MONEDAS = cartera()
    if MONEDAS == True:
        return True

    euros_invertidos = MONEDAS[1]
    valor_actual = 0

    for clave, valor in MONEDAS[0].items():
        if clave == 'EUR' or valor == 0:
            pass
        else:
            conversion = consultaApi(clave, 'EUR', valor)
            if conversion == False:
                valor = False
                return valor
            valor_actual += conversion['data']['quote']['EUR']['price']

        '''
        if fila[3] == 'BTC' and fila[5] == 'EUR':
            conversion = consultaApi(clave, 'EUR', MONEDAS[clave])
            MONEDAS[fila[3]] -= fila[4] 
            MONEDAS['EUR'] += conversion[0]['data']['quote']['EUR']['price']
        
            pass
    
            conversion = consultaApi('BTC', 'EUR', fila[4])
        '''

    return euros_invertidos, valor_actual

