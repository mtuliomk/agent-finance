# Guia de Coleta Restante: Dados de FIIs via CVM e BCB
**Data:** 2026-09-26  
**Objetivo:** Completar pesquisa com dados que ainda não foram obtidos via fontes confiáveis do catálogo  
**Tempo Estimado:** 45-60 minutos (coleta manual)  
**Fontes:** CVM (primária), BCB (suporte), eventualmente gestor/administrador (secundária)

---

## 1. DADOS ESTRUTURAIS DO FII (Via CVM)

### Passo 1.1: Acessar Portal de Consultas da CVM

1. Navegue até: **https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/fundos-de-investimento**
2. Procure pela opção **"Fundos Registrados"** ou **"Busca de Fundos"**
3. Use a barra de busca para cada ticker

### Passo 1.2: Para Cada FII (CPTR11, HGLG11, MFII11, HCTR11, CTXT11, PATL11)

**Procedimento:**
1. Digite o ticker (ex: `CPTR11`) na barra de busca
2. Localizar o fundo na lista de resultados
3. Clicar no nome do fundo para acessar pasta de documentos

**Documentos a Baixar (por fundo):**

#### Documento 1: Regulamento do Fundo
- **Identificação:** "Regulamento" ou "Regulamento Aprovado"
- **Por que:** Contém definição de segmento, objetivos, política de distribuição
- **O que extrair:**
  - Nome completo do fundo (aba inicial ou art. 1)
  - Segmento imobiliário (ex: shopping, hotel, logística, residencial)
  - Composição de ativos principais
  - Frequência de distribuição de rendimentos
  - Data de aprovação e CNPJ

#### Documento 2: Informe Mensal — Mês Mais Recente (ex: Agosto 2026)
- **Identificação:** "Informe Mensal", "Extrato de Informações" ou "Monthly Report"
- **Por que:** Contém PL, número de cotas, dividendo do mês
- **O que extrair:**
  - Patrimônio Líquido (PL): valor total em R$
  - Data do PL
  - Número de cotas emitidas
  - Valor da cota (ou calcular: PL / Cotas)
  - Distribuição do mês (dividendo por cota)
  - Composição de ativos

#### Documentos 3-7: Informativos dos 5 Meses Anteriores
- **Identificação:** Informativos mensais (julho, junho, maio, abril, março 2026)
- **Por que:** Compilar tendência de dividendos (últimos 6 meses)
- **O que extrair:** Distribuição mensal (dividendo por cota)

---

## 2. COMPILAÇÃO: DIVIDENDOS DOS ÚLTIMOS 6 MESES

### Estrutura de Coleta

Para cada FII, criar tabela:

```
| Mês (2026) | Dividendo/Cota (R$) | Observações |
|---|---|---|
| Setembro | [a preencher] | |
| Agosto | [a preencher] | |
| Julho | [a preencher] | |
| Junho | [a preencher] | |
| Maio | [a preencher] | |
| Abril | [a preencher] | |
```

**Cálculo de Yield Anualizado (após coleta):**
- **Somatório 6 meses:** Dividendo/cota × 6 (para aproximar 12 meses)
- **Yield Anual Aproximado:** (Soma 6 meses × 2) / Preço atual × 100%
- **Observação:** Resultado é apenas orientativo; dividendos não são garantidos

---

## 3. DADOS CRÍTICOS: PATL11 (Preço de Aquisição)

### Passo 3.1: Procurar em Múltiplas Fontes

**Fonte 1 — Informe de Aquisição (XP):**
- Verificar arquivo original na pasta `/inbox/` ou `/state/raw/`
- Procurar por nota de corretagem ou confirmação de aquisição que identifique preço

**Fonte 2 — CVM (se arquivo encontrado):**
- Alguns informativos incluem histórico de entradas/saídas
- Verificar abas de "Composição de Ativos" ou "Movimentação do Mês"

**Fonte 3 — Cotação Histórica (B3 ou corretora):**
- Se não encontrado preço exato, usar cotação aproximada do dia da aquisição (se data conhecida)
- Marcar como "[aproximado — data desconhecida]" para rastreabilidade

**Se Não Encontrado:**
- Documentar em `decisions/pesquisa-fiis-2026-09-26.md` como [não encontrado na origem]
- Usar cotação mais antiga disponível (ex: R$ 46-60 baseado em padrão de outros FIIs)
- Marcar com flag [⚠️ Estimado]

---

## 4. CONTEXTO MACROECONÔMICO (Via BCB)

### Passo 4.1: Taxa Selic Atual

1. Navegue até: **https://www.bcb.gov.br/controleinflacao/historicotaxasjuros**
2. Procure pela **última decisão do Copom** ou **taxa meta atual**
3. Registrar:
   - Taxa Selic meta (%)
   - Data da decisão
   - Previsão de próxima reunião

