#TODO: Docstrings and Type annotations

from .common_libs import PriceSeriesFrom
from .market_indicators import *


class CrossSMA:
    
    def __init__(self, operational_parameters):
        
        self.n_smaller = operational_parameters['strategy']['parameters']\
            ['number_samples'][0]
        self.n_bigger = operational_parameters['strategy']['parameters']\
            ['number_samples'][1]
        self.price_source = operational_parameters['price_source']
        self.positive_treshold = operational_parameters['strategy']['parameters']\
            ['treshold'][0]
        self.positive_treshold = operational_parameters['strategy']['parameters']\
            ['treshold'][1]
        
    def set_side(self, klines):
        
        side = 'sell'
        
        if (len(klines) < self.n_bigger):
            
            raise IndexError ('There os no sufficient klines entrys to calculate the bigger moving avarage')
        
        else:
            
            price = getattr(PriceSeriesFrom(klines), self.price_source + '_')()
            
            rolling_mean = Trend(price).simple_moving_average

            last_smaller = rolling_mean(self.n_smaller)[len(price) - 1]
            
            last_bigger = rolling_mean(self.n_bigger)[len(price) - 1]

            print ('Média longa = {}, média curta = {}'.format(last_bigger, last_smaller))
            
            if (last_smaller > last_bigger): side = 'buy'
        
        return side
    

    def set_order(self, klines, asset_info, historical):
        pass