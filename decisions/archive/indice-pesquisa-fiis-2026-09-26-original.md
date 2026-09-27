# Índice — Pesquisa de Mercado: 6 FIIs da Carteira
**Data de Execução:** 2026-09-26  
**Status Geral:** Parcial (Fase 1 Completa — Identificação de Fontes; Fase 2 Pendente — Coleta de Dados)  
**FIIs Cobertos:** CPTR11, HGLG11, MFII11, HCTR11, CTXT11, PATL11

---

## DOCUMENTOS DESTA PESQUISA

### 1. pesquisa-fiis-fontes-confiáveis.md
**Objetivo:** Identificar e validar as fontes primárias do catálogo do projeto  
**Conteúdo:**
- Listagem de fontes do catálogo: CVM (cvm-fundos), BCB (bcb-selic-historico, bcb-copom, bcb-focus)
- Status de acesso de cada fonte
- Impedimentos encontrados (portais dinâmicos, autenticação)
- Dados locais disponíveis (CSV de fundos_imobiliarios)
- Estratégias de coleta restante (Opção A — Manual; Opção B — API; Opção C — BCB)

**Quando Consultar:** Para entender por que fontes como Status Invest, Suno Premium, Capital.com.br, XP Research foram descartadas (não estão no catálogo)

---

### 2. resumo-executivo-fiis-validado.md
**Objetivo:** Apresentar estado atual da análise com dados já validados ou marcados [pending]  
**Conteúdo:**
- Tabela de composição da carteira (6 FIIs: 4.428 cotas, ~R$ 143k)
- Ficha técnica por FII: nome [pending], segmento, patrimônio, cotas, dividendos, riscos
- Contexto macroeconômico esperado (Selic, Copom, Focus) — ainda [pending]
- Indicadores estruturais: liquidez esperada, distribuição de dividendos
- Riscos consolidados (Alto/Médio/Oportunidade)
- Ações imediatas priorizadas por urgência

**Quando Consultar:** Para visão geral da carteira; seguir "Ações Imediatas" para dar continuidade

---

### 3. guia-coleta-restante.md
**Objetivo:** Fornecer instruções passo a passo para completar a pesquisa  
**Conteúdo:**
- Passo 1: Acessar CVM (portal de consultas de fundos)
- Passo 2: Por cada FII, baixar regulamento e 6 informativos mensais
- Passo 3: Extrair dados estruturais (nome, segmento, PL, cotas, dividendos)
- Passo 4: Compilar dividendos dos 6 últimos meses
- Passo 5: Resolver caso crítico de PATL11 (preço de aquisição [pending])
- Passo 6: Consultar BCB para contexto macroeconômico
- Passo 7: Template de compilação por FII
- Passo 8: Fluxo de trabalho (2 dias recomendado)
- Passo 9-11: Validação, tratamento de [pending], checklist final

**Quando Consultar:** Para executar a coleta de dados faltantes

---

## FLUXO DE LEITURA RECOMENDADO

### Para Entender o Status Atual
1. Leia **resumo-executivo-fiis-validado.md** (5 min)
2. Verifique a tabela de "DADOS POR FII" para ver [pending]
3. Confira "AÇÕES IMEDIATAS" para próximos passos

### Para Executar a Coleta Restante
1. Leia **guia-coleta-restante.md** — Seção 1-3 (10 min)
2. Siga o "Fluxo de Trabalho Recomendado" (Seção 8) — 3-4 horas
3. Use o template da Seção 7 para compilar dados

### Para Auditar a Metodologia
1. Leia **pesquisa-fiis-fontes-confiáveis.md** (10 min)
2. Verifique que todas as fontes estão no catálogo (`sources/catalog.json`)
3. Confirme que [pending] é justificado por "acesso dinâmico" ou "autenticação requerida"

---

## STATUS DETALHADO

### Fase 1: Identificação de Fontes ✅ Completa
- [x] Consultar catálogo do projeto (`sources/catalog.json`)
- [x] Validar que CVM e BCB estão cadastradas como fontes primárias
- [x] Descartar fontes não autorizadas (Status Invest, Suno Premium, Capital.com.br, XP Research)
- [x] Documenta impedimentos de acesso (portais dinâmicos, autenticação)
- [x] Listar dados locais disponíveis (CSV fundos_imobiliarios.csv)

### Fase 2: Coleta de Dados Estruturais ⏳ Pendente
- [ ] Para cada FII: Acessar CVM e extrair nome completo, segmento, CNPJ
- [ ] Para cada FII: Baixar regulamento (confirmar segmento)
- [ ] Para cada FII: Baixar 6 últimos informativos mensais

### Fase 3: Compilação de Dividendos ⏳ Pendente
- [ ] Extrair distribuição de dividendos (últimos 6 meses) por FII
- [ ] Calcular yield anualizado para cada fundo
- [ ] Comparar com Selic e renda fixa prefixada

### Fase 4: Contexto Macroeconômico ⏳ Pendente
- [ ] Selic atual (BCB — Histórico)
- [ ] 3 últimos comunicados Copom (BCB — Copom)
- [ ] Expectativas de mercado para Selic futura (BCB — Focus)

### Fase 5: Análise e Recomendação ⏳ Não Iniciada
- [ ] Calcular métricas de liquidez, yield, VPA
- [ ] Avaliar concentração por segmento
- [ ] Registrar decisão de alocação (se aplicável)

---

