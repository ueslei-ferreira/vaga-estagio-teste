import requests
from bs4 import BeautifulSoup
import os
import zipfile

def baixa_arquivos(link, diretorio):
    """
    Faz download de um arquivo e salva em uma pasta local.

    Args:
        link (str): URL do arquivo a ser baixado.
        diretorio (str): Caminho completo (incluindo nome do arquivo) onde o conteúdo será salvo.
    Processo
        - Faz uma requisição para o link referido.
        - Salva o documento na pasta especificada.
    """
    
    resposta = requests.get(link)
    if resposta.status_code == 200:
        with open(diretorio, "wb") as arquivo:
            arquivo.write(resposta.content)
        print(f"Download concluído: {diretorio}")
    else:
        print(f"Erro ao baixar {link}")

def compacta_arquivos(pasta, arquivos, zip_nome):
    
    """
    Compacta uma lista de arquivos em um arquivo ZIP.

    Args:
        pasta (str): Caminho da pasta onde os arquivos estão localizados.
        arquivos (list): Lista de nomes dos arquivos a serem compactados.
        zip_name (str): Nome do arquivo ZIP de saída.

    Processo:
        - Itera sobre a lista de arquivos.
        - Adiciona cada arquivo ao arquivo ZIP com o nome relativo.
    """

    try:
        with zipfile.ZipFile(zip_nome, "w") as zipf:
            for arquivo in arquivos:
                # Caminho completo do arquivo
                caminho_completo = os.path.join(pasta, arquivo)
                
                # Verifica se o arquivo existe antes de tentar adicioná-lo
                if os.path.isfile(caminho_completo):
                    # Adiciona o arquivo ao ZIP
                    zipf.write(caminho_completo, arcname=arquivo)
                else:
                    print(f"Arquivo {caminho_completo} não encontrado.")
        
        # Verifica se o arquivo ZIP foi criado com sucesso
        if os.path.exists(zip_nome):
            print(f"Arquivo {zip_nome} criado com sucesso!")
        else:
            print(f"Falha ao criar o arquivo {zip_nome}.")

    except Exception as e:
        print(f"Ocorreu um erro ao criar o arquivo ZIP: {e}")

def escolhe_anexos(url):
    
    """
    Baixa anexos (PDFs) da Atualização do Rol de Procedimentos do gov.br e salva em uma pasta local.

    Args:
        url (str): URL da página contendo os links dos anexos.

    Processo:
        1. Faz uma requisição HTTP para acessar a página.
        2. Extrai links de anexos específicos usando BeautifulSoup.
        3. Faz o download dos arquivos PDF e os salva na pasta 'anexos_baixados'.
        4. Compacta os arquivos baixados em um arquivo ZIP.
    """
    
    resposta = requests.get(url)  # Faz a requisição HTTP

    # Verifica se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, "html.parser")
        
        anexos = []

        # Encontra todos os links dentro da página
        for link in soup.find_all("a"):
            href = link.get("href")
            
            # Filtra apenas os links dos anexos
            if href and (("Anexo_I" in href or "Anexo_II" in href) and href.endswith(".pdf")):
                print("Link encontrado:", href)
                anexos.append(href)
        
        # Criar uma pasta para salvar os PDFs
        nome_pasta = "anexos_baixados"
        os.makedirs(nome_pasta, exist_ok=True)

        cont = 0
        for link in anexos:
            #Define o nome dos anexos a serem baixados em sequencia
            if cont == 0:
                nome_anexo = "Anexo_I.pdf"
                diretorio = os.path.join(nome_pasta, nome_anexo)
            else:
                nome_anexo = "Anexo_II.pdf"
                diretorio = os.path.join(nome_pasta, nome_anexo)
            
            #chama a função para fazer o download do arquivo
            baixa_arquivos(link, diretorio)
            
            cont+=1
            
        # Nome do arquivo ZIP de saída
        zip_nome = "anexos_baixados.zip"

        # Lista de arquivos dentro da pasta
        arquivos = ["Anexo_I.pdf", "Anexo_II.pdf"]
        
        #chama a função para compactar arquivos
        compacta_arquivos(nome_pasta, arquivos, zip_nome)
        
    else:
        print("Erro ao acessar a página:", resposta.status_code)
    
if __name__ == '__main__':
    
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"  # URL do site alvo
    escolhe_anexos(url)