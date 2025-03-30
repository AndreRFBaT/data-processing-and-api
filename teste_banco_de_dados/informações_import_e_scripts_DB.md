# Comandos necessários para o script de importação do banco de dados

# Tarefas de Código:

* 3.3. Crie queries para estruturar tabelas necessárias para o arquivo csv.
* 3.4. Elabore queries para importar o conteúdo dos arquivos preparados, atentando para o encoding correto.

## Criação das tabelas

### Criação da tabela de demonstrativos contábeis
```sql
-- Criação da tabela de demonstrativos contábeis
CREATE TABLE demonstrativos_contabeis (
    data DATE,
    reg_ans INT,
    cd_conta_contabil INT,
    descricao VARCHAR(255),
    vl_saldo_inicial DECIMAL(15, 2),
    vl_saldo_final DECIMAL(15, 2)
);
```

### Criação da tabela de operadoras ativas

```sql
CREATE TABLE operadoras (
    registro_ans INT PRIMARY KEY,
    cnpj VARCHAR(18) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(3),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_de_comercializacao VARCHAR(255),
    data_registro_ans DATE
);
```
---


## Importação dos dados no formato csv e com enconding UTF-8

### Mover os arquivos para a pasta /tmp/ (Ubuntu)
```bash
# Movendo os arquivos para a pasta /tmp/ por causa da permissão do diretório

# Movendo os arquivos para a pasta /tmp/
mv caminho/para/arquivos_contendo_dados_de_2023_e_2024.csv /tmp/
# Movendo os arquivos para a pasta /tmp/
mv caminho/para/Relatorio_cadop.csv /tmp/

```

### Importação dos dados no formato csv e com enconding UTF-8

- Importação dos dados de demonstrativos contábeis no formato csv e com enconding UTF-8
```sql
\COPY teste_para_enviar (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM '/tmp/3T2024.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
```
- Importação dos dados de operadoras ativas no formato csv e com enconding UTF-8
```sql
\COPY teste_operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans)
FROM '/tmp/Relatorio_cadop.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
```
---


## Comandos para verificar se os dados foram importados corretamente

### Verificando se os dados foram importados corretamente

```sql
-- Comando para demonstrativos contábeis
SELECT * FROM demonstrativos_contabeis LIMIT 10;

-- Comando para operadoras
SELECT * FROM operadoras LIMIT 10;
```

### Saída do comando:

![alt text](/teste_banco_de_dados/imagens_tarefa_DB/image.png)

```bash
postgres=# SELECT * FROM demonstrativos_contabeis LIMIT 10;
    data    | reg_ans | cd_conta_contabil |                 descricao                 | vl_saldo_inicial | vl_saldo_final 
------------+---------+-------------------+-------------------------------------------+------------------+----------------
 2024-07-01 | 347825  | 1314              | TÍTULOS E CRÉDITOS A RECEBER              |        812002.13 |      832679.65
 2024-07-01 | 347825  | 13142             | TÍTULOS A RECEBER                         |        812002.13 |      832679.65
 2024-07-01 | 347825  | 131429            | Títulos a Receber                         |        812002.13 |      832679.65
 2024-07-01 | 347825  | 13142908          | Outros Títulos a Receber                  |        812002.13 |      832679.65
 2024-07-01 | 347825  | 131429081         | Outros Títulos a Receber                  |        812002.13 |      832679.65
 2024-07-01 | 347825  | 1317              | DEPÓSITOS JUDICIAIS E FISCAIS             |        216680.87 |      216680.87
 2024-07-01 | 347825  | 13171             | DEPÓSITOS JUDICIAIS E FISCAIS             |        216680.87 |      216680.87
 2024-07-01 | 347825  | 131719            | Depósitos Judiciais e Fiscais             |        216680.87 |      216680.87
 2024-07-01 | 347825  | 13171901          | Depósitos Judiciais e Fiscais             |        216680.87 |      216680.87
 2024-07-01 | 347825  | 131719011         | Depósitos Judiciais - Eventos / Sinistros |          7490.17 |        7490.17
(10 linhas)
```

### No DBeaver
![alt text](</teste_banco_de_dados/imagens_tarefa_DB/prova do operadoras estão funcionando.png>)
---

<br></br>

# Tarefas de desenvolvimento de queries analíticas:

## 3.5. Desenvolva uma query analítica para responder:

## · Quais as 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre?

### Solução:

Script SQL para responder a pergunta sobre os valores encontrados no último trimestre

