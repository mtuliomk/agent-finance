---
name: analise-risco
description: Avalia concentração, crédito, liquidez e cobertura FGC da carteira ou de uma compra proposta; use em risco por emissor e limites de garantia.
---

# Análise de risco

**Consultar:** `knowledge/risco.md`, `knowledge/portfolio.md`, snapshots e manifesto; `knowledge/tributacao.md` se venda for mitigação. Use `make fontes-listar TOPIC=credito` para localizar FGC e fontes de crédito; pesquise emissor/BCB conforme necessidade.

1. Agrupe CDB/LCA elegíveis por instituição/conglomerado em todas as custódias disponíveis; liste agrupamentos desconhecidos. Confirme produto, emissor e regra FGC vigente.
2. Compare saldo atual e juros projetados com limite aplicável; reporte também consumo do teto global de quatro anos somente se o histórico de garantias pagas for conhecido. Não chame cobertura jurídica de liquidez imediata.
3. Examine riscos não cobertos: CRI, ações, FIIs, correlação entre emissores, prazos e preço de saída. Proponha mitigação e custos, sem inventar limite pessoal.

**Saída:** matriz por emissor/conglomerado, cobertura potencial e incertezas, concentrações e opções de mitigação. **Qualidade:** custodiante não substitui emissor; ausência de dados não vira cobertura presumida.
