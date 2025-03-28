import csv
from tqdm import tqdm  # Importa o tqdm para a barra de progresso

# Caminho para o arquivo CSV original
input_file = './dados/3T2023.csv'
# Caminho para o novo arquivo corrigido
output_file = './3T2023try.csv'

# Abrir o arquivo CSV original para leitura e o novo arquivo para escrita
with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Contar o número total de linhas no arquivo
    total_lines = sum(1 for row in infile)  # Isso conta as linhas do arquivo

    # Reabrir o arquivo para leitura novamente, pois o contador de linhas o deixou no final
    infile.seek(0)
    
    # Usar tqdm para exibir a barra de progresso
    for row in tqdm(reader, total=total_lines, desc="Processando CSV", unit="linha"):
        # Substituir a vírgula por ponto nas colunas de valores
        if row[4]:  # VL_SALDO_INICIAL (coluna de índice 4)
            row[4] = row[4].replace(',', '.')
        if row[5]:  # VL_SALDO_FINAL (coluna de índice 5)
            row[5] = row[5].replace(',', '.')
        
        # Escrever a linha corrigida no novo arquivo
        writer.writerow(row)

print(f"Arquivo corrigido gerado: {output_file}")
