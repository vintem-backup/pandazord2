from django.db import models

class BinanceAssets (models.Model):

    class Meta:

        db_table = '"binance_assets"'
    
    STATUS_CHOICES=(
        ('ON','on'),
        ('OFF','off'),
        )

    asset_symbol = models.CharField(max_length=8, primary_key=True)
    get_data = models.CharField(max_length=3, choices=STATUS_CHOICES, default='OFF')
    status = models.CharField(max_length=8, default='absent')
    last_change_by_pid = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.asset_symbol