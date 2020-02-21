#TODO: Docstrings and Type annotations

import pandas as pd

from common_libs import DataframeFromDb

class OneMinuteNumber:

    def __init__(self, out_candle_interval):
        
        number_of_one_minute_candles = {'3m':3, '5m':5, '15m':15, '30m':30, '1h':60, '2h':120, 
                                             '4h':240, '6h':360, '12h':720, '1d':1440, '1w':10080}
        
        #TODO: Adicionar teste para verificar se o intevalo está no dicionário (raise KeyError)
        
        self.per_out_candle = number_of_one_minute_candles[out_candle_interval]

    
    def total_entrys(self, out_candle_number):

        return out_candle_number*self.per_out_candle

class TransformFromOneMinute:

    def __init__(self, klines_in):

        self.klines_in = klines_in

        
    def to(self, out_candle_interval):
        
        klines = pd.DataFrame(columns = ['open_time', 'open', 'high', 'low', 'close', 'volume'])

        slice_size = OneMinuteNumber(out_candle_interval).per_out_candle

        end_index = len(self.klines_in); start_index = end_index - slice_size; i = 0

        while end_index > slice_size:

            work_klines = pd.DataFrame()
            work_klines = work_klines.append(self.klines_in.iloc[start_index:end_index], ignore_index=True)

            klines.loc[i, 'open_time'] = work_klines.loc[0, 'open_time']
            klines.loc[i, 'open'] = work_klines.loc[0, 'open']
            klines.loc[i, 'high'] = work_klines['high'].max()
            klines.loc[i, 'low'] = work_klines['low'].min()
            klines.loc[i, 'close'] = work_klines.loc[slice_size - 1, 'close']
            klines.loc[i, 'volume'] = work_klines['volume'].sum()

            i+=1; start_index-=slice_size; end_index-=slice_size

        return klines.sort_values(by = ['open_time'], axis=0, ascending=True, inplace=False, 
                                  kind='quicksort', na_position='last', ignore_index=True) 

    
class BinanceFromDb(DataframeFromDb):
    
    def __init__(self, DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD):
        
        super().__init__(DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
    

    def get_dataframe_one_minute_by_sql(self, sql_query):
        
        return super().get(sql_query)
    
    
    def latest_one_minute(self, asset_symbol, number_of_one_minute_entries):
        
        table_name = 'binance_klines_' + asset_symbol + '_1m'
        
        field_key = 'open_time'

        sort_type = 'DESC'

        limit = str(number_of_one_minute_entries)
        
        sql_basic_select_query = 'SELECT * FROM ' + table_name

        sql_query = sql_basic_select_query + ' ORDER BY ' + field_key + ' ' + sort_type + ' LIMIT ' + limit
        
        return self.get_dataframe_one_minute_by_sql(sql_query)

    
    def all_latest_one_minute(self, asset_symbol):

        table_name = 'binance_klines_' + asset_symbol + '_1m'

        sql_query = 'SELECT * FROM ' + table_name
        
        return self.get_dataframe_one_minute_by_sql(sql_query)

    
    def get_latest(self, asset_symbol, candle_interval, number_of_candles):
        
        if (candle_interval == '1m'):

            klines = self.latest_one_minute(asset_symbol, number_of_candles)

        else:
            
            number_of_entries = OneMinuteNumber(candle_interval).total_entrys(number_of_candles)
            
            klines_in = self.latest_one_minute(asset_symbol, number_of_entries)
            
            klines = TransformFromOneMinute(klines_in).to(candle_interval)
    
        return klines