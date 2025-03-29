import os
import requests
from bs4 import BeautifulSoup
import zipfile

def baixar_csvs(url, pasta_destino):
    """
    Baixa todos os arquivos ZIP de uma URL, salva na pasta especificada,
    descompacta os arquivos ZIP e exclui os arquivos compactados após a extração.

    Args:
        url (str): URL do diretório contendo os arquivos.
        pasta_destino (str): Caminho da pasta onde os arquivos serão salvos.
    """
    # Cria a pasta de destino, se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Pasta criada: {pasta_destino}")

    # Faz a requisição para obter o HTML da página
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return

    # Analisa o HTML para encontrar os links dos arquivos
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    # Filtra links que terminam com .zip
    arquivos_links = [link['href'] for link in links if link['href'].endswith('.zip')]

    if not arquivos_links:
        print(f"Nenhum arquivo ZIP encontrado em {url}")
        return

    print(f"Encontrados {len(arquivos_links)} arquivos ZIP em {url}. Iniciando download...")

    # Baixa cada arquivo ZIP
    for arquivo_link in arquivos_links:
        arquivo_url = url + arquivo_link
        arquivo_destino = os.path.join(pasta_destino, arquivo_link)

        try:
            print(f"Baixando: {arquivo_link}...")
            arquivo_response = requests.get(arquivo_url)
            if arquivo_response.status_code == 200:
                with open(arquivo_destino, 'wb') as f:
                    f.write(arquivo_response.content)
                print(f"Arquivo salvo: {arquivo_destino}")

                # Descompacta o arquivo ZIP
                print(f"Descompactando: {arquivo_link}...")
                with zipfile.ZipFile(arquivo_destino, 'r') as zip_ref:
                    zip_ref.extractall(pasta_destino)
                print(f"Arquivos extraídos para: {pasta_destino}")

                # Exclui o arquivo ZIP após a extração
                os.remove(arquivo_destino)
                print(f"Arquivo ZIP excluído: {arquivo_link}")
            else:
                print(f"Erro ao baixar {arquivo_link}: {arquivo_response.status_code}")
        except Exception as e:
            print(f"Erro ao processar {arquivo_link}: {e}")

if __name__ == "__main__":
    # URLs e pastas de destino
    urls_pastas = {
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/": "demonstracoes_contabeis2023",
        "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/": "demonstracoes_contabeis2024",
        "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/": "operadoras_ativas"
    }

    # Baixa os arquivos de cada URL e salva na pasta correspondente
    for url, pasta in urls_pastas.items():
        print(f"\nProcessando URL: {url}")
        baixar_csvs(url, pasta)