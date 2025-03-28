import csv
from tqdm import tqdm
import re

# Caminhos dos arquivos
input_file = './demonstrativos_finais.csv'
output_file = './demonstrativos_finais_corrigido.csv'
error_file = './demonstrativos_finais_erros.csv'

# Função para validar e formatar números decimais
def validar_numero(valor):
    valor = valor.strip()  # Remove espaços extras
    if re.match(r'^-?\d+(,\d+)?$', valor):  # Verifica se é um número válido
        return valor.replace(',', '.')  # Substitui vírgula por ponto
    return None  # Retorna None para valores inválidos

# Função para validar e limitar números inteiros ao BIGINT
def validar_bigint(valor):
    valor = valor.strip()
    if valor.isdigit():  # Se for um número inteiro positivo
        num = int(valor)
        if num > 9223372036854775807:  # Se ultrapassar o BIGINT
            return None  # Considera inválido
        return str(num)
    return None  # Retorna None para valores inválidos

# Processamento do arquivo CSV
with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile, \
     open(error_file, mode='w', newline='', encoding='utf-8') as errfile:

    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')
    error_writer = csv.writer(errfile, delimiter=';')

    # Contar linhas para a barra de progresso
    total_lines = sum(1 for _ in infile)
    infile.seek(0)  # Voltar ao início do arquivo

    for row in tqdm(reader, total=total_lines, desc="Processando CSV", unit="linha"):
        if len(row) > 5:  # Garantir que existem colunas suficientes
            valid_row = True  # Assume que a linha é válida

            row[4] = validar_numero(row[4]) if row[4] else ''
            row[5] = validar_bigint(row[5]) if row[5] else ''

            # Se algum valor for None, a linha é inválida
            if row[4] is None or row[5] is None:
                error_writer.writerow(row)  # Salva no arquivo de erros
                valid_row = False

            if valid_row:
                writer.writerow(row)  # Salva no arquivo corrigido

print(f"Arquivo corrigido gerado: {output_file}")
print(f"Arquivo com erros gerado: {error_file}")
