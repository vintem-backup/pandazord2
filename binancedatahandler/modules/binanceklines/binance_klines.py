#binance_handler.py

import requests
import requests
import json
import time
from datetime import datetime
from copy import deepcopy
#import delta_time_in_seconds_between_utc_and

def server_time():

    binance_time = datetime.fromtimestamp(int((requests.get('https://api.binance.com/api/v1/time').\
                                               json()['serverTime'])/1000))

    return binance_time


class GetKlines:
    
    def __init__(self, asset_symbol, candle_interval, start_time, max_attempts):
        
        self.asset_symbol = asset_symbol
        self.candle_interval = candle_interval
        self.start_time = start_time
        self.max_attempts = max_attempts
  
    
    def formated(self):
        
        klines = []
        
        for i in range(5):

            raw_klines = self.raw()

            if(raw_klines): klines = self._format(raw_klines); break

            else: time.sleep(2)
        
        return klines
    
    
    def raw(self):
        
        raw_klines = []

        url = '''https://api.binance.com/api/v1/klines?symbol=\
''' + self.asset_symbol + '''&interval=''' + self.candle_interval +\
'''&startTime=''' + self.start_time

        for i in range(max_attempts):

            try:

                response = requests.get(url)

                response.raise_for_status()

            except (Exception, requests.exceptions.RequestException) as error: #TODO: TRATAR EXCEÇÃO AQUI

                time.sleep(5)

            finally:

                if (int(response.status_code) == 200): raw_klines = response.json(); break
            
        return raw_klines
    
    def is_there_missing_data_in(klines_in):
        pass
    
    
    def _format(self, klines_in):
        
        def completing_missing_data_on_1_minute_candle():
            pass

        def clear_and_adjust_time_prices_and_volume_of(klines_in):

            klines_out = []

            delta = delta_time_in_seconds_between_utc_and(server_time())
            
            for i in range (len(klines_in)):

                open_time = datetime.fromtimestamp(int(klines_in[i][0]/1000) + delta)
                
                volume =  (float(klines_in[i][5]))

                data = [open_time,
                        float(klines_in[i][1]), #Open
                        float(klines_in[i][2]), #High
                        float(klines_in[i][3]), #Low
                        float(klines_in[i][4]), #Close
                        volume]

                klines_out.append(data)

            return klines_out

        def making_seconds_be_zero_on(klines_in):

            klines_out = deepcopy(klines_in)

            for i in range(len(klines_in)):

                entry = klines_in[i][0]

                if (entry.second != 0):

                    out = datetime.fromtimestamp((datetime.timestamp(entry) - entry.second))

                    klines_out[i][0] = out

            return klines_out
        
        klines = clear_and_adjust_time_prices_and_volume_of(klines_in)
        
        klines = making_seconds_be_zero_on(klines)
        
        return klines