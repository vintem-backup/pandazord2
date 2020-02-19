from django.db import models
from datetime import datetime

#TODO: Renomear esta tabela, lembrando da propagação para os progrmas que dela dependem
class BinanceAsset (models.Model):

    class Meta:

        db_table = '"binance_assets"'
    
    AUTO_UPDATE_CHOICES=(
        ('ON','on'),
        ('OFF','off'),
        )
    
    SIDE_CHOICES=(
        ('S','SELL'),
        ('B','BUY'),
        )

    asset_symbol = models.CharField(max_length=8, primary_key=True)
    
    auto_update = models.CharField(max_length=3, choices=AUTO_UPDATE_CHOICES, default='OFF')
    
    status = models.CharField(max_length=8, default='absent')
    
    last_updated_by_pid = models.IntegerField(null=True, blank=True)
    
    collect_data_since = models.DateTimeField(default = datetime.fromtimestamp(1241893500))
    
    real_current_side = models.CharField(max_length=4, choices=SIDE_CHOICES, default='S')
    
    real_target_price = models.FloatField(null=True, blank=True)
    
    bt_current_side = models.CharField(max_length=4, choices=SIDE_CHOICES, default='S')
    
    bt_target_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.asset_symbol