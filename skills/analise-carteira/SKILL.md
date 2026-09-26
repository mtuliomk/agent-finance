---
name: analise-carteira
description: Analisa alocação, exposição e lacunas da carteira pessoal a partir dos snapshots locais; use em perguntas sobre carteira atual ou rebalanceamento.
---

# Análise de carteira

**Consultar:** `knowledge/portfolio.md`, `knowledge/schema-posicoes.md`, `state/positions/manifest.json` e snapshots disponíveis; `knowledge/risco.md` para crédito. Web só para indicadores/preços externos necessários, conforme `knowledge/fontes.md`.

1. Verifique datas, custodiantes cobertos, posições sem `market_value` e moedas. Não chame fotografia incompleta de carteira total. Agregue por classe, emissor/conglomerado, vencimento e liquidez; não some moedas sem câmbio datado.
2. Compare concentração e necessidade de caixa com a política pessoal explícita; onde não há limite definido, mostre exposição e peça o critério antes de rotular excesso subjetivo. Acione `analise-risco` para FGC/crédito.
3. Para alternativas, use `comparar-investimentos`; confirme ofertas via fonte atual. Separe diagnóstico, hipótese e proposta.

**Saída:** data-base/cobertura, tabela de valores e percentuais calculáveis, concentrações, vencimentos/liquidez, riscos, lacunas e próximos dados úteis. **Qualidade:** totais conciliados ao snapshot, denominador declarado e nenhuma posição presumida.
