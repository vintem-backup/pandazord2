# Plano de Refatoração

## De uma modo geral

* [ ] Revisar os programas, vasculhando atributos/métodos privados e violações deste modelo, como no livro da alura, capitúlo 8

* [ ] Adicionar decorador de cálculo do tempo de processamento (há alguns modelos no PyPi).

## webinterface

* [x] Retirar: "real_current_side", "real_target_price", "bt_current_side", "bt_target_price"  

* [x] Acrescentar jsonField para descrever posição  

* [x] Adicionar campo de controle para "trade_on"

* [x] Acrescentar jsonField para os parâmetros da estratégia  

## Binancedatahandler

* [ ] Aumentar o nível de abstrações, chamando nos programas ***"listening_of_binance_assets_table.py"*** e ***"complete_oldest_data_so_far.py"*** apenas as funções contidas no ***"modules"*** (autorais) ou, no máximo, bibliotecas python "padrões".  

  * [ ] No nível de consultas ao banco de dados, tentar implementar o ***SQLAlchemy***, abaixo da abstração criada, como neste [exemplo](https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/ "learndatasci, Data Science Tutorials")
  
  * [ ] No nível de comunicação com a binance, tentar implemetar o [*wrapper* python](https://python-binance.readthedocs.io/en/latest/ "Python wrapper for binance API") largamente utilizado, abaixo da abstração criada.  

* [x] No programa ***"complete_oldest_data_so_far.py"***, deslocar a consulta do ***"last_open_time"*** ao banco de dados: de fora do ***whilie True*** para dentro, a fim de manter a regularidade da complementação do dado, mesmo em caso de falha do cluster.  
**OBS.:** A função ***"replace_with_zero_where_data_is_missing"*** deixará de retornar o ***"last_open_time"***, já que não será mais necessário, tornando até mais correto o retorno.  

## Trader

### main

#### Backing Test

* [ ] Calcular o tempo de duração do processo através do decorador específico.

### modules

#### historical

(É realmente necessário? E em que granulção de log?)

* [ ] Dados de interesse: open_time, price, side (long, short, closed), order (hold, buy, sell)

#### klines_handler

* [x] Adicionar método para pegar toda a massa de dados de 1m disponível para aquele par, para backingtest  
* [x] "Descer" as credenciais do banco 'os.environmet...' para este módulo, ao invés do 'trader'
* [ ] Adicionar método para pegar as *klines* **a partir de** e **até** um *datetime* específicos  
* [ ] Adicionar método para apenas "atualizar" a *kline*, "memorizando" a massa de dados mais extensa,substituindo a entrada mais antiga e adicionando uma entrada mais recente (*"cache"*).  
* [ ] Adicionar funcionalidade *"no offset"* a fim de retornar **apenas** [candles que "façam sentido"](/docs/questions.md)
* [ ] Escrever os testes  

#### Assets_handler

* [x] "Descer" as credenciais do banco 'os.environmet...' para este módulo, ao invés do 'trader'

#### Strategies

* [ ] É possível criar uma cadeia de classes para formar o objeto "operational_parametres". Ver o livro da alura entre as pgs 100 e 102
