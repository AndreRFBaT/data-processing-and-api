-- Soma dos valores encontrados no último trimestre
SELECT
   o.registro_ans,
   o.razao_social,
   d.descricao,
   MAX(d.data) AS data,
   SUM(d.vl_saldo_final) AS total_despesa  -- Soma das despesas para evitar distorção
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.reg_ans = o.registro_ans
WHERE
   d.descricao ILIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
   AND EXTRACT(YEAR FROM d.data) = 2024
   AND EXTRACT(MONTH FROM d.data) BETWEEN 10 AND 12  -- Último trimestre
   AND d.vl_saldo_final IS NOT NULL
GROUP BY o.registro_ans, o.razao_social, d.descricao
ORDER BY total_despesa DESC  -- Ordenação correta pela soma total
LIMIT 10;

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