**Alternativa:** Se o site não carregar, procure por:
- https://www.bcb.gov.br/controleinflacao/comunicadoscopom (comunicados)
- Buscar "Copom [setembro 2026]" ou mês atual

### Passo 4.2: Últimos 3 Comunicados do Copom

1. Acessar: **https://www.bcb.gov.br/controleinflacao/comunicadoscopom**
2. Baixar ou anotar:
   - Data da reunião
   - Decisão (taxa meta)
   - Justificativa (se disponível)
   - Próxima reunião prevista

**Campos a Registrar:**

| Reunião | Data | Selic Meta | Decisão (Alta/Manutenção/Baixa) | Justificativa Resumida |
|---|---|---|---|---|
| Mais Recente | [data] | [%] | | |
| -1 Reunião | [data] | [%] | | |
| -2 Reuniões | [data] | [%] | | |

### Passo 4.3: Relatório Focus (Expectativas)

1. Acessar: **https://www.bcb.gov.br/publicacoes/focus**
2. Procurar pela **edição mais recente** de setembro 2026
3. Localizar campo **"Selic — fim de período"** (próximas reuniões)
4. Anotar:
   - Expectativa para fim de 2026
   - Expectativa para fim de 2027
   - Intervalo (percentil 25-75 ou mediana/desvio)

---

## 5. TEMPLATE DE COMPILAÇÃO

Use este template para organizar dados de CADA FII:

```markdown
## [TICKER] — [Nome Completo]

### Dados Estruturais (CVM)
- **CNPJ:** [extraído do regulamento]
- **Segmento:** [hotel/shopping/logística/residencial/misto]
- **Data de Emissão:** [data]
- **Regulamento Consultado:** [link ou referência]
- **Data da Consulta:** 2026-09-26

### Patrimônio e Cotas (Informe Mensal)
- **Patrimônio Líquido (PL):** R$ [valor] (data: [mês/ano])
- **Número de Cotas:** [número] (data: [mês/ano])
- **Valor Patrimonial/Cota (VPA):** R$ [PL/Cotas] 
  - Fórmula: R$ [PL] / [Cotas] = R$ [VPA]
- **Preço Corrente:** [pending — exigir cotação B3 ou corretora]

### Distribuição de Dividendos (Últimos 6 Meses)
| Mês | Dividendo/Cota (R$) | % de VPA |
|---|---|---|
| Set/26 | R$ [x] | [x/VPA]% |
| Ago/26 | R$ [x] | [x/VPA]% |
| Jul/26 | R$ [x] | [x/VPA]% |
| Jun/26 | R$ [x] | [x/VPA]% |
| Mai/26 | R$ [x] | [x/VPA]% |
| Abr/26 | R$ [x] | [x/VPA]% |
| **Somatório 6M** | **R$ [soma]** | — |
| **Anualizado (×2)** | **R$ [soma×2]** | **[%/VPA]** |

### Composição de Ativos (Últimos 5 Imóveis Principais)
| Descrição | Valor (R$) | % PL |
|---|---|---|
| [Imóvel 1] | R$ [x] | [%] |
| [Imóvel 2] | R$ [x] | [%] |
| [Imóvel 3] | R$ [x] | [%] |
| [Imóvel 4] | R$ [x] | [%] |
| [Imóvel 5] | R$ [x] | [%] |

### Análise
- **Liquidez:** [Alta/Média/Baixa] — Baseado em [volume médio/patrimônio]
- **Yield (6M Anualizado):** [%] — = (R$ [dividendos 6M × 2]) / R$ [preço corrente] × 100
- **Status da Cotação:** [Preço de aquisição: R$ [x.xx] (data [desconhecida])]
- **Risco de Fechamento:** [Sim/Não] — PL > R$ 50M? [confirmar]

### Última Atualização
- **Data de Consulta:** 2026-09-26
- **Informe Consultado:** Setembro 2026 (ou [mês mais recente disponível])
- **Documentos Baixados:** [Regulamento, Informativos Ago/26, Jul/26, Jun/26, Mai/26, Abr/26]

```

---

## 6. FLUXO DE TRABALHO RECOMENDADO

### Dia 1: Coleta CVM (2 horas)

1. Acessar CVM em paralelo para 3 FIIs (ex: CPTR11, HGLG11, MFII11)
2. Para cada fundo:
   - [ ] Baixar regulamento
   - [ ] Baixar 6 informativos (Ago/26 a Abr/26)
3. Extrair dados para template acima

### Dia 1 (continua): Coleta CVM (+ 1 hora)

4. Repetir procedimento para 3 FIIs restantes (HCTR11, CTXT11, PATL11)
5. Prioridade especial: PATL11 → procurar preço de aquisição

### Dia 2: Compilação (1 hora)

6. Organizar dados no template por FII
7. Calcular PL/Cota, VPA, Yields
8. Compilar tabela-resumo dos 6 fundos

