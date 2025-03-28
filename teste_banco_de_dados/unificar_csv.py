import pandas as pd
import os
from tqdm import tqdm

# Diretório onde estão os arquivos
diretorio = "./dados"

# Lista dos arquivos CSV (ajuste os nomes conforme necessário)
arquivos = [
    "1T2023.csv", "2T2023.csv", "3T2023.csv", "4T2023.csv",
    "1T2024.csv", "2T2024.csv", "3T2024.csv", "4T2024.csv"
]

# Lista para armazenar os dados
dados = []
erros = []

# Processar cada arquivo
for arquivo in tqdm(arquivos, desc="Processando arquivos"):
    caminho = os.path.join(diretorio, arquivo)
    
    try:
        df = pd.read_csv(caminho, delimiter=";", dtype=str)  # Ler como string para evitar erros iniciais
        
        # Remover espaços extras dos nomes das colunas
        df.columns = df.columns.str.strip()

        # Substituir vírgulas por pontos em colunas numéricas
        colunas_numericas = ["VL_SALDO_INICIAL", "VL_SALDO_FINAL"]
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = df[col].str.replace(",", ".", regex=False)

        # Converter para numérico, armazenando erros
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Remover linhas que contenham erros
        erros_df = df[df.isna().any(axis=1)]
        if not erros_df.empty:
            erros.append(erros_df)

        # Adicionar ao conjunto de dados unificado
        dados.append(df.dropna())  # Remove linhas com erro

    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")

# Concatenar todos os dados
df_final = pd.concat(dados, ignore_index=True)

# Salvar o arquivo final corrigido
df_final.to_csv("dados_unificados_corrigidos.csv", sep=";", index=False, encoding="utf-8")

# Salvar os erros encontrados em um arquivo separado
if erros:
    df_erros = pd.concat(erros, ignore_index=True)
    df_erros.to_csv("erros_encontrados.csv", sep=";", index=False, encoding="utf-8")
    print("Arquivo de erros gerado: erros_encontrados.csv")
else:
    print("Nenhum erro encontrado nos arquivos.")

print("Arquivo final gerado: dados_unificados_corrigidos.csv")
