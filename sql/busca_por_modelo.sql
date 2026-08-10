-- EAN DA PC60T - AUTOMATICO
SELECT DISTINCT B.EAN13                                                       AS "Código"
              , (SELECT Z.CO13DESCRI
                 FROM CO13T Z
                 WHERE Z.CO13EMP06 = A.PC13EM06PA
                   AND Z.CO13CODPRO = A.PC13PROPA)/*A.PC13PROPA*/             AS "Descrição para Faturamento"
               , TRIM(SUBSTR(A.PC13CODIGO, 1, (INSTR(A.PC13CODIGO, '-') - 1))) AS "Referência"
--              , TRIM(A.PC13CODIGO) AS "Referência"
              , A.PC13PROPA                                                   AS "Cód. Auxiliar"
              , '56681513009620'                                              AS "Fornecedor"
              , 'Não'                                                         AS "Fornecedor exclusivo"
              , '2'                                                           AS "Comprador"
              , '1'                                                           AS "Empresa"
              , 'Sim'                                                         AS "Contabiliza saldo em estoque"
              , 'Não'                                                         AS "Indisponível para venda"
              , (SELECT Y.PC04DESCR
                 FROM PC04T Y
                 WHERE Y.PC04CODIGO = A.PC13CLASS)/*A.PC13CLASS*/             AS "Tipo de Produto"
              , (SELECT X.PC03DESCR
                 FROM PC03T X
                 WHERE X.PC03CODEMP = A.PC13EMPLIN
                   AND X.PC03CODIGO = A.PC13LINHA)/*A.PC13LINHA*/             AS "Linha"
              , 'CAPODARTE'                                                   AS "Marca"
              , (SELECT W.PCAIDESC
                 FROM PCAIT W
                 WHERE W.PCAICODEMP = A.PC13EMPIND
                   AND W.PCAICODIGO = A.PC13CODCOL)/*A.PC13CODCOL*/           AS "Coleção"
              , A.PC13DESPLA                                                  AS "Material"
              , NVL((SELECT V.PCEXDESCRI
                     FROM PCEXT V
                     WHERE V.PCEXCODEMP = A.PC13EMP08
                       AND V.PCEXCODIGO = A.PC13ESTCOD), 0)/*A.PC13ESTCOD*/   AS "Estilo de Uso"
              , B.TAMANHO                                                     AS "Tamanho"
              , (SELECT U.PC10DESCR
                 FROM PC10T U
                 WHERE A.PC13COR = U.PC10CODIGO) /*A.PC13COR*/                AS "Cores"
              , TRIM(A.PC13UNIMED)                                            AS "Unidade de venda"
              , ''                                                            AS "Múltiplo de venda"
              , ''                                                            AS "Moeda"
              , '0,01'                                                        AS "Custo com ICMS (R$)"
              , ''                                                            AS "Desconto (%)"
              , ''                                                            AS "Acréscimo (%)"
              , ''                                                            AS "IPI (%)"
              , ''                                                            AS "Frete (R$)"
              , ''                                                            AS "Despesas acessórias (R$)"
              , ''                                                            AS "Substituição tributária (R$)"
              , ''                                                            AS "Diferencial ICMS (R$)"
              , ''                                                            AS "Mark-up (%)"
              , (SELECT TO_CHAR(M.PC33VALSUG, 'FM99G999G990D00')
                 FROM PC33T2 M
                 WHERE M.PC33EMP08 = A.PC13EMP08
                   AND M.PC33CODIGO = 'TP_CAPO_01'
                   AND M.PC33MODELO = A.PC13CODIGO)                           AS "Preço de venda R$"
              , 'Sim'                                                            AS "Permite desconto"
              , ''                                                            AS "Comissão %"
              , '1'                                                           AS "Configuração tributária"
              , A.PC13NBM                                                     AS "NCM"
              , ''                                                            AS "CEST"
              , ''                                                            AS "Produto supérfluo"
              , '1'                                                           AS "Tipo de item"
              , '0'                                                           AS "Origem da mercadoria"
              , ''                                                            AS "Regime de Incidência PIS e COFINS"
              , 'Não'                                                         AS "Produto é brinde"
              , 'Não'                                                         AS "Produto de catálogo"
              , ''                                                            AS "Descrição de catálogo"
              , ''                                                            AS "Disponível na loja virtual"
              , 'Não'                                                         AS "Exige controle"
              , ''                                                            AS "Tipo de controle"
              , ''                                                            AS "Tamanho controle"
              , ''                                                            AS "Classificação de Tamanho"
              , ''                                                            AS "Tipo de Lançamento"
              , '0'                                                           AS "Peso bruto (kg)"
              , '0'                                                           AS "Peso líquido (kg)"
              , ''                                                            AS "Descrição complementar?"
              , ''                                                            AS "Altura (frete)"
              , ''                                                            AS "Largura (frete)"
              , ''                                                            AS "Comprimento (frete)"
              , ''                                                            AS "Altura"
              , ''                                                            AS "Largura"
              , ''                                                            AS "Comprimento"
              , ''                                                            AS "Importado por balança"
              , ''                                                            AS "Produto vendido por (balança)"
              , ''                                                            AS "Quantidade mínima"
              , ''                                                            AS "Quantidade máxima"
              , ''                                                            AS "Quantidade compra"
              , ''                                                            AS "Localização"
              , ''                                                            AS "Observação"
              , B.EAN13                                                       AS "Código de barras"
              , ''                                                            AS "Características"
              , ''                                                            AS "Status"
              , ''                                                            AS "Código Integracao OMS"
              , ''                                                            AS "Produto Desativado"
              , ''														      AS "Bloqueia atualização de preço franqueadora"
