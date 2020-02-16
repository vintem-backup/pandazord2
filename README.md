# Pandazord Draft

[Pandazord](https://www.pandazord.trade "Pandzord's official homepage") first approach. A multimarket trading bot.

## O que é

Um robô que realiza trades e tem a intenção de ser agnóstico quanto ao mercado em que está negociando.

## Tecnologias

A lingagem de programação predominante no robô é o Python.

A intenção é conceber uma arquitetura baseada em *microsserviços*, isolados em *containers Docker*.

## Vulnerabilidades Conhecidas

### PID em docker

Os números dos PIDs dos subprocessos ficam armazenados no banco. Caso o cluster caia e reinicie, esses números são "lembrados" pelo volume. Pode ocorrer de os novos processos disparados terem PIDs iguais aos dos processos "mortos", então, do jeito que a lógica foi concebida, esses processos (que deveriam estar 'mortos') não serão mortos, já que há um novo processo com o mesmo o número. Assim, o ativo que tinha esse número ficará sem atualização, até que o ativo cujo novo processo com o mesmo PID atualize 100%.

- Sugestão de correção

    - 1) Durante a leitura da tabela *"binance_assets"*, colecionar os PIDs numa lista, levantar os PIDs repetidos, matar os PIDs repetidos.

- Status

     - 1) Implementando sugestão de correção 1.
     - 2) Sugestão 1 implementada, testada e funcionando. Porém, caso o PID pertença a outro processo que não aqueles lançados no subprocess (o que é improvável, porém aconteceu nos testes, porque os números de PID foram "inventados" sem conferir se pertenciam a outros processos do sistema) o **psutil** falhará, por não ter acesso ao PID.

### Erro de leitura da tabela no programa complete_oldest_data_so_far.py

Da forma como foi escrita a função de consulta ao banco de dados, caso a função *return_last_open_time_from_db_or_create_table_if_doesnt_exist* não consiga ler da tabela (retorna lista vazia, e não *"raise error"*), a mesma  retornará o timestamp mais antigo (definido pelo usuário) o que pode conflitar com o valor real do último candle fechado armazenado no banco.

- Sugestão de correção

     Alterar a função de consulta ao banco, para retornar o erro em caso de exceção, bem como a *return_last_open_time_from_db_or_create_table_if_doesnt_exist* a fim de lidar com este retorno.

- Status

    Em fila para correção.

## Etapas de desenvolvimento

### Prova de conceito

- Deixar o bot suficientemente funcional (estável, seguro, etc) para que possa realizar trades em múltiplos mercados de criptomoedas na *exchange* [Binance](https://www.binance.com "The World's Leading
Cryptocurrency Exchange"), utilizando uma "estratégia de calibração" simples (cruzamento de médias móveis com *"stop trending"*).

### Novas estratégias

- Adição de novas funções de indicadores de mercado, além das médias móveis;
- Desenvolvimento e teste de novas estratégias, com ou sem inteligência artificial.

### Arquitetura

- Divisão do subgrupo em repositórios distintos para cada *microsserviço*;
- Adoção do *[OpenFaas](https://www.openfaas.com "Serverless Functions, Made Simple")* como padrão arquitetural;
- Deploy em *cluster [kubernetes](https://kubernetes.io/ "Production-Grade Container Orchestration")*.

### Expansão para B3

- Criação do *microsserviço* de aquisição de dados da B3;
- Adição do *backing test* de estratégias para B3 no *microsserviço* de *backing test* ou criação de um microsserviço próprio;
- Adição das funções de disparamento de ordens para B3 no *microsserviço* de "brocker" ou criação de um microsserviço próprio.
