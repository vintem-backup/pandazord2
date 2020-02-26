from pgmask.dataframelayer import DataframeLayer
from pgmask.basiclayer import BasicLayer

class AssetsHandler:

    def __init__(self, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, 
    DB_NAME, exchange_name, asset_symbol):

        self.PGDF = DataframeLayer(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
        self.PGBL = BasicLayer(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
        self.exchange_name = exchange_name
        self.asset_symbol = asset_symbol
    

    def info(self):

        return self.PGDF.read_entries_list((self.exchange_name + '_assets'), 
        'asset_symbol', self.asset_symbol.split(sep=','))
    

    def update(self, field, update_to):

        update_status = self.PGBL.update_entry(table_name = self.exchange_name + '_assets', 
        pk_field = 'asset_symbol', 
        pk_value = self.asset_symbol, 
        field_to_update = field, 
        new_field_value = update_to)

        return update_status