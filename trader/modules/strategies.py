#TODO: Docstrings and Type annotations

from .common_libs import PriceSeriesFrom
from .market_indicators import *


class CrossSMA:
    
    def __init__(self, sample_numbers, price_source):
        
        self.n_smaller = sample_numbers[0]
        self.n_bigger = sample_numbers[1]
        self.price_source = price_source
        
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