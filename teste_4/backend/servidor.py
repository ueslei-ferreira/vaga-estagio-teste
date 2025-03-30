from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Caminho relativo para o arquivo CSV
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "teste_3",
    "operadoras_ativas",
    "Relatorio_cadop.csv"
)

# Carrega o arquivo CSV em um DataFrame do pandas
df = pd.read_csv(DATA_PATH, sep=';', encoding='utf-8', dtype=str)

@app.route('/busca', methods=['GET'])
def busca():
    """
    Endpoint para buscar registros no arquivo CSV com base em um termo de busca.

    O termo de busca é enviado como um parâmetro de consulta 'q' na URL.
    Ele realiza a busca nos campos: Razão Social, Nome Fantasia, CNPJ, Registro ANS e Modalidade.

    Returns:
        JSON: Lista de registros que correspondem ao termo de busca.
        Se o parâmetro 'q' não for fornecido, retorna um erro 400.
    """
    termo = request.args.get('q', '').lower()
    if not termo:
        return jsonify({"error": "Parâmetro 'q' obrigatório"}), 400

    # Filtra os registros no DataFrame com base nos campos relevantes
    resultados = df[
        df['Razao_Social'].str.lower().str.contains(termo, na=False) |  # Busca no campo Razão Social
        df['Nome_Fantasia'].str.lower().str.contains(termo, na=False) |  # Busca no campo Nome Fantasia
        df['CNPJ'].str.contains(termo, na=False) |  # Busca no campo CNPJ
        df['Registro_ANS'].str.contains(termo, na=False) |  # Busca no campo Registro ANS
        df['Modalidade'].str.lower().str.contains(termo, na=False)  # Busca no campo Modalidade
    ]

    # Substitui valores NaN por None para evitar problemas no JSON
    resultados = resultados.where(pd.notnull(resultados), None)

    # Converte os resultados para o formato JSON e retorna
    return jsonify(resultados.to_dict(orient='records'))

if __name__ == '__main__':
    """
    Inicia o servidor Flask na porta padrão (5000) e habilita o modo de depuração.
    """
    app.run(host='0.0.0.0', debug=True)