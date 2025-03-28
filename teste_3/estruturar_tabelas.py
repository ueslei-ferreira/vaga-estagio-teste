import psycopg2
import pandas as pd
import os

# Configurações do banco de dados
DB_CONFIG = {
    "dbname": "estagio-teste",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5433"
}

# Função para processar os arquivos CSV
def analisar_csvs(pastas):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Criar as tabelas se não existirem
    # Tabela registros (existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
            id SERIAL PRIMARY KEY,
            data VARCHAR(255),
            reg_ans INTEGER,
            cd_conta_contabil INTEGER,
            descricao TEXT,
            vl_saldo_inicial FLOAT,
            vl_saldo_final FLOAT
        );
    ''')
    
    # Nova tabela operadoras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operadoras (
            id SERIAL PRIMARY KEY,
            registro_ans INTEGER,
            cnpj VARCHAR(255),
            razao_social VARCHAR(255),
            nome_fantasia VARCHAR(255),
            modalidade VARCHAR(255),
            logradouro VARCHAR(255),
            numero VARCHAR(255),
            complemento VARCHAR(255),
            bairro VARCHAR(255),
            cidade VARCHAR(255),
            uf CHAR(2),
            cep VARCHAR(10),
            ddd VARCHAR(5),
            telefone VARCHAR(20),
            fax VARCHAR(20),
            endereco_eletronico VARCHAR(255),
            representante VARCHAR(255),
            cargo_representante VARCHAR(255),
            regiao_de_comercializacao INTEGER,
            data_registro_ans DATE
        );
    ''')
    conn.commit()

    for pasta in pastas:
        for arquivo in os.listdir(pasta):
            if arquivo.endswith(".csv"):
                caminho_csv = os.path.join(pasta, arquivo)
                print(f"Processando: {caminho_csv}")
                
                try:
                    # Identificar qual tabela usar
                    if pasta == 'operadoras_ativas':
                        df = pd.read_csv(caminho_csv, encoding="utf-8", sep=";")
                        df.columns = [col.lower() for col in df.columns]  # Normalizar nomes das colunas
                    else:
                        df = pd.read_csv(caminho_csv, encoding="utf-8", sep=";", decimal=",")
                    
                    df.fillna(0, inplace=True)  # Substitui valores NaN por 0
                    
                    for _, row in df.iterrows():
                        if pasta == 'operadoras_ativas':
                            cursor.execute('''
                                INSERT INTO operadoras (
                                    registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, 
                                    complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, 
                                    representante, cargo_representante, regiao_de_comercializacao, data_registro_ans
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ''', tuple(row))
                        else:
                            cursor.execute('''
                                INSERT INTO demonstracoes_contabeis (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            ''', tuple(row))
                except UnicodeDecodeError:
                    print(f"Erro ao ler {caminho_csv}. Verifique o encoding do arquivo.")
                    continue

    conn.commit()
    cursor.close()
    conn.close()
    print("Importação concluída com sucesso!")

if __name__ == "__main__":
    caminhos_pastas = [
        'demonstracoes_contabeis2023',
        'demonstracoes_contabeis2024',
        'operadoras_ativas'  # Nova pasta adicionada
    ]
    analisar_csvs(caminhos_pastas)