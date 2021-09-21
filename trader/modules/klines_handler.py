#TODO: Docstrings and Type annotations

from pgmask.dataframelayer import DataframeLayer
import pandas as pd

#Production
#POSTGRES_USER = os.environ['POSTGRES_USER']
#POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
#DB_HOST = os.environ['DB_HOST']
#PG_PORT = os.environ['PG_PORT']
#POSTGRES_DB = os.environ['POSTGRES_DB']

#Dev-new    
POSTGRES_USER = 'pandazord'
POSTGRES_PASSWORD = 'QBBV9E%pcYKHUcjj'
DB_HOST = 'localhost'
PG_PORT = 5432
POSTGRES_DB = 'pandazord_database'

class OneMinuteCandlesAmount:

    def __init__(self, out_candle_interval):
        
        number_of_one_minute_candles = {'1m':1, '3m':3, '5m':5, '15m':15, '30m':30, '1h':60, 
        '2h':120, '4h':240, '6h':360, '12h':720, '1d':1440, '1w':10080}
        
        #TODO: Adicionar teste para verificar se o intevalo está no dicionário (raise KeyError)
        
        self.per_out_candle = number_of_one_minute_candles[out_candle_interval]

    
    def total(self, out_candle_number):

        return (out_candle_number + 1)*self.per_out_candle

class Transform:

    def __init__(self, klines_in):

        self.klines_in = klines_in

    #TODO: Adicionar teste para verificação se a kline é de 1m    
    def from_1m_to(self, out_candle_interval):
        
        if (out_candle_interval == '1m'):

            klines = self.klines_in
            return klines
        
        else:
        
            klines = pd.DataFrame(columns = ['open_time', 'open', 'high', 'low', 'close', 'volume'])

            slice_size = OneMinuteCandlesAmount(out_candle_interval).per_out_candle

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

    
class BinanceFromDb(object):
    
    def __init__(self):

        self.PGDF = DataframeLayer(POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, PG_PORT, POSTGRES_DB)
    
    def latest_one_minute(self, asset_symbol, number_of_one_minute_entries):
        
        table_name = 'binance_klines_' + asset_symbol + '_1m'
        
        return self.PGDF.latest_entries(table_name, field_key = 'open_time', 
                                        number_entries = number_of_one_minute_entries)


    def all_latest_one_minute(self, asset_symbol):

        table_name = 'binance_klines_' + asset_symbol + '_1m'
        
        return self.PGDF.latest_entries(table_name)
    
    
    def get_latest(self, asset_symbol, candle_interval, number_of_candles):
            
        number_of_entries = OneMinuteCandlesAmount(candle_interval).total(number_of_candles)
        
        klines_in = self.latest_one_minute(asset_symbol, number_of_entries)
        
        klines = Transform(klines_in).from_1m_to(candle_interval)

        return klines[:number_of_candles]