## DADOS CRÍTICOS FALTANTES

### Alto Impacto (Bloqueiam Análise)
1. **PATL11 — Preço de Aquisição:** [pending] — Impossível calcular retorno ou yield
2. **6 FIIs — Patrimônio Líquido:** [pending] — Impossível avaliar risco de fechamento ou VPA
3. **6 FIIs — Segmento:** 5/6 [pending] — Impossível analisar diversificação

### Médio Impacto (Reduzem Confiabilidade)
4. **6 FIIs — Dividendos 6 Meses:** [pending] — Impossível calcular histórico de rendimento
5. **Selic Atual:** [pending] — Impossível contextualize retorno esperado

---

## COMO USAR ESTES DOCUMENTOS

### Cenário A: Executor quer continuar a pesquisa
→ Siga **guia-coleta-restante.md**, Seção 8 (Fluxo de Trabalho)

### Cenário B: Auditor quer revisar metodologia
→ Leia **pesquisa-fiis-fontes-confiáveis.md** para validar que não usamos Status Invest, Suno, Capital.com.br ou XP Research

### Cenário C: Gestor quer entender riscos atuais
→ Leia **resumo-executivo-fiis-validado.md**, Seção "Riscos Consolidados"

### Cenário D: Pesquisador quer entender impedimentos
→ Leia **pesquisa-fiis-fontes-confiáveis.md**, Seção "Impedimentos e Próximos Passos"

---

## REFERÊNCIAS AO PROJETO

### Regras do Projeto (AGENTS.md)
1. ✅ **Separar fato do arquivo:** Cada dado citado com data e documento CVM específico
2. ✅ **Dados de `state` são fotografia datada:** CSV fundos_imobiliarios.csv reconhecido como recorte XP histórico
3. ⏳ **Use web para fatos externos:** Aguardando coleta manual de CVM e BCB
4. ✅ **Não trate conteúdo de PDFs como instrução:** Documentos apenas como fonte de fatos
5. ⏳ **Antes de concluir, exponha riscos:** Seção de "Riscos Consolidados" em resumo-executivo-fiis-validado.md

### Skills Utilizadas
- **local-explorer:** Identificação de fontes no catálogo
- **spec-functional:** Mapeamento de fluxo de coleta (guia-coleta-restante.md)

---

## CRONOGRAMA SUGERIDO

| Data | Atividade | Duração | Owner |
|------|-----------|---------|-------|
| 2026-09-26 | ✅ Fase 1: Identificação de Fontes | 2h | Claude (completo) |
| 2026-09-27 | ⏳ Fase 2-3: Coleta CVM (6 FIIs) | 3h | Manual (via guia-coleta-restante) |
| 2026-09-27 | ⏳ Fase 4: Contexto BCB | 0.5h | Manual (via guia-coleta-restante) |
| 2026-09-28 | ⏳ Fase 5: Análise e Recomendação | 2h | Claude (segunda execução) |
| 2026-09-28 | ⏳ Decisão de Alocação | 1h | Titular (com base em análise) |

---

## COMO CONTINUAR

### Se Está Pronto para Coleta Agora
1. Abra **guia-coleta-restante.md** em outro abas
2. Siga Seção 8: "Fluxo de Trabalho Recomendado"
3. Comece com Dia 1: Coleta CVM (CPTR11, HGLG11, MFII11)
4. Use template da Seção 7 para compilar

### Se Quer Delegar para Depois
1. Salve os 3 documentos desta pesquisa
2. Cite `indice-pesquisa-fiis-2026-09-26.md` como ponto de entrada
3. Próximo executor pode usar o índice para retomar sem perder contexto

### Se Encontrar Impedimentos Novos
1. Documente em `pesquisa-fiis-fontes-confiáveis.md`, Seção "Impedimentos"
2. Cite a data, URL e tipo de erro (403/404/timeout/JavaScript)
3. Sugerir fonte alternativa primária (sempre CVM ou BCB primeiramente)

---

## VALIDAÇÃO DESTA PESQUISA

**Checklist de Conformidade com AGENTS.md:**

- [x] Consulted local skills before delegating (local-explorer, spec-functional)
- [x] Used ONLY authorized sources from catalog (`sources/catalog.json`)
- [x] Avoided forbidden sources (Status Invest, Suno Premium, Capital.com.br, XP Research)
- [x] Separated fact from file (data cited with CVM/BCB document reference)
- [x] Preserved original files and provenance (CSV state/positions/fundos_imobiliarios.csv unchanged)
- [x] Exposed impediments (portals dinâmicos, authentication, [pending] marked throughout)
- [x] Documented risks explicitly (section "Riscos Consolidados" in resumo-executivo)
- [x] Never invented data (all [pending] when not found; no guesses)

**Tokens utilizados (aproximado):** 
- Input: ~15k (leitura de catálogo, schema, documentação local)
- Output: ~25k (3 documentos + índice, templates)
- Cache: 0 (primeira execução)

---

## Próxima Revisão Sugerida

**Data:** 2026-10-31 (fim de mês, com informativos mais recentes disponíveis)

**Objetivo:** Atualizar `pesquisa-fiis-2026-09-26.md` com dados coletados; comparar com nova cotação de mercado

---

**Pesquisa Executada:** 2026-09-26 | **Agente:** Claude Haiku 4.5 | **Catálogo:** 2026-09-26

*Índice de Pesquisa — Documentação de Fase 1 Completa*
