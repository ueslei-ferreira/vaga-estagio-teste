import pdfplumber
import csv
import os
import zipfile

def substitui_abreviacoes(cabecalho):
    """
    Substitui abreviações nos cabeçalhos de acordo com a legenda.

    Args:
        cabecalho (list): Lista contendo os cabeçalhos extraídos do PDF.
    
    Returns:
        list: Lista de cabeçalhos com as abreviações substituídas.
    """
    
    legenda = {
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial"
    }
    return [legenda.get(col, col) for col in cabecalho]

def pdf_para_csv(diretorio_pdf, diretorio_csv):
    """
    Converte um arquivo PDF contendo tabelas em um arquivo CSV.
    
    Args:
        diretorio_pdf (str): Caminho do arquivo PDF de entrada.
        diretorio_csv (str): Caminho do arquivo CSV de saída.
    
    Processo:
        1. Abre o arquivo PDF.
        2. Extrai tabelas e processa os cabeçalhos.
        3. Substitui abreviações nos cabeçalhos.
        4. Salva os dados extraídos em um arquivo CSV.
    """
    with pdfplumber.open(diretorio_pdf) as pdf:
        print("Extraindo dados!")
        cabecalho = [] #Lista utilizada para armazenar os cabeçalhos
        dados = []
        
        for pagina in pdf.pages:
            tabela = pagina.extract_table()
            if not tabela:
                continue  # Pula páginas sem tabela
            
            if not cabecalho:
                cabecalho = substitui_abreviacoes(tabela[0])  # Substitui as abreviações
                linhas = tabela[1:]  # Ignora o cabeçalho na primeira página
            else:
                #Caso o cabeçalho já tenha sido definido, verifica se a primeira linha da nova tabela é idêntica ao cabeçalho já salvo.Se for igual, remove essa linha da tabela.
                if tabela[0] == cabecalho:
                    linhas = tabela[1:]
                else:
                    linhas = tabela
                    
            #Percorre todas as linhas da tabela extraída, se alguma linha tiver menos colunas que o cabeçalho, preenche as células vazias com strings vazias.
            for row in linhas:
                padded_row = row + [''] * (len(cabecalho) - len(row)) if row else []
                dados.append(padded_row)
        
        #Cria e abre o arquivo CSV, escreve a linha do cabeçalho no arquivo e depois escreve todas as linhas extraídas da tabela.
        with open(diretorio_csv, 'w', newline='', encoding='utf-8') as arquivo_csv:
            print("Criando CSV")
            writer = csv.writer(arquivo_csv)
            writer.writerow(cabecalho)
            writer.writerows(dados)

def converter_e_compactar():
    """
    Garante a conversão do PDF para CSV e compacta o resultado em um arquivo ZIP.
    
    Processo:
        1. Verifica a existência do arquivo PDF.
        2. Converte o PDF para CSV.
        3. Compacta o arquivo CSV em um arquivo ZIP.
    """
    
    diretorio = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "teste_1", "anexos_baixados"
    )
    diretorio_pdf = os.path.join(diretorio, "Anexo_I.pdf")
    diretorio_csv = 'tabela.csv'

    if not os.path.exists(diretorio_pdf):
        print(f"Erro: O arquivo {diretorio_pdf} não foi encontrado.")
    else:
        pdf_para_csv(diretorio_pdf, diretorio_csv)
        print("Conversão concluída!")
        
        with zipfile.ZipFile('Teste_ueslei.zip', 'w') as zipf:
            zipf.write(diretorio_csv, arcname=os.path.basename(diretorio_csv))
            print(f"Arquivo ZIP 'Teste_ueslei.zip' criado com sucesso!")

if __name__ == '__main__':
    converter_e_compactar()
