"""Este módulo deve tratar da solicitação dos dados de mercado junto à binance. Suas principais
funcionalidades compreemdem:

    - Fazer a solicitação dos dados;

    - Ajustar dados faltantes;

    - Paralelizar requisições para pares de ativos diferentes, em segundo plano (concorrência);

    - Parar o processamento, periodicamente, em caso de aproximação do limite de 
    requests junto à binance;

    - Solicitar, de forma periódica, os dados;

    - Salvar os dados no banco de dados.

"""

import requests
import json
import time
from datetime import datetime

class BinanceDataHandler:

    def __init__(self, asset_pair, candle_interval, start_time, max_attempts):
        self.asset_pair = asset_pair
        self.candle_interval = candle_interval
        self.start_time = start_time
        self.max_attempts = max_attempts
    
    

