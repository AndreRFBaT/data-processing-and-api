-- Scripts para as buscas no banco de dados.


-- Busca por trimestre e ano
SELECT
   o.registro_ans,
   o.razao_social,
   d.descricao,  -- Incluindo a descrição no resultado
   MAX(d.data) AS data,
   MAX(d.vl_saldo_final) AS maior_despesa
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE
   d.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'  -- Descrição exata
   AND EXTRACT(MONTH FROM d.data) = 1  -- Mês janeiro (mesmo que você tenha mencionado "outubro" antes, mantendo o filtro de janeiro aqui)
   AND EXTRACT(YEAR FROM d.data) = 2024  -- Ano 2024
   AND d.vl_saldo_final IS NOT NULL  -- Garantir que haja saldo
GROUP BY o.registro_ans, o.razao_social, d.descricao  -- Incluindo a descrição no GROUP BY
ORDER BY maior_despesa DESC  -- Ordenando pelos maiores valores individuais
LIMIT 40;



-- Busca o ano todo
SELECT
   o.registro_ans,
   o.razao_social,
   d.descricao,  -- Incluindo a descrição no resultado
   MAX(d.data) AS data,
   MAX(d.vl_saldo_final) AS maior_despesa
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE
   d.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'  -- Descrição exata
   AND EXTRACT(YEAR FROM d.data) = 2024  -- Apenas o ano de 2024
   AND d.vl_saldo_final IS NOT NULL  -- Garantir que haja saldo
GROUP BY o.registro_ans, o.razao_social, d.descricao  -- Incluindo a descrição no GROUP BY
ORDER BY maior_despesa DESC  -- Ordenando pelos maiores valores individuais
LIMIT 10;


-- Busca o ultimo trimestre
SELECT
   o.registro_ans,
   o.razao_social,
   d.descricao,  -- Incluindo a descrição no resultado
   MAX(d.data) AS data,
   MAX(d.vl_saldo_final) AS maior_despesa
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE
   d.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'  -- Descrição exata
   AND EXTRACT(YEAR FROM d.data) = 2024  -- Apenas o ano de 2024
   AND EXTRACT(MONTH FROM d.data) BETWEEN 10 AND 12  -- Apenas o último trimestre (out, nov, dez)
   AND d.vl_saldo_final IS NOT NULL  -- Garantir que haja saldo
GROUP BY o.registro_ans, o.razao_social, d.descricao  -- Incluindo a descrição no GROUP BY
ORDER BY maior_despesa DESC  -- Ordenando pelos maiores valores individuais
LIMIT 10;
