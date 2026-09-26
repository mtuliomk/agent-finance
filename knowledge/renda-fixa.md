# Método para renda fixa e liquidez

Em CDB, compare fluxos **líquidos na mesma data final**, não taxas de vitrine. Fixe principal econômico de hoje, data de venda, data de vencimento, horizonte final, taxa contratada, preço executável de saída e aplicação substituta. Informe convenção de dias (corridos/úteis), capitalização, taxas e custos.

1. Manter: calcule fluxos contratuais até vencimento; aplique IR conforme aquisição e evento tributável; se horizonte ultrapassa o vencimento, modele reinvestimento pós-vencimento separadamente.
2. Vender: use cotação **líquida executável** da venda ou preço bruto com custos e IR identificados. O deságio não é uma taxa anual simples: afeta o principal que poderá render por todo o horizonte restante.
3. Reinvestir: capital líquido da venda é o novo principal; nova data de aquisição reinicia prazo da tabela regressiva. Calcule IR no resgate final da nova aplicação.
4. Exiba valor líquido final e diferença absoluta/percentual; calcule taxa de equilíbrio da alternativa quando os dados permitirem. Faça sensibilidade para preço de saída, taxa disponível e horizonte. Se não houver cotação executável, a conclusão é condicional.

Taxa prefixada, `% CDI`, `CDI + spread` e IPCA+ não são diretamente comparáveis: explicite trajetória de índice, inflação e datas. LCA pode ter tratamento tributário distinto; CRI tem risco e liquidez próprios. Nunca aplique cobertura FGC a CRI por analogia.

Liquidez significa possibilidade, prazo e preço de venda, não somente vencimento. Considere necessidade de caixa, spread de mercado e concentração antes de maximizar valor esperado.
