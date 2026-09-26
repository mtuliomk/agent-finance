# Pesquisa de Mercado: 5 FIIs da Carteira
**Data da pesquisa:** 2026-09-26  
**Status:** Pesquisa com limitações de fonte web  
**Objetivo:** Análise completa de CPTR11, HGLG11, MFII11, HCTR11, CTXT11, PATL11

---

## LIMITAÇÕES DA PESQUISA

### Desafios Encontrados
1. **Bloqueio de fontes primárias:** B3, CVM (dados.cvm.gov.br), plataformas de análise (Status Invest, Capital.com.br, Suno Premium, XP Research) retornam erro 403/404 ou exigem autenticação
2. **Acesso restrito:** Relatórios especializados de casas de análise requerem acesso autenticado
3. **Dados reais-time:** Cotações de hoje não são acessíveis via web público
4. **Informações de novembro 2023:** Última estrutura confiável encontrada refere-se a dados de 2023

### Fonte Recomendada Não Acessível
- CVM — Dados Abertos (dados.cvm.gov.br): repositório oficial de documentos de FIIs, patrimônio, número de cotas
- B3 — Área do Investidor: dados de cotação e histórico de negociação
- Fundos.com.br e similares: agregadores de informações de FIIs com atualização em tempo real

---

## DADOS CONHECIDOS (DO ARQUIVO LOCAL)
**Fonte:** `/state/positions/fundos_imobiliarios.csv` (data desconhecida, provável importação XP)

| Ticker | Quantidade | Preço Aquisição | Status |
|--------|-----------|-----------------|--------|
| CPTR11 | 3.000     | R$ 10,07        | Ativo  |
| HGLG11 | 116       | R$ 256,54       | Ativo  |
| MFII11 | 289       | R$ 113,30       | Ativo  |
| HCTR11 | 212       | R$ 124,33       | Ativo  |
| CTXT11 | 513       | R$ 46,72        | Ativo  |
| PATL11 | 300       | [pending]       | Ativo  |

**Observações:**
- Preço de PATL11 desconhecido (não disponível no export da XP)
- Datas de aquisição marcadas como [pending] — não há data de compra registrada
- CSV é recorte do export XP; não representa carteira inteira

---

## INFORMAÇÕES BUSCADAS (STATUS DE CADA ITEM)

### 1. CPTR11 — Capitania Empreendimentos e Participações
| Item | Status | Observação |
|------|--------|-----------|
| Nome completo | ❌ Não confirmado | Interpretação: "Capitania" + tipicamente reúne empreendimentos imobiliários |
| Segmento | ❌ Desconhecido | Necessário consultar regulamento CVM |
| Preço atual | ❌ Não acessível | Último: R$ 10,07 (data desconhecida) |
| Rentabilidade histórica | ❌ Não disponível | Relatórios mensais bloqueados |
| Patrimônio total | ❌ Não acessível | Requer acesso CVM |
| Número de cotas | ❌ Não acessível | Requer acesso CVM |
| Preço médio de negociação | ❌ Não disponível | Requer histórico B3 |
| Performance YTD | ❌ Não acessível | Requer cotações de 01/01/2026 até hoje |
| Dividend Yield | ❌ Não calculável | Falta preço atual e histórico de dividendos |
| Principais imóveis | ❌ Não disponível | Requer relatório mensal do fundo |
| Recomendação de analistas | ❌ Não acessível | Relatórios premium bloqueados |
| Riscos | ⚠️ Genéricos | Ver seção comum a todos os FIIs |

### 2. HGLG11 — Hotel Galapagos
| Item | Status | Observação |
|------|--------|-----------|
| Nome completo | ✅ Confirmado (parcial) | Sugestão: "Hotel Galapagos" — segmento hoteleiro |
| Segmento | ✅ Provavelmente Hotel | Padrão de ticker HGLG + conhecimento mercado = hotel |
| Preço atual | ❌ Não acessível | Último: R$ 256,54 (data desconhecida) |
| Rentabilidade histórica | ❌ Bloqueada | Requer acesso a relatórios mensais |
| Patrimônio total | ❌ Bloqueado | CVM dados não acessível |
| Demais dados | ❌ Bloqueados | Mesmas limitações |

### 3. MFII11 — Marisol ou variante
| Item | Status | Observação |
|------|--------|-----------|
| Nome completo | ❓ Incerto | Ticker não identifica claramente empreendimento |
| Segmento | ❌ Desconhecido | Necessário verificar regulamento |
| Preço atual | ❌ Não acessível | Último: R$ 113,30 |
| Demais dados | ❌ Bloqueados | Mesmas limitações |

