#TODO: Docstrings and Type annotations
#TODO: Revisar
#TODO: Testar no Jupyter

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

    def bottom_trigger(klines, target_price, trigger): #ok

        positive = False; positive_found = 0
        price_series = getattr(PriceSeriesFrom(klines[:trigger.n_measurements]), price_source + '_')()
        
        for price in price_series:
            
            if (price <= target_price*(1 - trigger.rate)): positive_found+=1
        
        if (positive_found >= trigger.n_positives): positive = True
        
        return positive

    def upper_trigger(klines, target_price, trigger): #ok

        positive = False; positive_found = 0
        price_series = getattr(PriceSeriesFrom(klines[:trigger.n_measurements]), price_source + '_')()
        
        for price in price_series:
            
            if (price >= target_price*(1 + trigger.rate)): positive_found+=1
        
        if (positive_found >= trigger.n_positives): positive = True
        
        return positive

    def long_stop(self, klines, target_price): #seems_ok

        return True in [self.bottom_trigger(klines, target_price, self.first), 
        self.bottom_trigger(klines, target_price, self.second)]

    def short_stop(self, klines, target_price): #seems_ok

        return True in [self.upper_trigger(klines, target_price, self.first), 
        self.upper_trigger(klines, target_price, self.second)]

    def long_new_price(self, klines, target_price): #seems_ok

        hit_new_price, new_price = False, target_price
        
        hit_new_price = self.upper_trigger(klines, target_price, self.update)

        if (hit_new_price): new_price = target_price*(1 + self.update.rate)

        return hit_new_price, new_price

    def short_new_price(self, klines, target_price): #seems_ok

        hit_new_price, new_price = False, target_price
        
        hit_new_price = self.bottom_trigger(klines, target_price, self.update)

        if (hit_new_price): new_price = target_price*(1 - self.update.rate)

        return hit_new_price, new_price
    
    def verify(self, klines, position): #seems_ok

        class Stop: #seems_ok
            
            def __init__(self, is_true, position, update_target, new_target_price, command): #seems_ok

                self.is_true = is_true
                self.update_target, self.new_target_price = update_target, new_target_price
                self.order = {
                    'type' : 'stop loss',
                    'command' : command,
                    'size' : position['size'],
                    'leverage' : 1,
                    'price' : 'market'
                }
        
        #Default values
        is_true, update_target, new_target_price, command = False, False, position['target_price'], 'hold'

        if(position['side'] == 'long'):
            is_true = self.long_stop(klines, position['target_price'])
            if(is_true): command = 'sell'
            update_target, new_target_price = self.long_new_price(klines, position['target_price'])
        
        elif(position['side'] == 'short'):
            is_true = self.short_stop(klines, position['target_price'])
            if(is_true): command = 'buy'
            update_target, new_target_price = self.short_new_price(klines, position['target_price'])
        
        elif(position['side'] == 'closed'):
            print('Closed, nothing to do.')

        else:
            print('Not a valid position.')
        
        return Stop(is_true, position, update_target, new_target_price, command)