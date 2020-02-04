# Camada pyhton de abstração para banco de dados postgres

## O que este pacote faz

Cria tabela no banco, grava, lê e atualiza dados em uma tabela existente.

## O que ainda não faz

Apaga dados de tabelas ou tabelas, renomeia tabelas. Vide a seção "copiar depois".

## Testes

**ATENÇÃO:** Os testes ainda estão "em rascunho".

### Criar tabelas
  
Criado o teste para conferir se a tabela é criada. O teste verificou positivo, porém é preciso testar os cenários de exceção como:

    - Tentar criar uma tabela já exixtente
    - Etc

### Salvar dados em tabelas

Teste de salvamento verificou positivo, porém é preciso testar os cenários de exceção como:

    - Tenta salvar em tabela inexistente
    - Tenta salvar pk conflitante
    - Tenta gravar dados que não condizem com as colunas
    - etc

### Ler dados de uma tabela
  
Teste de leitura verificou positivo, porém é preciso testar os cenários de exceção como:

    - Tenta ler de uma tabela inexistente
    - Etc

### Ainda falta testar

- Conexão com o banco
- Comandos SQL
- update_record
- Funções ainda não escritas (deletar entradas, deletar tabela, renomear tabela)

## Para copiar depois

### Renomear tabela

    import psycopg2
    import psycopg2.extras

    connection = psycopg2.connect(host=DB_HOST, database=POSTGRES_DB, 
                                user=POSTGRES_USER, password=POSTGRES_PASSWORD)

    pointer = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    table_name = 'binance_klines_xrpusdt_1m'

    new_table_name = 'binance_klines_btcusdt_1m_test'


    query = 'ALTER TABLE ' + table_name + ' RENAME TO ' + new_table_name + ';'

    pointer.execute(query)
    connection.commit()
    connection.close()

    print(query)

### Apagar tabela

    connection = psycopg2.connect(host=DB_HOST, database=POSTGRES_DB, 
                                user=POSTGRES_USER, password=POSTGRES_PASSWORD)

    pointer = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    table_name = 'test'


    #query = 'ALTER TABLE ' + table_name + ' RENAME TO ' + new_table_name + ';'
    query = 'DROP TABLE ' + table_name + ';'

    pointer.execute(query)  
    connection.commit()
    connection.close()

### Teste de update record

    #Testando para mudança da chave 'status', da tabela 'binance_pairs' Modifique À vontade.

    #=======================================================================
    #Função auxiliar para gerar uma string randômica
    import random
    import string

    def randomString(stringLength=10):
        
        """Generate a random string of fixed length """
        
        letters = string.ascii_lowercase
        
        return ''.join(random.choice(letters) for i in range(stringLength))
    #=======================================================================


    table_name = 'binance_pairs'

    pk_field = 'name'

    pk_value = 'BTCUSDT'

    field_to_update = 'status'

    new_field_value = randomString(8) #Máximo 8 caracteres

    records = read_table(table_name, mute='yes')

    for record in records:

        if (record[pk_field] == pk_value):

            old_record = record
            
            old_field_value = record[field_to_update]

    update_table_job_status = update_table(table_name, pk_field, pk_value, field_to_update, new_field_value)

    print(update_table_job_status + '''
    ''')

    if (update_table_job_status == 'done'):
        
        records = read_table(table_name, mute='yes')
        
        for record in records:
            
            if (record[pk_field] == pk_value):
                
                new_record = record
                
        #Desfazendo
        update_table_job_status = update_table(table_name, pk_field, pk_value, field_to_update, old_field_value)
        
    print('''Entrada anterior   - ''' + str(old_record) + '''
    Entrada atualizada - ''' + str(new_record) + '''
    ''')