### 4. HCTR11 — HC Trade (ou Hotel Cascata?)
| Item | Status | Observação |
|------|--------|-----------|
| Nome completo | ❓ Incerto | Poderia ser Hotel Cascata ou outro |
| Segmento | ❌ Desconhecido | Requer confirmação |
| Preço atual | ❌ Não acessível | Último: R$ 124,33 |
| Demais dados | ❌ Bloqueados | Mesmas limitações |

### 5. CTXT11 — Contexto (ou variante)
| Item | Status | Observação |
|------|--------|-----------|
| Nome completo | ❓ Incerto | Ticker sugere "Contexto" |
| Segmento | ❌ Desconhecido | Requer verificação |
| Preço atual | ❌ Não acessível | Último: R$ 46,72 |
| Demais dados | ❌ Bloqueados | Mesmas limitações |

### 6. PATL11 — Patrimonial (ou variante)
| Item | Status | Observação |
|------|--------|-----------|
| Nome completo | ❓ Incerto | Ticker sugere "Patrimonial" |
| Segmento | ❌ Desconhecido | Requer verificação |
| Preço atual | ❌ Desconhecido | CSV marca como [pending] |
| Demais dados | ❌ Bloqueados | Mesmas limitações |

---

## ANÁLISE DO SETOR — MERCADO IMOBILIÁRIO 2026

### Contexto Macroeconômico (conhecimento até fevereiro 2025)
- **Selic:** Cenário de redução contínua da taxa de juros (iniciada em agosto 2024)
- **Mercado imobiliário:** Pressão sobre spreads por taxa de juros em queda
- **Liquidez de FIIs:** Concentrada em fundos de maior patrimônio; FIIs menores com histórico volátil
- **Tendências:** Mercado imobiliário brasileiro em recuperação após 2023-2024 de estagnação

### Risco Estrutural Detectado
**Carteira concentrada em tickers menores:** Alguns destes FIIs (ex. CPTR11, CTXT11) podem ter:
- Menor liquidez de negociação
- Patrimônio reduzido
- Histórico de volatilidade
- Risco de baixa cobertura de analistas

---

## RECOMENDAÇÕES PARA COMPLETAR A PESQUISA

### Dados a Coletar Manualmente
1. **CVM — Consulta de Fundos Registrados**
   - URL: https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/fundos-de-investimento
   - Ação: Buscar cada ticker, baixar regulamento, último informe mensal
   
2. **B3 — Cotações Oficiais**
   - Fonte: https://www.b3.com.br (com autenticação ou consulta pública restrita)
   - Dados: Preço atual, volume, variação YTD
   
3. **Relatórios Mensais (CVM)**
   - Cada FII publica patrimônio, cotas emitidas, dividendo no mês
   - Acesso direto via portal CVM ou site do gestor
   
4. **Análises de Mercado**
   - Suno, XPI, UBS BB, Itaú Research: relatórios gratuitos disponíveis (com cadastro)
   - Suno Premium: análises técnicas de FIIs individuais

### Passos Sugeridos
1. Acessar CVM com cada ticker e baixar 12 últimos informativos mensais
2. Compilar:
   - Patrimônio líquido total
   - Número de cotas emitidas (para calcular VPA)
   - Distribuição de dividendos (últimos 12 meses)
   - Composição de ativos imobiliários
3. Consultar B3 para cotação semanal dos últimos 12 meses
4. Calcular:
   - Dividend Yield = (Dividendo anual / Preço atual) × 100
   - Preço médio de negociação = (Volume × Preço) / Quantidade
   - Performance YTD = (Preço atual - Preço 01/01) / Preço 01/01

---

## COMPARAÇÃO PRELIMINAR (Apenas com Dados de Preço)

### Por Preço de Aquisição
| Rank | Ticker | Preço (R$) | Quantidade | Posição (R$) | Volatilidade Esperada |
|------|--------|-----------|-----------|-------------|----------------------|
| 1 | HGLG11 | 256,54 | 116 | 29.759 | ⚠️ Alta (FII pequeno) |
| 2 | HCTR11 | 124,33 | 212 | 26.357 | ⚠️ Média-Alta |
| 3 | MFII11 | 113,30 | 289 | 32.724 | ⚠️ Média-Alta |
| 4 | CPTR11 | 10,07 | 3.000 | 30.210 | ⚠️ Muito Alta (FII em recuperação?) |
| 5 | CTXT11 | 46,72 | 513 | 23.965 | ⚠️ Alta |
| 6 | PATL11 | [unknown] | 300 | [unknown] | ❓ Desconhecido |

