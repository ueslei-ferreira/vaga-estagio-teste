import psycopg2

DB_CONFIG = {
    "dbname": "seu_banco",
    "user": "seu_usuario",
    "password": "sua_senha",
    "host": "localhost",
    "port": "5433"
}

def executar_consultas():
    """
    Consulta e exibe as 10 operadoras com maiores despesas em sinistros.

    Esta função realiza duas consultas no banco de dados:
    1. Consulta as 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS 
       DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre.
    2. Consulta as 10 operadoras com maiores despesas na mesma categoria no último ano.

    As despesas são calculadas como a diferença entre `vl_saldo_final` e `vl_saldo_inicial` 
    para cada operadora.

    Explicação das Consultas SQL:
    - Ambas as consultas utilizam a tabela `demonstracoes_contabeis` e realizam as seguintes operações:
      1. **Filtro por Descrição (`descricao`)**:
         - Filtra os registros onde a coluna `descricao` contém o texto 
           "SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR".
         - Usa `ILIKE` para ignorar diferenças de maiúsculas e minúsculas.
         - Usa `TRIM` e `REGEXP_REPLACE` para remover espaços extras e normalizar o texto.
      2. **Cálculo de Despesas**:
         - Calcula as despesas como a soma da diferença entre `vl_saldo_final` e `vl_saldo_inicial`.
      3. **Filtro por Intervalo de Tempo**:
         - Último trimestre: Filtra registros com `data` dentro dos últimos 3 meses.
         - Último ano: Filtra registros com `data` dentro dos últimos 12 meses.
      4. **Agrupamento e Ordenação**:
         - Agrupa os resultados pela coluna `reg_ans` (identificador da operadora).
         - Ordena os resultados em ordem decrescente de despesas (`total_despesas`).
      5. **Limitação de Resultados**:
         - Retorna apenas os 10 primeiros resultados com `LIMIT 10`.

    Exibição:
    - Os resultados são exibidos no console, com o índice, o identificador da operadora (`reg_ans`) 
      e o valor total das despesas formatado como moeda (R$).

    Requisitos:
    - A tabela `demonstracoes_contabeis` deve conter as colunas:
      - `reg_ans` (identificador da operadora)
      - `descricao` (descrição do evento)
      - `vl_saldo_inicial` (valor inicial)
      - `vl_saldo_final` (valor final)
      - `data` (data do registro)

    - A coluna `descricao` deve conter o texto "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS 
      DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" para que os registros sejam incluídos na consulta.


    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Consulta para último trimestre
    consulta_trimestre = """
    SELECT 
        reg_ans AS operadora,
        SUM(vl_saldo_final - vl_saldo_inicial) AS total_despesas
    FROM demonstracoes_contabeis
    WHERE 
        TRIM(UPPER(REGEXP_REPLACE(descricao, '[ ]+', ' ', 'g'))) 
        ILIKE '%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
        AND data >= DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '3 months'
        AND data < DATE_TRUNC('quarter', CURRENT_DATE)
    GROUP BY reg_ans
    ORDER BY total_despesas DESC
    LIMIT 10;
    """

    # Consulta para último ano
    consulta_ano = """
    SELECT 
        reg_ans AS operadora,
        SUM(vl_saldo_final - vl_saldo_inicial) AS total_despesas
    FROM demonstracoes_contabeis
    WHERE 
        TRIM(UPPER(REGEXP_REPLACE(descricao, '[ ]+', ' ', 'g'))) 
        ILIKE '%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
        AND data >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY reg_ans
    ORDER BY total_despesas DESC
    LIMIT 10;
    """

    try:
        # Execução para último trimestre
        print("="*60)
        print("Top 10 Operadoras - Último Trimestre")
        print("="*60)
        cursor.execute(consulta_trimestre)  # Executa a consulta para o último trimestre
        resultados_tri = cursor.fetchall()  # Recupera os resultados da consulta
        for idx, (operadora, valor) in enumerate(resultados_tri, 1):  # Itera sobre os resultados
            print(f"{idx:2}. Operadora: {operadora:10} | Despesas: R$ {valor:,.2f}")  # Exibe o índice, operadora e despesas formatadas

        # Execução para último ano
        print("\n" + "="*60)
        print("Top 10 Operadoras - Último Ano")  # Título da seção
        print("="*60)
        cursor.execute(consulta_ano)  # Executa a consulta para o último ano
        resultados_ano = cursor.fetchall()  # Recupera os resultados da consulta
        for idx, (operadora, valor) in enumerate(resultados_ano, 1):  # Itera sobre os resultados
            print(f"{idx:2}. Operadora: {operadora:10} | Despesas: R$ {valor:,.2f}")  # Exibe o índice, operadora e despesas formatadas

    except Exception as e:
        print(f"Erro: {str(e)}")  # Exibe a mensagem de erro caso ocorra uma exceção
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    executar_consultas()