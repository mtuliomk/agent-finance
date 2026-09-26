---
name: analise-cdb
description: Avalia CDB e decisão de manter versus vender e reinvestir, incluindo preço de saída e IR em cada perna; use para resgate antecipado ou nova compra de CDB.
---

# Análise de CDB

**Consultar:** `knowledge/portfolio.md`, `knowledge/renda-fixa.md`, `knowledge/tributacao.md`, `knowledge/risco.md`; posição em `state/positions/` e decisão anterior do mesmo papel, se houver. Localize fontes de FGC/IR com `make fontes-listar TOPIC=credito` e `make fontes-listar TOPIC=tributacao`; oferta e cotação executável devem vir de documento/corretora.

1. Fixe lote, data de aquisição, taxa/convenção, vencimento, valor atual e preço líquido de saída. Peça dado ausente; sem preço executável, só cenários.
2. Calcule manter até o horizonte e vender+reinvestir na **mesma data final**. Trate IR de venda e de nova aplicação separadamente, com prazos corretos; inclua deságio capitalizado, custos e possível IOF. Mostre contas ou fórmula reproduzível.
3. Faça sensibilidade de taxa de reinvestimento, preço de saída e horizonte. Avalie risco do emissor, FGC, liquidez e risco de reinvestimento; pitch de assessor requer verificação.

**Saída:** premissas/fontes, fluxos líquidos por cenário, ponto de equilíbrio se possível, riscos e conclusão condicional. **Qualidade:** não compare taxa nominal com retorno líquido nem atribua a Pine/BMG decisões não reconstruídas.
