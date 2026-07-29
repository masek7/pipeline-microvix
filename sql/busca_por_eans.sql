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
              , 'Sim'                                                         AS "Permite desconto"
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
              , ''                                                            AS "Bloqueia atualização de preço franqueadora"
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
--   AND A.PC13CODIGO IN ('4015042-0037','4015042-0010','4015042-0038','4019922-0001','4019922-0002','4019920-0001','4019912-0001','4019912-0002','4019921-0003','4019910-0001','4019910-0004','4019920-0002','4019921-0001','4019965-0001','4019965-0003','4019916-0003','4019910-0002','4019921-0004','4019908-0002','4019141-0033','4019141-0034','4019141-0035','4019231-0015','4019231-0013','4019231-0014','4019908-0003','4019908-0001','4019910-0003','4019916-0004','4019916-0002','4019916-0001','4019920-0003','4019921-0002','4019965-0002','4019903-0001','4019903-0002','4019903-0003','4019911-0001','4019914-0001','4019911-0002','4019917-0002','4019904-0001','4019904-0003','4019905-0003','4019905-0001','4019915-0001','4019919-0002','4019914-0002','4019917-0001','4019913-0001','4019919-0001','4019913-0002','4019915-0003','4017642-0014','4019918-0003','4019919-0003','4019905-0002','4019917-0003','4019918-0001','4019918-0002','4017642-0015','4019904-0002','4019906-0001','4019906-0002','4019906-0003','4019907-0002','4019907-0001','4019907-0003','4019907-0004','4019915-0002','4019927-0001','4019927-0002','4019923-0003','4018438-0025','4019802-0005','4019802-0006','4019816-0007','4018438-0023','4019928-0002','4019909-0002','4019816-0006','4019928-0001','4018438-0022','4019902-0001','4019923-0002','4019909-0003','4019925-0001','4019668-0015','4019668-0013','4019925-0003','4019923-0001','4018438-0024','4018823-0016','4018823-0014','4018823-0015','4019668-0014','4019802-0004','4019816-0008','4019902-0004','4019902-0002','4019902-0003','4019909-0001','4019925-0002','4019928-0003','4019779-0005','4019898-0010','4019771-0010','4019594-0011','4019594-0013','4019594-0012','4019771-0011','4019772-0013','4019772-0012','4019779-0007','4019779-0006','4019779-0008','4019898-0011','4019899-0010','4019899-0011','4019771-0004','4019772-0003','4003066-0037','4003066-0038','4006834-0029','4006834-0030','4011201-0030','4011201-0031','4015038-0031','4015038-0032','4019901-0003','4019901-0001','4016738-0039','4016738-0038','4019773-0006','4016738-0036','4019197-0008','4019901-0002','4019773-0005','4019197-0007','4019197-0006','4019900-0001','4019900-0002','4019900-0003','4016465-0042','4016465-0040','4016465-0041','4016738-0037','4015042-0012','4605838-0001','4605838-0002','4605839-0001','4605839-0002','4605839-0004','4605838-0004','4605838-0003','4605839-0003','4605847-0005','4605840-0003','4605847-0004','4605847-0001','4605847-0003','4605872-0003','4605872-0001','4605872-0002','4605840-0001','4605840-0002','4605847-0002','4605843-0001','4605845-0001','4605845-0002','4605844-0001','4604124-0020','4604124-0018','4604124-0019','4601866-0038','4605837-0002','4601866-0036','4605836-0003','4605836-0002','4605836-0001','4601571-0036','4601571-0035','4601571-0037','4601866-0037','4605836-0006','4605836-0005','4605836-0004','4605837-0004','4605837-0003','4605837-0001','4605842-0001','4605846-0001','4605846-0002','4605842-0002','4605842-0003','4602416-0018','4603850-0025','4602887-0027','4602887-0028','495053-0014','495053-0015','495053-0016','495059-0003','4602416-0017','492315-0009')
  AND B.EAN13 in ({ean_placeholders})--(7900478012549)
--   AND EAN13 NOT LIKE '%9999999999999%'
-- AND A.PC13PROPA = 2313350
--     AND B.TAMANHO = 39
ORDER BY TRIM(SUBSTR(A.PC13CODIGO, 1, (INSTR(A.PC13CODIGO, '-') - 1)))
--    TRIM(A.PC13CODIGO)
       , B.TAMANHO