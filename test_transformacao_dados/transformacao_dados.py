import pdfplumber
import pandas as pd
import zipfile
import os
from tqdm import tqdm

# Configurações:
pdf_path = "../test_web_scraping/anexos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"  # Caminho correto para o PDF
zip_path = "../test_web_scraping/anexos.zip"  # Caminho para o arquivo ZIP

def extrair_dados_pdf(pdf_path):
    """Extrai dados de um PDF e retorna uma lista com os dados.

    A função itera por todas as páginas do PDF e extrai as tabelas. Se a
    tabela for encontrada, adiciona cada linha da tabela na lista de dados.

    Args:
        pdf_path (str): O caminho do PDF a ser extraido.

    Returns:
        list: Uma lista com os dados extraidos do PDF.
    """
    with pdfplumber.open(pdf_path) as pdf:
        dados = []
        paginas = pdf.pages

        # Iterar por todas as páginas e usando o tqdm
        for pagina in tqdm(paginas, desc="Extraindo dados do PDF", unit="pagina"):
            tabela = pagina.extract_table()
            if tabela:
                # Adiciona cada linha da tabela na lista de dados
                for linha in tabela:  #[:]:
                    dados.append(linha)
    return dados

def substituir_abreviacoes(df):
    """Substitui abreviações por descrições completas em um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame que contém as abreviações a serem substituídas.

    Returns:
        pd.DataFrame: O DataFrame com as abreviações substituídas.
    """
    # Dicionário com abreviações e suas descrições atualizadas
    legenda = {
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial",
        "HCO": "Seg. Hospitalar Com Obstetrícia",
        "HSO": "Seg. Hospitalar Sem Obstetrícia",
        "REF": "Plano Referência",
        "PAC": "Procedimento de Alta Complexidade",
        "DUT": "Diretriz de Utilização"
    }

    # Substituir as abreviações no conteúdo do DataFrame
    df.replace(legenda, inplace=True)

    # Substituir as abreviações no nome das colunas
    df.rename(columns=lambda x: legenda.get(x, x), inplace=True)

    return df


def salvar_csv(dados, nome_arquivo):
    """Salva os dados extraídos em um arquivo CSV.

    A função salva os dados extraídos do PDF em um arquivo CSV, substituindo
    as abreviações por descrições completas.

    Args:
        dados (list): A lista de dados extraídos do PDF.
        nome_arquivo (str): O nome do arquivo CSV a ser salvo.

    Returns:
        str: O nome do arquivo CSV salvo.
    """
    # Primeira linha como cabeçalho
    df = pd.DataFrame(dados[1:], columns=dados[0])
    df = substituir_abreviacoes(df)
    # Vírgula como delimitador
    df.to_csv(nome_arquivo, index=False, sep=',')
    print(f"Arquivo CSV salvo em: {nome_arquivo}")
    return nome_arquivo

def compactar_csv(nome_arquivo_csv, nome_arquivo_zip):
    """Compacta um arquivo CSV em um arquivo ZIP.

    Args:
        nome_arquivo_csv (str): O caminho do arquivo CSV a ser compactado.
        nome_arquivo_zip (str): O nome do arquivo ZIP de destino."""

    with zipfile.ZipFile(nome_arquivo_zip, "w") as zipf:
        zipf.write(nome_arquivo_csv, os.path.basename(nome_arquivo_csv))
    print(f"Arquivo compactado em: {nome_arquivo_zip}")

def main():
    """Função principal que executa o processo de transformação de dados.

    Realiza a extração de dados do PDF Anexo I, salva os dados em um arquivo
    CSV e, posteriormente, compacta o arquivo CSV em um arquivo ZIP.

    Caso não seja possível extrair dados do PDF, imprime uma mensagem de erro.
    """
    # Caminho do PDF Anexo I
    pdf_path = "../test_web_scraping/anexos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    # Nome do arquivo CSV
    nome_csv = "rol_procedimentos.csv"
    # Nome do arquivo ZIP
    nome_zip = "Teste_Andre_R_F_Batista.zip"

    # 2.1 - Extração dos dados
    dados = extrair_dados_pdf(pdf_path)

    if dados:
        # 2.2 - Salvar os dados em CSV
        arquivo_csv = salvar_csv(dados, nome_csv)

        # 2.3 - Compactar o CSV em ZIP
        compactar_csv(arquivo_csv, nome_zip)

        # Limpar o arquivo CSV após a compactação
        os.remove(arquivo_csv)
    else:
        print("Não foi possível extrair dados do PDF.")

if __name__ == "__main__":
    main()