```sql
-- Soma dos valores encontrados no último trimestre
SELECT
   o.registro_ans,
   o.razao_social,
   d.descricao,
   MAX(d.data) AS data,
   -- Soma das despesas para evitar distorção
   SUM(d.vl_saldo_final) AS total_despesa
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE
   d.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'

   -- Apenas o ano de 2024
   AND EXTRACT(YEAR FROM d.data) = 2024

   -- Último trimestre
   AND EXTRACT(MONTH FROM d.data) BETWEEN 10 AND 12
   AND d.vl_saldo_final IS NOT NULL

GROUP BY o.registro_ans, o.razao_social, d.descricao
-- Ordenação correta pela soma total
ORDER BY total_despesa DESC
LIMIT 10;
```

### Resultado:

### No DBeaver
![alt text](</teste_banco_de_dados/imagens_tarefa_DB/saida demonstrativos beaver.png>)

### No terminal

![alt text](/teste_banco_de_dados/imagens_tarefa_DB/image-4.png)

```sql
 registro_ans |                       razao_social                       |                                      descricao                                       |    data    | total_despesa  
--------------+----------------------------------------------------------+--------------------------------------------------------------------------------------+------------+----------------
 326305       | AMIL ASSISTÊNCIA MÉDICA INTERNACIONAL S.A.               | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 20820818085.36
 359017       | NOTRE DAME INTERMÉDICA SAÚDE S.A.                        | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  9307980465.62
 368253       | HAPVIDA ASSISTENCIA MEDICA S.A.                          | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  7755562753.15
 346659       | CAIXA DE ASSISTÊNCIA DOS FUNCIONÁRIOS DO BANCO DO BRASIL | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  7459368017.21
 339679       | UNIMED NACIONAL - COOPERATIVA CENTRAL                    | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  7002487899.10
 302147       | PREVENT SENIOR PRIVATE OPERADORA DE SAÚDE LTDA           | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  5920615078.62
 343889       | UNIMED BELO HORIZONTE COOPERATIVA DE TRABALHO MÉDICO     | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  5411476065.42
 323080       | GEAP AUTOGESTÃO EM SAÚDE                                 | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  3435605702.55
 352501       | UNIMED PORTO ALEGRE - COOPERATIVA MÉDICA LTDA.           | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  3368044333.04
 335690       | UNIMED CAMPINAS - COOPERATIVA DE TRABALHO MÉDICO         | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  3059368303.48
(10 linhas)
```
---
<br></br>


## · Quais as 10 operadoras com maiores despesas nessa categoria no último ano?

### Solução:
```sql
-- Soma dos valores encontrados no ano todo
SELECT
   o.registro_ans,
   o.razao_social,
   d.descricao,
   MAX(d.data) AS data,
   SUM(d.vl_saldo_final) AS total_despesa  -- Soma das despesas para o ano inteiro
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE
   d.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
   AND EXTRACT(YEAR FROM d.data) = 2024
   AND d.vl_saldo_final IS NOT NULL
GROUP BY o.registro_ans, o.razao_social, d.descricao
ORDER BY total_despesa DESC  -- Ordenação pela soma total
LIMIT 10;
```

### Resultado:

### No DBeaver:
![alt text](/teste_banco_de_dados/imagens_tarefa_DB/image-1.png)

![alt text](/teste_banco_de_dados/imagens_tarefa_DB/image-2.png)


### No terminal:

![alt text](/teste_banco_de_dados/imagens_tarefa_DB/image-3.png)

```sql
 registro_ans |                       razao_social                       |                                      descricao                                       |    data    | total_despesa  
--------------+----------------------------------------------------------+--------------------------------------------------------------------------------------+------------+----------------
 326305       | AMIL ASSISTÊNCIA MÉDICA INTERNACIONAL S.A.               | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 51005557507.35
 359017       | NOTRE DAME INTERMÉDICA SAÚDE S.A.                        | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 23545735832.81
 368253       | HAPVIDA ASSISTENCIA MEDICA S.A.                          | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 19385534464.99
 346659       | CAIXA DE ASSISTÊNCIA DOS FUNCIONÁRIOS DO BANCO DO BRASIL | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 18412177093.19
 339679       | UNIMED NACIONAL - COOPERATIVA CENTRAL                    | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 17391267369.70
 302147       | PREVENT SENIOR PRIVATE OPERADORA DE SAÚDE LTDA           | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 14635643010.58
 343889       | UNIMED BELO HORIZONTE COOPERATIVA DE TRABALHO MÉDICO     | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 | 13162050667.89
 323080       | GEAP AUTOGESTÃO EM SAÚDE                                 | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  8769323198.69
 352501       | UNIMED PORTO ALEGRE - COOPERATIVA MÉDICA LTDA.           | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  8150206390.68
 335690       | UNIMED CAMPINAS - COOPERATIVA DE TRABALHO MÉDICO         | EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR  | 2024-10-01 |  7627984233.80
(10 linhas)
```