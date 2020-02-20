import pandas as pd
import psycopg2

class DataframeFromDb:
    
    def __init__(self, DB_HOST, DB_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD):
        
        super().__init__()
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT
        self.POSTGRES_DB = POSTGRES_DB
        self.POSTGRES_USER = POSTGRES_USER
        self.POSTGRES_PASSWORD = POSTGRES_PASSWORD

    def get(self, sql_query):
        
        try:
        
            dataframe = pd.DataFrame()

            with psycopg2.connect("host={} port={} dbname={} user={} password={}".\
                                  format(self.DB_HOST, 
                                         self.DB_PORT, 
                                         self.POSTGRES_DB, 
                                         self.POSTGRES_USER, 
                                         self.POSTGRES_PASSWORD)) as connection:

                reversed_dataframe = pd.read_sql(sql_query, connection, index_col=None,coerce_float=True,
                                                 params=None, parse_dates=None, columns=None, chunksize=None)

                dataframe = reversed_dataframe.sort_values(by = ['open_time'], 
                                                                   axis=0,
                                                                   ascending=True, 
                                                                   inplace=False, 
                                                                   kind='quicksort', 
                                                                   na_position='last', 
                                                                   ignore_index=True)

            return dataframe
        
        except Exception as err:
            
            table_not_found = bool(("relation" and "does not exist") in str(err))
            
            if (table_not_found): raise Exception('Table not found')


class PriceSeriesFrom:
    
    def __init__(self, market_df):
        
        super().__init__()
        self.market_df = market_df
    
    def open_(self):
        return self.market_df['open']
    
    def high_(self):
        return self.market_df['high']
    
    def low_(self):
        return self.market_df['low']
    
    def close_(self):
        return self.market_df['close']
    
    def ohlc4_(self):
        
        price = (self.market_df['open'] +
                self.market_df['high'] +
                self.market_df['low'] +
                self.market_df['close'])/4
        
        return price
    
    def hl2_(self):
        
        price = (self.market_df['high'] +
                self.market_df['low'])/2
        
        return price
    
    def hlc3_(self):
        
        price = (self.market_df['high'] +
                self.market_df['low'] +
                self.market_df['close'])/3
        
        return price