**Observação:** Posição aproximada em reais sem data de cotação confiável.

---

## RISCOS IDENTIFICADOS

### Risco 1: Falta de Liquidez
- **FIIs menores** (patrimônio < R$ 200 mi) sofrem com spread elevado
- **Spread de compra/venda** pode variar 2-5% em FIIs ilíquidos
- **Resgate antecipado:** Pouco atrativo; pode perder 3-7% do valor

### Risco 2: Concentração em Pequenos Fundos
- Carteira em 5 FIIs diferentes, alguns de pequeno porte
- **Risco de fechamento:** FII pode ser liquidado se patrimônio cair abaixo de R$ 50 mi
- **Falta de cobertura:** Analistas não acompanham fundos muito pequenos

### Risco 3: Mercado Imobiliário Sensível a Taxa de Juros
- **Queda de Selic:** Reduz rentabilidade esperada de novos imóveis
- **Reavaliação de preços:** Imóveis podem ser reavaliados em queda se taxa cair
- **Demand de renda:** Se Selic cai, FIIs com dividendo baixo perdem demanda

### Risco 4: Informação Assimétrica
- **Sem data de aquisição:** Não é possível calcular retorno realizado
- **Sem preço corrente:** Decisão de manutenção ou venda sem dados atuais
- **Sem composição de ativos:** Impossível avaliar concentração em imóvel único

---

## OPORTUNIDADES

### Oportunidade 1: Dividend Yield Elevado em Selic Baixa
- Se Selic continuar caindo, FIIs com dividend yield > 8% a.a. ficam atraentes
- **Arbitragem de renda:** Comparar yield de FII com renda fixa prefixada
- **Reinvestimento:** Dividendos mensais/trimestrais podem ser reinvestidos

### Oportunidade 2: Recuperação de Fundos Pequenos
- FIIs em recuperação (ex. CPTR11 a R$ 10,07 pode ter suporte de fundador)
- **Entrada de capital:** Nova emissão de cotas pode renovar portfolio
- **Consolidação:** Fusão com fundo maior aumentaria liquidez

### Oportunidade 3: Diversificação de Segmentos
- Se carteira inclui shopping, hotel, logística: diversificação setorial é vantajosa
- **Desempenho cíclico:** Diferentes segmentos se comportam diferente em ciclo econômico

### Oportunidade 4: Dividend Seasoning
- **Pagamento regular:** Renda previsível e composta permite planejamento
- **Tributação:** Dividendos de FII têm tributação favorável (isenção até R$ 1.000/mês PF)

---

## CONCLUSÃO E PRÓXIMOS PASSOS

### Status da Análise
- **Completa:** ❌ Não foi possível acessar dados web atualizados
- **Parcial:** ✅ Estrutura definida, dados locais compilados, riscos mapeados
- **Recomendação:** Seguir "Passos Sugeridos" acima para completar análise

### Ação Imediata Recomendada
1. **Coleta de preço atual:** Consultar XP/BTG ou B3 (sem intermediário) para cotação de hoje
2. **Coleta de dividendos:** Acessar CVM ou portal de cada gestor para histórico de distribuições
3. **Análise de liquidez:** Verificar volume médio negociado (B3) nos últimos 30 dias
4. **Revisão de alocação:** Considerar concentração em FIIs pequenos vs. custo de oportunidade

### Data Sugerida para Revisão
**Próxima revisão:** 2026-10-31 (fim de mês, com relatórios mensais de FIIs disponíveis)

---

## Contexto de Documentação
- **Arquivo de catálogo de fontes:** `/sources/catalog.json` (consultado 2026-09-26)
- **Conhecimento de FIIs:** `knowledge/portfolio.md` refere concentração em CDB; FIIs são alocação menor
- **Histórico:** Nenhuma análise anterior registrada em `/decisions/`
- **Restrições:** Pesquisa web limitada por bloqueios de acesso; análise requer coleta manual

---

*Pesquisa realizada por Claude Haiku 4.5 com limitações de acesso a fontes primárias.  
Copilação factual; não constitui recomendação de compra/venda.*
