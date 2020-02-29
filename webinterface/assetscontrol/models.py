from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import datetime

AUTO_UPDATE_CHOICES=(
    ('ON','on'),
    ('OFF','off'),
    )

TRADE_CHOICES=(
    ('Y', 'yes'),
    ('N', 'no'),
)

def default_operational_parameters():
    
    return {
        'strategy' : {
            'name' : 'CrossSMA',
            'parameters' : {
                'number_samples' : (3,100),
            }
        },
        
        'stop_loss' : {
            'name' : 'Default',
            'parameters': {
                'first_trigger' : (1,3,10),
                'second_trigger' : (1,16,50)
            }
                
        },
        
        'candle_interval': '1h',
        'sleep_duration': 60,
        'price_source':'ohlc4'
        
    }

def default_position():
    
    return {
        'side' : 'closed',
        'size': 0.0,
        'target_price': 0.0
    }


class BinanceAsset (models.Model):

    class Meta:

        db_table = '"binance_assets"'

    asset_symbol = models.CharField(max_length=8, primary_key=True)
    
    auto_update = models.CharField(max_length=3, choices=AUTO_UPDATE_CHOICES, default='OFF')
    
    status = models.CharField(max_length=8, default='absent')
    
    last_updated_by_pid = models.IntegerField(null=True, blank=True)
    
    collect_data_since = models.DateTimeField(default = datetime.fromtimestamp(1241893500))

    trade_on = models.CharField(max_length=3, choices=TRADE_CHOICES, default='N')

    available_amount = models.FloatField(null=True, blank=True, default=0.0)
    
    operational_parameters = JSONField(default=default_operational_parameters)

    position = JSONField(default=default_position)

    def __str__(self):
        return self.asset_symbol