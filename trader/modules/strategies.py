from .shared_objects import PriceSeriesFrom


class CrossingMovingAverages:
    
    def __init__(self, sample_number_pair, price_source):
        
        self.n_smaller = sample_number_pair[0]
        self.n_bigger = sample_number_pair[1]
        self.price_source = price_source
        
    def set_side(self, klines):
        
        side = 'sell'
        
        if (len(klines) < self.n_bigger):
            
            raise IndexError ('There os no sufficient klines \
entrys to calculate the bigger moving avarage')
        else:
            
            price = getattr(PriceSeriesFrom(klines), self.price_source + '_')()
            
            last_small_rolling_mean = price.rolling(self.n_smaller).mean()[len(price) - 1]
            
            last_big_rolling_mean = price.rolling(self.n_bigger).mean()[len(price) - 1]
            
            if (last_small_rolling_mean > last_big_rolling_mean): side = 'buy'
        
        return side