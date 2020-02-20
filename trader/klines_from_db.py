import pandas as pd

from modules.shared_objects import DataframeFromDb

class BinanceKlines(DataframeFromDb):
    
    def __init__(self, DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD):
        
        super().__init__(DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
    
    def latest_one_minute(self, sql_query):
        
        one_minute_klines = super().get(sql_query)
        
        return one_minute_klines    
    
    
    def the_n_latest_one_minute(self, asset_symbol, number_of_one_minute_entries):
        
        table_name = 'binance_klines_' + asset_symbol + '_1m'
        
        field_key = 'open_time'

        sort_type = 'DESC'

        limit = str(number_of_one_minute_entries)
        
        sql_basic_select_query = 'SELECT * FROM ' + table_name

        sql_query = sql_basic_select_query + ' ORDER BY ' + field_key + ' ' + sort_type + ' LIMIT ' + limit

        n_minute_klines = self.latest_one_minute(sql_query)
        
        return n_minute_klines

    
    def all_latest_one_minute(self, asset_symbol):

        table_name = 'binance_klines_' + asset_symbol + '_1m'

        sql_query = 'SELECT * FROM ' + table_name

        all_minute_klines = self.latest_one_minute(sql_query)
        
        return all_minute_klines

    
    def get_latest(self, asset_symbol, candle_interval, number_of_candles):
        
        if (candle_interval == '1m'):

            final_klines = self.the_n_latest_one_minute(asset_symbol, number_of_candles)

        else:
                    
            klines = pd.DataFrame(columns = ['open_time', 'open', 'high', 'low', 'close', 'volume'])
            
            number_of_one_minute_candles = {'3m':3, '5m':5, '15m':15, '30m':30, '1h':60, '2h':120, 
                                        '4h':240, '6h':360, '12h':720, '1d':1440, '1w':10080}

            slice_size = number_of_one_minute_candles[candle_interval]
            
            number_of_entries = number_of_candles*slice_size

            klines_in = self.the_n_latest_one_minute(asset_symbol, number_of_entries)

            end_index = len(klines_in); start_index = end_index - slice_size; i=number_of_candles

            while i > 0:

                work_klines = pd.DataFrame()

                work_klines = work_klines.append(klines_in.iloc[start_index:end_index], ignore_index=True)

                klines.loc[i, 'open_time'] = work_klines.loc[0, 'open_time']

                klines.loc[i, 'open'] = work_klines.loc[0, 'open']

                klines.loc[i, 'high'] = work_klines['high'].max()

                klines.loc[i, 'low'] = work_klines['low'].min()

                klines.loc[i, 'close'] = work_klines.loc[slice_size - 1, 'close']

                klines.loc[i, 'volume'] = work_klines['volume'].sum()

                i-=1; start_index-=slice_size; end_index-=slice_size
                
            final_klines = klines.sort_values(by = ['open_time'], axis=0, ascending=True, inplace=False, 
                                              kind='quicksort', na_position='last', ignore_index=True) 

        return final_klines