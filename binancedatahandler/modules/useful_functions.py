#TODO: Docstrings and type annotations
from datetime import datetime
import requests

def utc_time_func():
    
    try:
    
        url = 'http://worldclockapi.com/api/json/utc/now'

        time_utc_now = requests.get(url).json

        year = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[0])
        month = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[1])
        day = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[2])

        hour = int(time_utc_now()['currentDateTime'].split('T')[1].split(':')[0])
        minute = int(time_utc_now()['currentDateTime'].split('T')[1].split(':')[1].split('Z')[0])
    
        utc_now = datetime(year, month, day, hour, minute)
    
    except (Exception) as error: #TODO: Tratar exceção
        
        utc_now = datetime.utcnow()

    return utc_now

def delta_time_in_exact_seconds_from_hours_between_utc_and(this_time):

    utc_time = utc_time_func()
    
    delta_time = utc_time - this_time

    delta_hour = round(delta_time.total_seconds()/3600)
    
    delta = delta_hour*3600
    
    return delta