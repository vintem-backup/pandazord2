import requests
from datetime import datetime

class BinanceKlines:
    
    def __init__(self, asset_symbol, candle_interval, max_attempts):
        
        self.asset_symbol = asset_symbol
        self.candle_interval = candle_interval
        self.max_attempts = max_attempts

    
    def get_from(self, start_time):
        
        self.start_time = start_time
        
        raw_klines = []

        url = '''https://api.binance.com/api/v1/klines?symbol=\
''' + self.asset_symbol + '''&interval=''' + self.candle_interval +\
'''&startTime=''' + self.start_time

        for i in range(self.max_attempts):

            try:

                response = requests.get(url)

                response.raise_for_status()
                
                if (int(response.status_code) == 200): raw_klines = response.json(); break

            except (Exception, requests.exceptions.RequestException) as error: #TODO: TRATAR EXCEÇÃO AQUI
                
                time.sleep(5) 
            
        return raw_klines

    
    def get_from_to(self):
        pass


def binance_server_time():

    binance_time = datetime.fromtimestamp(int((requests.get('https://api.binance.com/api/v1/time').\
                                               json()['serverTime'])/1000))

    return binance_time


def test_binance_request_limit():
    
    requests_limit_reached = True #Default
    
    for i in range(5):
        
        try:

            response_ping = requests.get('https://api.binance.com/api/v1/ping')
            
            #False if X-MBX-USED-WEIGHT < 1100
            requests_limit_reached = bool(int(response_ping.headers['X-MBX-USED-WEIGHT']) >= 1100)
            
            if not (requests_limit_reached): break
        
        except (Exception, requests.exceptions.RequestException) as error: #TODO: TRATAR EXCEÇÃO AQUI
            
            time.sleep(2)

    return requests_limit_reached