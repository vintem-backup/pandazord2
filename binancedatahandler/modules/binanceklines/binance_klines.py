#TODO: Docstrings and type annotations

import requests
import json
import time
from datetime import datetime
from copy import deepcopy

import sys
sys.path.append('..')
from modules.useful_functions import *

def binance_server_time():

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

        for i in range(self.max_attempts):

            try:

                response = requests.get(url)

                response.raise_for_status()

            except (Exception, requests.exceptions.RequestException) as error: #TODO: TRATAR EXCEÇÃO AQUI

                time.sleep(5)

            finally:

                if (int(response.status_code) == 200): raw_klines = response.json(); break
            
        return raw_klines


    def _format(self, klines_in):

        def clear_columns_and_adjust_time_and_prices_and_volume_on(klines_in):

            klines_out = []

            delta = delta_time_in_exact_seconds_from_hours_between_utc_and(binance_server_time())
            
            for i in range (len(klines_in)):

                data = [datetime.fromtimestamp(int(klines_in[i][0]/1000) + delta), #open_time
                        float(klines_in[i][1]), #Open
                        float(klines_in[i][2]), #High
                        float(klines_in[i][3]), #Low
                        float(klines_in[i][4]), #Close
                        float(klines_in[i][5]) #volume
                        ]

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
        
        klines_adjusted = clear_columns_and_adjust_time_and_prices_and_volume_on(klines_in)
        
        klines = making_seconds_be_zero_on(klines_adjusted)
        
        return klines