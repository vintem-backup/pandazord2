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

operational_parameters = {
    'strategy' : {
        'name' : 'CrossSMA',
        
        'parameters' : {
            'candle_interval': '1h',
            'price_source' : 'ohlc4',
            'n_smaller' : 3,
            'n_bigger' : 100
        }
    },
    
    'stop_loss' : {
        'name' : 'Default',
        
        'parameters': {
            'candle_interval': '1m',
            'price_source' : 'ohlc4',
            
            'first_trigger' : {
                'rate(%)' : 5,
                
                'treshold' : {
                    'n_measurements' : 10,
                    'n_positives' : 3
                }
                
            },
            
            'second_trigger' : {
                'rate(%)' : 1,
                
                'treshold' : {
                    'n_measurements' : 50,
                    'n_positives' : 20
                }                
            },
            
            'update_target_if' : {
                'rate(%)' : 6,
                
                'treshold' : {
                    'n_measurements' : 10,
                    'n_positives' : 4                
                }
            }
        }
    },
    
    'sleep_duration': 60,
}

def default_operational_parameters():
    
    return operational_parameters

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