from .common_libs import PriceSeriesFrom

class Default:

    class Trigger:
        
        def __init__(self, parameters):
            
            self.rate = parameters['rate(%)']/100
            self.n_measurements = parameters['treshold']['n_measurements']
            self.n_positives = parameters['treshold']['n_positives']
    
    def __init__(self, parameters):

        self.price_source = parameters['price_source']
        self.first, self.second, self.update = (self.Trigger(parameters['first_trigger']), 
        self.Trigger(parameters['second_trigger']), 
        self.Trigger(parameters['update_target_if']))

        
    def how_many_candles(self): #ok
        
        return max(self.first.n_measurements, self.second.n_measurements, self.update.n_measurements)
    

    def is_stop(self, klines): #not_ok
        
        price = getattr(PriceSeriesFrom(klines), price_source + '_')()
    
    
    def verify(self, klines, position): #not_ok

        class Stop: #not_ok
            
            def __init__(self, klines): #not_ok
                
                self.is_true = self.is_stop(klines)
        
        return Stop(klines)