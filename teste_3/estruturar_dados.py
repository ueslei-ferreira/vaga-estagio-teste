import psycopg2
import pandas as pd
import os

# Configurações do banco de dados
BD_CONFIG = {
    "dbname": "seu_banco",
    "user": "seu_usuario",
    "password": "sua_senha",
    "host": "localhost",
    "port": "5433"
}

def exportar_dados_csvs(pastas):
    """
    Processa arquivos CSV pastas e insere os dados em tabelas PostgreSQL.

    Args:
        pastas (list): Caminhos das pastas contendo os arquivos CSV a serem processados.

    """
    # abre a conexão com o banco de dados
    conn = psycopg2.connect(**BD_CONFIG)
    cursor = conn.cursor()

    # Cria tabela para demonstrações contábeis se não existir.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
            id SERIAL PRIMARY KEY,
            data DATE,
            reg_ans VARCHAR(15),
            cd_conta_contabil VARCHAR(15),
            descricao TEXT,
            vl_saldo_inicial FLOAT,
            vl_saldo_final FLOAT
        );
    ''')
    
    # Cria tabela para operadoras se não existir.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operadoras (
            id SERIAL PRIMARY KEY,
            registro_ans VARCHAR(7),
            cnpj VARCHAR(15),
            razao_social VARCHAR(255),
            nome_fantasia VARCHAR(255),
            modalidade VARCHAR(255),
            logradouro VARCHAR(255),
            numero VARCHAR(100),
            complemento VARCHAR(255),
            bairro VARCHAR(50),
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

    # Processa cada pasta especificada
    if pastas:
        for pasta in pastas:  # Itera sobre cada pasta na lista
            print(f"Processando arquivos na pasta: {pasta}")
            for arquivo in os.listdir(pasta):  # Lista os arquivos na pasta atual
                if arquivo.endswith(".csv"):
                    caminho_csv = os.path.join(pasta, arquivo)
                    print(f"Processando: {caminho_csv}")
                    
                    try:
                        # Lê o CSV e processa os dados
                        if 'demonstracoes_contabeis' in pasta:
                            df = pd.read_csv(caminho_csv, encoding="utf-8", sep=";", decimal=",")
                        else:
                            df = pd.read_csv(caminho_csv, encoding="utf-8", sep=";")
                            df.columns = [col.lower() for col in df.columns]
                            
                        # Substitui valores NaN por 0, evita erros de conversão e inserção
                        df.fillna(0, inplace=True)
                        
                        # Insere os dados no banco
                        for _, row in df.iterrows():
                            if 'operadoras_ativas' in pasta:
                                cursor.execute('''
                                    INSERT INTO operadoras (
                                        registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, 
                                        complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, 
                                        representante, cargo_representante, regiao_de_comercializacao, data_registro_ans
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ''', tuple(row))
                            else:
                                cursor.execute('''
                                    INSERT INTO demonstracoes_contabeis (
                                        data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final
                                    ) VALUES (%s, %s, %s, %s, %s, %s)
                                ''', tuple(row))
                    except UnicodeDecodeError:
                        print(f"Erro de encoding no arquivo: {caminho_csv}")
                        continue

    # Finaliza transação e fecha conexão
    conn.commit()
    cursor.close()
    conn.close()
    print("Importação concluída com sucesso!")

if __name__ == "__main__":
    # Especifique as pastas que deseja processar
    pastas = ['demonstracoes_contabeis2023','demonstracoes_contabeis2024' , 'operadoras_ativas']
    
    # Chama a função para processar as pastas
    exportar_dados_csvs(pastas)