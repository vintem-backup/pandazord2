#from django.db import models

import pandas as pd
import psycopg2

class KlinesFromDatabase:
    
    def __init__(self, DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD):
        
        super().__init__()
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT
        self.POSTGRES_DB = POSTGRES_DB
        self.POSTGRES_USER = POSTGRES_USER
        self.POSTGRES_PASSWORD = POSTGRES_PASSWORD
    
    
    def most_fresh_one_minute_klines_dataframe(self, asset_symbol, number_of_one_minute_entries):
        
        one_minute_klines = pd.DataFrame()
        
        table_name = 'binance_klines_' + asset_symbol + '_1m'
        
        field_key = 'open_time'

        sort_type = 'DESC'

        limit = str(number_of_one_minute_entries)
        
        sql_basic_select_query = 'SELECT * FROM ' + table_name

        sql_query = sql_basic_select_query + ' ORDER BY ' + field_key + ' ' + sort_type + ' LIMIT ' + limit

        with psycopg2.connect("host={} port={} dbname={} user={} password={}".\
                              format(self.DB_HOST, 
                                     self.DB_PORT, 
                                     self.POSTGRES_DB, 
                                     self.POSTGRES_USER, 
                                     self.POSTGRES_PASSWORD)) as connection:
            
            one_minute_reversed_klines = pd.read_sql(sql_query, connection, index_col=None, 
                                                     coerce_float=True, params=None, parse_dates=None, 
                                                     columns=None, chunksize=None)
    
            one_minute_klines = one_minute_reversed_klines.sort_values(by = ['open_time'], 
                                                                              axis=0, 
                                                                              ascending=True, 
                                                                              inplace=False, 
                                                                              kind='quicksort', 
                                                                              na_position='last', 
                                                                              ignore_index=True)
        
        return one_minute_klines

    
    def get_most_fresh_klines(self, asset_symbol, candle_interval, number_of_candles):
        
        klines = pd.DataFrame(columns = ['open_time', 'open', 'high', 'low', 'close', 'volume'])

        if (candle_interval == '1m'): 

            klines = self.most_fresh_one_minute_klines_dataframe(asset_symbol, number_of_candles)

        else:

            number_of_one_minute_candles = {'3m':3, '5m':5, '15m':15, '30m':30, '1h':60, '2h':120, 
                                        '4h':240, '6h':360, '12h':720, '1d':1440, '1w':10080}

            slice_size = number_of_one_minute_candles[candle_interval]
            
            number_of_entries = number_of_candles*slice_size

            klines_in = self.most_fresh_one_minute_klines_dataframe(asset_symbol, number_of_entries)

            start_index = 0; end_index = slice_size; i=0

            while end_index < (len(klines_in) + 1):

                work_klines = pd.DataFrame()

                work_klines = work_klines.append(klines_in.iloc[start_index:end_index], ignore_index=True)

                klines.loc[i, 'open_time'] = work_klines.loc[0, 'open_time']

                klines.loc[i, 'open'] = work_klines.loc[0, 'open']

                klines.loc[i, 'high'] = work_klines['high'].max()

                klines.loc[i, 'low'] = work_klines['low'].min()

                klines.loc[i, 'close'] = work_klines.loc[slice_size - 1, 'close']

                klines.loc[i, 'volume'] = work_klines['volume'].sum()

                i+=1; start_index+=slice_size; end_index+=slice_size

        return klines