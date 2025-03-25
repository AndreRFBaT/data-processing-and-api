import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile

# Configurações
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
SAVE_DIR = "anexos"
ZIP_FILENAME = "anexos.zip"

def criar_diretorio(diretorio: str):
    """Cria um diretório se não existir."""
    os.makedirs(diretorio, exist_ok=True)

def obter_links_pdfs(url: str) -> list:
    """Faz scraping na página e retorna os links dos PDFs."""
    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao acessar o site")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "Anexo" in href and href.endswith(".pdf"):
            # Ajustar links relativos
            if not href.startswith("http"): 
                href = "https://www.gov.br" + href
            pdf_links.append(href)

    return pdf_links

def baixar_pdfs(links: list, diretorio: str) -> list:
    """Baixa os PDFs encontrados e retorna a lista de arquivos baixados."""
    arquivos_baixados = []

    for pdf_url in links:
        nome_arquivo = os.path.join(diretorio, pdf_url.split("/")[-1])
        response = requests.get(pdf_url)

        if response.status_code == 200:
            with open(nome_arquivo, "wb") as file:
                file.write(response.content)
            arquivos_baixados.append(nome_arquivo)
            print(f"Baixado: {nome_arquivo} - Tamanho: {len(response.content)} bytes")
        else:
            print(f"Erro ao baixar: {pdf_url}")

    return arquivos_baixados

def compactar_arquivos(arquivos: list, zip_filename: str):
    """Compacta os arquivos em um arquivo ZIP."""
    if arquivos:
        with ZipFile(zip_filename, "w") as zipf:
            for file in arquivos:
                zipf.write(file, os.path.basename(file))
        print(f"Arquivos compactados em {zip_filename}")
    else:
        print("Nenhum arquivo para compactar.")

def main():
    """Função principal que orquestra todo o processo."""
    criar_diretorio(SAVE_DIR)

    pdf_links = obter_links_pdfs(URL)
    if not pdf_links:
        print("Nenhum link de PDF encontrado. Encerrando o programa.")
        return

    arquivos_baixados = baixar_pdfs(pdf_links, SAVE_DIR)
    compactar_arquivos(arquivos_baixados, ZIP_FILENAME)

if __name__ == "__main__":
    main()
