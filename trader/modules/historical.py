from pgmask.dataframelayer import DataframeLayer as PG_DF
from pgmask.basiclayer import BasicLayer as PG_BL

def get_historical_name(exchange_name, asset_symbol, operational_parameters):
    
    table_name = exchange_name + asset_symbol + operational_parameters[\
        'candle_interval'] + operational_parameters['price_source']
    
    strategy_part_name = operational_parameters['strategy']['name']
    for parameter in operational_parameters['strategy']['parameters']:

        for item in operational_parameters['strategy']['parameters'][parameter]:
            strategy_part_name = strategy_part_name + str(item)

    stop_part_name = operational_parameters['stop_loss']['name']
    for parameter in operational_parameters['stop_loss']['parameters']:

        for item in operational_parameters['stop_loss']['parameters'][parameter]:
            stop_part_name = stop_part_name + str(item)
    
    table_name = table_name + strategy_part_name + stop_part_name
    
    return table_name


class Historical:
    
    def __init__(self, historical_table_name, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
        
        self.name = historical_table_name
        self.PGDF = PG_DF(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
        self.PGBL = PG_BL(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
        self.keys_dict = {'open_time': 'timestamp', 'price': 'numeric', 'side': 'char(4)'}
    
    def get(self):
        
        try:
            
            historical = self.PGDF.latest_entries(self.name)

        except:
            
            self.PGBL.create_table(self.name, self.keys_dict, pk = 'open_time')
        
            historical = self.PGDF.latest_entries(self.name)
        
        return historical
    
    def save_df(self, data):
        
        self.PGDF.save_df_into_db(self.name, data, if_exists='append', index='opentime')

    def save_like_list(self, data):
        
        hist_list = []
        for i in range(len(data)):
            
            hist_list.append(list(data.iloc[i]))
            
        self.PGBL.save_data_in_table(self.name, self.keys_dict, hist_list)
    
    def create_minimal(self):
        pass