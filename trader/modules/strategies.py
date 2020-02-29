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

        
    def how_many_candles(self):
        
        return self.n_bigger


    def what_side_and_leverage(self, klines):
        
        side = 'short'; leverage = 1.0
        
        if (len(klines) < self.n_bigger):
            
            raise IndexError ('There os no sufficient klines entrys to calculate the bigger moving avarage')
        
        else:
            
            price = getattr(PriceSeriesFrom(klines), self.price_source + '_')()
            rolling_mean = Trend(price).simple_moving_average
            last_smaller = rolling_mean(self.n_smaller)[len(price) - 1]
            last_bigger = rolling_mean(self.n_bigger)[len(price) - 1]
            
            if (last_smaller > last_bigger): side = 'long'
        
        return side, leverage

    def verify(self, klines, position):
        
        side, leverage = self.what_side_and_leverage(klines)
        
        class Trade:
            
            def __init__(self, position, side, leverage):
                
                self.is_true = False
                self.leverage = leverage
                self.command = 'hold'
                    
                if(side == 'long' and position.iloc[0]['side'] == 'closed'): 
                    self.command = 'buy'; self.is_true = True
                
                elif(side == 'short' and position.iloc[0]['side'] == 'long'): 
                    self.command = 'sell'; self.is_true = True
        
        return Trade(position, side, leverage)