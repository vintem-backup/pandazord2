import random
import string

def randomString(stringLength=10):
    
    """Generate a random string of fixed length """
    
    letters = string.ascii_lowercase
    
    return ''.join(random.choice(letters) for i in range(stringLength))

test_table_name = randomString(10)

# 1 - create_table test

keys_dict = {'open_time': 'timestamp', 'open': 'numeric', 'high': 'numeric', 'low': 'numeric', 
             'close': 'numeric', 'volume': 'numeric'}

table_was_created = pg.create_table(test_table_name, keys_dict ,pk='open_time')

if table_was_created: print('Tabela {} criada com sucesso'.format(test_table_name))

# 2 - save_data_in_table test

import datetime

test_data = [[datetime.datetime(2017, 8, 17, 4, 0), '4261.48', '4261.48', '4261.48',
              '4261.48', '1.77518300'],
                [datetime.datetime(2017, 8, 17, 4, 1), '4261.48', '4261.48', '4261.48',
              '4261.48', '1.77518300'],
                [datetime.datetime(2017, 8, 17, 4, 2), '4261.48', '4261.48', '4261.48',
              '4261.48', '1.77518300']]

data_was_saved_in_table = pg.save_data_in_table(test_table_name, keys_dict, test_data)

if data_was_saved_in_table: print('Dados gravados na tabela {} com sucesso'.format(test_table_name))

# 3 read_records_from_table test

returned_data = pg.read_records_from_table(test_table_name)

data_successfully_read = bool(returned_data[0][0] == test_data[0][0])

if data_successfully_read: print('Dados Lidos com Sucesso')