from django.db import models

class BinanceAsset (models.Model):

    class Meta:

        db_table = '"binance_assets"'
    
    AUTO_UPDATE_CHOICES=(
        ('ON','on'),
        ('OFF','off'),
        )

    asset_symbol = models.CharField(max_length=8, primary_key=True)
    auto_update = models.CharField(max_length=3, choices=AUTO_UPDATE_CHOICES, default='OFF')
    status = models.CharField(max_length=8, default='absent')
    last_modified_by = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.asset_symbol