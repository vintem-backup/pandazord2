# Plano de Refatoração

## Serviço (container) binancedatahandler

*[ ] Aumentar o nível de abstrações, chamando nos programas **"listening_of_binance_assets_table.py"** e **"complete_oldest_data_so_far.py"** apenas as funções contidas no **"modules"** (autorais) ou, no máximo, bibliotrcas python "padrões".  

*[ ] No nível de consultas ao banco de dados, tentar implementar o SQLAlchemy, abaixo da abstração criada, como neste [exemplo](https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/ "learndatasci, Data Science Tutorials")
  
  *[ ] No nível de comunicação com a binance, tentar implemetar o [**wrapper** python](https://python-binance.readthedocs.io/en/latest/ "Python wrapper for binance API") largamente utilizado, abaixo da abstação criada.  

*[x] mlkm
