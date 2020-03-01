# Questões

## klines da Binance

### Por que 1m

Todos os *"candle intervals"* fornecidos pela binance são múltiplos do candle de 1m, portanto, pareceu uma decição óbvia adquirir apenas 1m e *"parsear"* os outros tempos gráficos.

Também para a concepção de backing *"tests"* mais precisos, mesmo operando com candles mais *"largos*", parece mais seguro ter o dado de cada minuto para checagem da estratégia; por exemplo, conferir os critérios de *"stoploss"* numa frequencia mais alta parece mais sensato do que esperar uma volta inteira equivalente ao *"candle largo"* em operação.

### Em aberto (28/02/2020): offset e treshold

Do jeito que foi concebido, o módulo *"klines handler*", pode retornar um conjunto de candles de qualquer tamanho (desde que, "originalmente", a binance os forneça) em qualquer instante. Então, por exemplo, pode-se ter um conjunto de candles de 6h:

| **open_time**         | **open** | **high** | ... |
| --------------------- |:--------:|:--------:| ---:|
| `2019-02-26 01:19:00` | 3830.89  | 3830.89  | ... |
| `2019-02-26 07:19:00` | 3830.89  | 3830.89  | ... |
| `2019-02-26 13:19:00` | 3830.89  | 3830.89  | ... |
|           ...         |   ...    |   ...    | ... |

Obviamente, porderia ser feito de uma forma a retornar apenas os tempos que, "originalmente façam sentido", como, ainda tomando ocmo exemplo o candle de 6h, 01:00:00, 07:00:00, 13:00:00..., porém, a intenção era verificar a estratégia mais refinadamente (neste caso, a cada minuto, mesmo que o *"candle interval"* da operação não o seja).

Admitindo que será mantido deste jeito (verificação da estratégia a cada minuto, mesmo utolizando "candles maiores") **a questão posta é se haverá falsos positivos**.

Duas formas de contornar o problema são:

- Usar um timesleep equivalente ao tamanho do candle testado e, eventualmente, ciclar num tempo menor caso esteja comprado (ou vendido a descoberto) a fim de verificar *stoploss*;

- Manter a abordagem atual, adicioanando um *"treshold"* na estratégia, a fim de evitar os falsos positivos.

#### Decisão atual (28/02/2020)

Por se tratar de uma estratégia de calibração que se utiliza de apenas **UM** indicador (e de apenas uma classe, tendência) a possibilidade de falso positivo já exite, mesmo sem a questão posta acima. Assim, é preferível manter o curso do desenvolvimento, criando uma estrutura suficientemente robusta para testes, que possa trazer respostas mais claras.

Além disso, a adição de novos indicadores deve dimimnuir a possibilidade de falsos positivos.
