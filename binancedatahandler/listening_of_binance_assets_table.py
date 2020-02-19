#TODO: Docstrings and Type annotations

import sys
import os
import subprocess
import time
import psutil
from datetime import datetime
from iteration_utilities import duplicates, unique_everseen
from modules.postgres_handler import PostgresHandler as PG
from modules.useful_functions import *

DB_HOST = os.environ['DB_HOST']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

candle_interval = '1m'

pg = PG(DB_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)

def main():
    
    while True:

        try:

            binance_assets = pg.read_entries_from_table('binance_assets')

            if (len(binance_assets) == 0): time.sleep(1)

            else:
                
                pid_list = []

                for binance_asset in binance_assets:last_updated_by_pid

                    pid = binance_asset['last_updated_by_pid']
                    
                    pid_list.append(pid)
                    
                    oldest_open_time = (int(datetime.timestamp(
                        binance_asset['collect_data_since'])))*1000 #milisseconds

                    if (binance_asset['auto_update'] == 'ON'):

                        if not (running_this_subprocess(pid)):

                            complete_data_subprocess = subprocess.Popen([sys.executable,
                            'complete_oldest_data_so_far.py',
                            str(binance_asset['asset_symbol']),
                            candle_interval,
                            str(oldest_open_time)])

                            was_entry_updated_pid = pg.update_entry('binance_assets', 
                                                        'asset_symbol', 
                                                        str(binance_asset['asset_symbol']),
                                                        'last_updated_by_pid',
                                                        int(complete_data_subprocess.pid))

                            if not (was_entry_updated_pid): pass #TODO: Tratar exceção

                    else:

                        if(running_this_subprocess(pid)): psutil.Process(pid).kill()

                #Killing duplicated PIDs
                duplicated_pid_list = list(unique_everseen(duplicates(pid_list)))
                
                if (len(duplicated_pid_list) > 0):

                    for duplicated_pid in duplicated_pid_list:

                        if(running_this_subprocess(duplicated_pid)): psutil.Process(duplicated_pid).kill()
                
                time.sleep(60 - int(datetime.now().second))

        except (Exception) as error: time.sleep(1)

if __name__ == "__main__":
    
    main()