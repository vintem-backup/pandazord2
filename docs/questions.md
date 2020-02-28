# Questões

## klines da Binance

### Por que 1m

Todos os *"candle intervals"* fornecidos pela binance são múltiplos do candle de 1m, portanto, pareceu uma decição óbvia adquirir apenas 1m e *"parsear"* os outros tempos gráficos.

Também para a concepção de backing *"tests"* mais precisos, mesmo operando com candles mais *"largos*", parece mais seguro ter o dado de cada minuto para checagem da estratégia; por exemplo, conferir os critérios de *"stoploss"* numa frequencia mais alta parece mais sensato do que esperar uma volta inteira equivalente ao *"candle largo"* em operação.

### Em aberto (28/02/2020): offset e treshold

Do jeito que foi concebido, o módulo *"klines handler*", pode retornar um conjunto de candles de qualquer tamanho (desde que, "originalmente", a binance os forneça) em qualquer instante. Então, por exemplo, pode-se ter um conjunto de candles de 6h:

| `open_time`         | open    | high    | ... |
| ------------------- |:-------:|:-------:| ---:|
| 2019-02-26 01:19:00 | 3830.89 | 3830.89 | ... |
| 2019-02-26 07:19:00 | 3830.89 | 3830.89 | ... |
| 2019-02-26 19:19:00 | 3830.89 | 3830.89 | ... |
|          ...        |   ...   |   ...   | ... |

Obviamente, 
