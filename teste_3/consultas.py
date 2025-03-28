import psycopg2

DB_CONFIG = {
    "dbname": "estagio-teste",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5433"
}

def executar_consultas():
    """
    Consulta operadoras com maiores despesas em sinistros, considerando datas no formato YYYY-MM
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    consulta_base = """
    WITH parametros AS (
        SELECT 
            MAX(TO_DATE(data, 'YYYY-MM')) AS data_maxima,
            {periodo} AS meses
        FROM demonstracoes_contabeis
    )
    SELECT 
        o.razao_social,
        SUM(dc.vl_saldo_final) AS total_despesas
    FROM demonstracoes_contabeis dc
    JOIN operadoras o ON dc.reg_ans = o.registro_ans
    CROSS JOIN parametros
    WHERE 
        dc.descricao ILIKE '%SINISTROS%'
        AND TO_DATE(dc.data, 'YYYY-MM') 
            BETWEEN DATE_TRUNC('month', data_maxima - (meses || ' months')::INTERVAL)
            AND data_maxima
    GROUP BY o.razao_social
    ORDER BY total_despesas DESC
    LIMIT 10;
    """

    try:
        # Último trimestre
        print("="*60)
        print("Top 10 Operadoras - Último Trimestre")
        print("="*60)
        cursor.execute(consulta_base.format(periodo=3))
        for idx, (operadora, valor) in enumerate(cursor.fetchall(), 1):
            print(f"{idx:2}. {operadora:40} R$ {valor:,.2f}")

        # Último ano
        print("\n" + "="*60)
        print("Top 10 Operadoras - Último Ano")
        print("="*60)
        cursor.execute(consulta_base.format(periodo=12))
        for idx, (operadora, valor) in enumerate(cursor.fetchall(), 1):
            print(f"{idx:2}. {operadora:40} R$ {valor:,.2f}")

    except Exception as e:
        print(f"Erro: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    executar_consultas()