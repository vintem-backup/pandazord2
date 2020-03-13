#TODO: Docstrings and Type annotations

from pgmask.dataframelayer import DataframeLayer
from pgmask.basiclayer import BasicLayer

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

class AssetsHandler:

    def __init__(self, exchange_name, asset_symbol):

        self._PGDF = DataframeLayer(POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, PG_PORT, POSTGRES_DB)
        self._PGBL = BasicLayer(POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, PG_PORT, POSTGRES_DB)
        self._exchange_name = exchange_name
        self._asset_symbol = asset_symbol
    
    def get_dataframe(self):
        
        self.asset_df = self._PGDF.read_entries_list(table_name=(self._exchange_name + '_assets'),
                                                     column_name= 'asset_symbol',
                                                     entries_list=self._asset_symbol.split(sep=','))

        return self.asset_df
    
    def operational_parameters(self):
        
        self.op_param = self.get_dataframe().iloc[0].operational_parameters
        return self.op_param

class Position:

    def __init__(self, current_position):
        self._side = current_position['side']
        self._size = current_position['size']
        self._target_price = current_position['target_price']

    @property
    def side(self):
        return self._side

    @property
    def size(self):
        return self._size

    @property
    def target_price(self):
        return self._target_price

    @side.setter
    def side(self, side_to_set):
        side_list = ['closed', 'long', 'short']
        error_message = 'Incorrect! Side must be '
        error_append = ''

        if (side_to_set not in side_list):
            for item in side_list[:-1]:
                error_append+= "'" + item + "'" + ', '

            error_message = error_message + error_append + 'or ' + "'" + side_list[-1] + "'" + '.'

            print(error_message) #TODO: Tratar exceção sem print
        else:
            self._side = side_to_set

    @size.setter
    def size(self, size_to_set):
        numerical = (isinstance(size_to_set, float) or isinstance(size_to_set, int))

        if (numerical):
            if (size_to_set < 0.0):
                print ('Invalid. Size must not be negative.') #TODO: Tratar exceção sem print

            else:
                self._size = size_to_set

        else:
            print("Invalid. Must be a numerical ('float' or 'int') type." ) #TODO: Tratar exceção sem print

    @target_price.setter
    def target_price(self, target_price_to_set):
        numerical = (isinstance(target_price_to_set, float) or isinstance(target_price_to_set, int)) 

        if (numerical):
            if (target_price_to_set < 0.0):
                print ('Invalid. Target price must not be negative.') #TODO: Tratar exceção sem print

            else:
                self._target_price = target_price_to_set

        else:
            print("Invalid. Must be a numerical ('float' or 'int') type." ) #TODO: Tratar exceção sem print

    def show(self):
        return {'side' : self._side, 'size' : self._size, 'target_price' : self._target_price}
    
    def update_with(self, new_position):
        self._side = new_position['side']
        self._size = new_position['size']
        self._target_price = new_position['target_price']

class BackingTestPosition(Position):
    pass

class RealTradePosition(Position):

    def update_with(self, new_position):
        
        super(RealTradePosition, self).update_with(new_position)
        # Save into DB method here...