### Dia 2 (continua): Contexto Macroeconômico (30 min)

9. Acessar BCB para Selic, Copom, Focus
10. Registrar em template de contexto (vide seção 4)

### Dia 2 (final): Validação (30 min)

11. Revisar dados contra AGENTES.md e regra #1 (separar fato do arquivo)
12. Citar data e documento específico de cada informação
13. Marcar [pending] para dados não encontrados
14. Atualizar `pesquisa-fiis-2026-09-26.md` com resultados

---

## 7. VALIDAÇÃO E MARCA DE DATA

### Para Cada Dado Compilado, Citar:
1. **Arquivo:** "Informe Mensal — CVM — CPTR11 — Agosto 2026"
2. **Data:** "Informe com data-base 31/08/2026"
3. **Linha/Campo:** "Patrimônio Líquido: R$ [x] (p. 2, campo PL)"
4. **Fonte URL:** "https://www.gov.br/cvm/pt-br/assuntos/regulados/..." (se aplicável)

**Exemplo Completo:**
> Patrimônio Líquido (PL) de CPTR11: R$ 245.300.000 (data-base 31/08/2026)
> *Fonte: CVM — Informe Mensal de CPTR11 — Agosto 2026, p. 2*

---

## 8. TRATAMENTO DE DADOS NÃO ENCONTRADOS

### Se [pending] Permanecer:

| Dado | Razão Provável | Ação |
|---|---|---|
| Preço de Aquisição (PATL11) | Export XP incompleto | Buscar em corretora ou marcar [não disponível] |
| Segmento (4 FIIs) | CVM não informou | Verificar com administrador ou marcar [não confirmado] |
| Dividendo recente | Informe não publicado | Usar última cotação disponível + alertar |
| PL ou Cotas | Fundo encerrado? | Verificar status (ativo/cancelado) em CVM |

### Documentação de [pending]:
- Sempre justificar por que não foi encontrado
- Citar data da tentativa de coleta
- Indicar próxima ação (busca em alternativa, contato com gestor, etc.)

---

## 9. FERRAMENTAS E ATALHOS

### Links Diretos (Adicionar ao Favoritos)

| Recurso | URL | Descrição |
|---|---|---|
| CVM — Fundos | https://www.gov.br/cvm/pt-br/assuntos/regulados/consultas-por-participante/fundos-de-investimento | Busca de fundos registrados |
| CVM — Dados Abertos | https://dados.cvm.gov.br/dataset/ | Portal de datasets abertos |
| BCB — Selic Histórica | https://www.bcb.gov.br/controleinflacao/historicotaxasjuros | Histórico de taxa básica |
| BCB — Copom | https://www.bcb.gov.br/controleinflacao/comunicadoscopom | Comunicados das reuniões |
| BCB — Focus | https://www.bcb.gov.br/publicacoes/focus | Expectativas de mercado |

### Busca Rápida (Scripts)

Para automatizar coleta futura (Python/curl):
```bash
# Exemplo: Buscar dados de FII via API CVM (se disponível)
# curl -s "https://dados.cvm.gov.br/api/3/action/package_search?q=CPTR11" | jq '.'
```

---

## 10. CHECKLIST FINAL

- [ ] **6 FIIs Consultados:** CPTR11, HGLG11, MFII11, HCTR11, CTXT11, PATL11
- [ ] **Regulamentos Baixados:** 6/6
- [ ] **Informativos 6 Meses:** 6 × 6 = 36 documentos (ou máximo disponível)
- [ ] **Dados Estruturais Compilados:** Nome, Segmento, CNPJ, PL, Cotas, VPA
- [ ] **Dividendos 6 Meses:** Tabelas preenchidas por FII
- [ ] **PATL11 — Preço de Aquisição:** Encontrado ou marcado [não disponível]
- [ ] **Contexto Macroeconômico:** Selic, Copom (3 últimas), Focus compilado
- [ ] **Documento de Saída:** `pesquisa-fiis-2026-09-26-completo.md` pronto para revisão

---

## 11. PRÓXIMAS AÇÕES APÓS COLETA

1. **Análise de Liquidez:** Comparar yield anualizado com Selic + spread para avaliar atratividade
2. **Revisão de Concentração:** Confirmar se 6 FIIs oferecem diversificação de segmentos
3. **Decisão de Alocação:** Manter, aumentar, reduzir ou rebalancear posições
4. **Registro de Decisão:** Se decisão tomada, documentar em `decisions/` conforme `knowledge/schema-decisoes.md`

---

**Guia Preparado:** 2026-09-26  
**Agente:** Claude Haiku 4.5  
**Referência:** AGENTS.md (regras de execução 1-5)

---

*Este guia é executável sem intermediários; CVM e BCB são fontes públicas de acesso irrestrito.*
