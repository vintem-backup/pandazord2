# Pandazord Draft

First approach of *pandazord*, a multimarket trading bot. Se more at: [Pandazord](https://www.pandazord.trade "Pandzord's official homepage")

## O que é

Um robô que realiza trades e tem a intenção de ser agnóstico quanto ao mercado em que está negociando.

## Tecnologias

A lingagem de programação predominante no robô é o Python.

A intenção é conceber uma arquitetura baseada em *microsserviços*, isolados em *containers Docker*.

## Vulnerabilidades Conhecidas

Nesta [seção](/docs/vulnerabilitys.md), são relatadas as principais falhas detectadas, bem como sugestões e status de correções.

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

## Refatoração

Acompanhhe [aqui](/docs/refactoring.md) o plano de reatoração.

## Questões pertinentes

Esta [seção](/docs/questions.md) reune as principais questões acerca do robô, trazendo algumas justificativas sobre algumas decisões de projeto.