--              , LPAD(A.PC13COR, 5, '0') AS teste1
--              , B.COR AS teste2
--, A.PC13DATCRI                                                  AS "Data de Criação do Modelo"
FROM PC13T A
   , (SELECT AUT_EAN13.EMPRESA
           , AUT_EAN13.MODELO
           , AUT_EAN13.COR
           , AUT_EAN13.TAMANHO
           , EAN12 || REPLACE(TRIM(((TRUNC((AUT_EAN13.IMPARES + (AUT_EAN13.PARES * 3)) / 10) + 1) * 10) -
                                   (AUT_EAN13.IMPARES + (AUT_EAN13.PARES * 3))), 10, 0) AS EAN13
      FROM (SELECT DISTINCT EAN2.PC60CODEMP                                            AS EMPRESA
                          , TRIM(SUBSTR(EAN2.PC60CHAVE, 1, 20))                        AS MODELO
                          , TO_NUMBER(REPLACE(SUBSTR(EAN2.PC60CHAVE, 21, 5), '0', '')) AS COR
                          , TRIM(SUBSTR(EAN2.PC60CHAVE, 26, 3))                        AS TAMANHO
                          , EAN2.PC60EAN12                                             AS EAN12
                          , TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 1, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 3, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 5, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 7, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 9, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 11, 1))                               AS IMPARES
                          , TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 2, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 4, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 6, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 8, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 10, 1))
              + TO_NUMBER(SUBSTR(EAN2.PC60EAN12, 12, 1))                               AS PARES
            FROM PC60T EAN2
            WHERE EAN2.PC60CODEMP = 111
               --AND TRIM(SUBSTR(EAN2.PC60CHAVE,1,20)) IN ('4602074-0002','4602074-0003','4602074-0001','4602079-0001','4602079-0002','4602079-0003','4602077-0001','4602077-0002','4602077-0003','4603486-0001','4603486-0002','4603486-0003','4603524-0001','4603524-0002','4603524-0003','4604595-0001','4604595-0002','4603770-0001','4603770-0002','493635-0001','493635-0002','493635-0003','493849-0001','493849-0003','493849-0002','4605496-0001','4605477-0002','4605477-0001','4605477-0003','4605409-0002','4605409-0001','4605474-0002','4605474-0001','4605475-0002','4605475-0003','4605475-0001','4605476-0002','4605476-0003','4605476-0001','4605480-0002','4605480-0001','4605480-0003','4605489-0001','494161-0001','4604822-0001')--,'4018748-11')
           ) AUT_EAN13) B
WHERE A.PC13EMP08 = B.EMPRESA
  AND TRIM(A.PC13CODIGO) = B.MODELO --TRIM(SUBSTR(B.PC60CHAVE,1,20))
--  AND LPAD(A.PC13COR, 5, '0') = B.COR --TRIM(SUBSTR(B.PC60CHAVE,21,5))
--  AND A.PC13COR = B.COR --TRIM(SUBSTR(B.PC60CHAVE,21,5))
  --AND A.PC13ANOPED > 0
  --AND A.PC13DATCRI > '20/11/2024'
--       AND TRIM(SUBSTR(B.PC60CHAVE,26,3)) = '34'
AND TRIM(A.PC13CODIGO) IN ({modelo_placeholders})
--AND B.EAN13 in ()
  --   AND EAN13 NOT LIKE '%9999999999999%'
-- AND A.PC13PROPA = 2313350
--     AND B.TAMANHO = 39
ORDER BY
            TRIM(SUBSTR(A.PC13CODIGO, 1, (INSTR(A.PC13CODIGO, '-') - 1)))
--    TRIM(A.PC13CODIGO)
       , B.TAMANHO