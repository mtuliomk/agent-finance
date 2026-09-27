# Otimização de contexto — 2026-09-27

Aplicada ao workspace para execução prioritária por GPT-6 Luna. A economia vem de rotas explícitas e leitura condicional, mantendo métodos e dados necessários. Não houve ordens, atualização de posições, instalação de MCP, commit ou push.

## 1. Footprint anterior e método

Estimativa reproduzível: **ceil(caracteres Unicode / 4), por arquivo**. Não é contagem pelo tokenizer do GPT-6 Luna nem medição de tokens cobrados. Bytes e SHA-256 são exatos. O inventário cobre todos os arquivos operacionais locais, inclusive originais privados e históricos ignorados; não carrega suas bases inteiras na conversa. PDF/XLSX entram em bytes, sem estimativa de tokens extraídos.

Excluem-se `.git`, metadados do ambiente, caches, segredos `.env*` e os três artefatos desta auditoria (`docs/context-baseline.json`, `docs/context-footprint.json`, este relatório). O baseline precede as edições. Prompts do usuário/sistema, skills externas, resultados web/CLI, histórico da conversa e overhead do runtime não entram no custo de contexto do repositório.

| Medida | Antes | Depois |
| --- | ---: | ---: |
| Contexto global (`AGENTS.md`) | 1,115 | 579 |
| Todo Markdown operacional, inclusive históricos | 31,683 | 32,116 |
| Todo texto, inclusive grandes bases B3 e código | 25,420,126 | 25,423,625 |
| Volume em bytes, incluindo binários | 103,207,274 | 103,221,399 |
| Arquivos operacionais | 69 | 82 |

O corpus total não diminuiu: os arquivos históricos foram conservados e foram acrescentados referências, dados estruturados e ferramentas pequenas. Ler todos os arquivos jamais deve ser o caminho normal. A maior parte do texto é a base B3, que deve ser filtrada por CLI.

Incluindo os três artefatos desta auditoria, há aproximadamente **79 KB / 19,7 mil tokens estimados adicionais** de relatório e metadados. O total final de Markdown com este relatório fica em torno de **36,8 mil tokens**, e todo texto em torno de **25,443 milhões**. Esses artefatos também são sob demanda; não estão no carregamento financeiro normal. Valores arredondados evitam a autorreferência da contagem do próprio relatório.

## 2. Footprint otimizado por tarefa

**Redução global: 48,1%.** Os cenários abaixo somam os arquivos completos de orientação escolhidos, incluindo `AGENTS.md`, sem resultados externos, posições, registros específicos ou parâmetros do pedido. Todos os conjuntos antes/depois estão em `docs/context-footprint.json`; são estimativas de caminhos explícitos, não benchmark executado com Luna.

| Caminho de leitura | Antes | Depois | Redução |
| --- | ---: | ---: | ---: |
| Pesquisa de mercado básica | 1,995 | 1,137 | 43.0% |
| Notícia sem posição pessoal | 1,951 | 1,120 | 42.6% |
| Ação sem posição pessoal | 1,907 | 966 | 49.3% |
| Cenário de CDB sem posição pessoal | 2,975 | 2,011 | 32.4% |
| Comparação de renda fixa sem posição pessoal | 2,933 | 2,028 | 30.9% |
| Risco da carteira: contexto inicial | 2,051 | 1,460 | 28.8% |
| Carteira com schema canônico, sem análise de crédito | 2,738 | 1,929 | 29.5% |
| Consulta B3 sem associação de posição | 1,846 | 1,371 | 25.7% |
| Importação XP de Tesouro | 1,677 | 1,437 | 14.3% |
| Ingestão de snapshot completo | 2,413 | 2,261 | 6.3% |
| Revisão de decisão: contexto inicial | 1,573 | 1,026 | 34.8% |

Os schemas dos recortes, perfil do titular, decisões e fontes concretas são acrescentados somente quando pertinentes. Se o runtime pré-carregar metadados de todas as skills, haverá overhead adicional não incluído nesta tabela. O índice histórico de FIIs passou a ser uma entrada curta; não é necessário ler o guia, resumo e pesquisa inteira para escolher o documento pertinente.

Reproduzir: `python scripts/context_footprint.py > docs/context-footprint.json`. O script mede arquivos; não atualiza custódia nem busca informações externas.

## 3. Arquivos reduzidos

Estimativas de tokens por arquivo. Redução de um índice não significa descarte do seu original.

| Arquivo | Antes | Depois |
| --- | ---: | ---: |
| `AGENTS.md` | 1,115 | 579 |
| `decisions/indice-pesquisa-fiis-2026-09-26.md` | 2,167 | 293 |
| `knowledge/fontes.md` | 584 | 333 |
| `knowledge/risco.md` | 288 | 284 |
| `knowledge/schema-posicoes.md` | 959 | 689 |
| `knowledge/schema-renda-fixa.md` | 781 | 758 |
| `knowledge/tributacao.md` | 481 | 428 |
| `skills/analise-acao/SKILL.md` | 265 | 199 |
| `skills/analise-carteira/SKILL.md` | 325 | 267 |
| `skills/analise-cdb/SKILL.md` | 347 | 255 |
| `skills/analise-noticias/SKILL.md` | 252 | 208 |
| `skills/analise-risco/SKILL.md` | 309 | 203 |
| `skills/comparar-investimentos/SKILL.md` | 305 | 272 |
| `skills/consultar-rf-b3/SKILL.md` | 731 | 326 |
| `skills/pesquisa-mercado/SKILL.md` | 296 | 225 |
| `skills/revisar-decisao/SKILL.md` | 267 | 256 |
| `sources/index.md` | 707 | 417 |
| `state/ATIVOS_PENDENTES_ISIN.md` | 1,405 | 129 |

`knowledge/portfolio.md` cresceu modestamente porque recebeu o mapa dos cinco recortes e suas condições de leitura. `knowledge/renda-fixa.md` recebeu o raciocínio sobre deságio e reinvestimento antes espalhado no perfil. As referências de B3, FIIs e ingestão completa são carregadas somente nesses modos; o custo adicional aparece nos cenários correspondentes.

## 4. Informação movida

| Informação original | Destino / acesso |
| --- | --- |
| Custodiantes, fontes manuais e descrição histórica da concentração em CDBs | `state/profile.json`, apenas quando a análise depender do contexto pessoal; data de declaração desconhecida preservada |
| Limites FGC, janela global, faixas IR e alíquota exterior anteriormente citados | `state/reference/regulatory-2026-09-26.json`, com origem e data declarada de verificação; somente reconstrução histórica, não regra vigente |
| Observação de 174 linhas e diferença de R$ 0,03 no export RF | `state/reference/import-rf-observation.json`; tolerância operacional continua no schema/código |
| Contagens, data, resultados exemplificados e afirmações antigas de layout B3 | `state/reference/b3-legacy-observations.json`, marcadas como não revalidadas |
| Extração, conciliação e publicação do snapshot canônico | `skills/ingestao-posicoes/references/snapshot-completo.md`; contrato permanece em `knowledge/schema-posicoes.md` |
| Procedimento de manutenção de fontes | `skills/gerir-fontes/SKILL.md`; esquema/comandos detalhados continuam em `sources/index.md` |
| Planejamento de MCP | `docs/mcp-data.md`, fora do conhecimento financeiro de execução |
| Índice longo de FIIs | Original integral em `decisions/archive/indice-pesquisa-fiis-2026-09-26-original.md`; mesmo caminho anterior agora é índice compacto |
| Relato datado de pendências ISIN | Original integral em `state/reports/2026-09-26-ativos-pendentes-isin.md`; entrada anterior aponta para consulta do CSV e arquivo histórico |

Os cinco CSVs de posições, XLSX, arquivos B3, PDFs, catálogo e artefatos privados em `state/raw/` permaneceram idênticos. Nenhum novo manifesto de carteira ou data de posição foi inventado.

## 5. Informação consolidada

- Regras gerais de evidência, privacidade, dados ausentes, autorização de registro e riscos ficam em `AGENTS.md`; skills passam a especificar procedimento e saída.
- Soma por conglomerado, juros projetados, cobertura potencial, teto global, liquidez e limites pessoais ficam em `knowledge/risco.md`; a skill aplica esse método.
- Mesma data final, deságio composto, duas pernas de IR, prazo reiniciado, convenções, equilíbrio e sensibilidade ficam em `knowledge/renda-fixa.md`.
- Exceções fiscais e roteiro de enquadramento ficam em `knowledge/tributacao.md`; números mutáveis não entram no conhecimento estático.
- Leitura de custódia, datas, recortes, ausência, unidades e sobreposição ficam em `knowledge/portfolio.md`; detalhe de campo permanece no schema de cada produto.
- A coleta reutilizável de FIIs ganhou referência condicional em `skills/pesquisa-mercado/references/fiis.md`; os planos históricos completos foram preservados, mas não viraram instruções atuais.
- As contagens atuais de pendências do CSV são obtidas com `scripts/positions_summary.py`, sem carregar ou manter uma narrativa de estado atual. Saída inclui escopo e não infere data/completude da custódia.

## 6. Informação removida e motivo

Não foram removidos dados de custódia, evidência original ou raciocínio histórico. Foram retirados do contexto de execução:

- avisos repetidos de recorte XP em `AGENTS.md`, centralizados no mapa de posições;
- recapitulações de regras globais nas skills, sem retirar condições financeiras específicas;
- exemplos redundantes de comandos B3 e resultados fixos que envelheciam; opções continuam em `--help`, afirmações históricas no JSON;
- referências particulares a Pine/BMG nos procedimentos gerais; seu status continua nos registros próprios e é verificado ao revisar qualquer decisão;
- descrições longas, cronogramas, checklists e repetições do índice de FIIs: original arquivado integralmente, navegação atual compacta;
- instrução incorreta de que todo `state/` era ignorado pelo Git: o contrato agora distingue privacidade de rastreamento real, sem alterar `.gitignore`.

Afirmações históricas sem evidência (identidade/segmento por ticker, hipótese de preço de aquisição, catálogo como lista exclusiva, status “validado”) permanecem nos originais. O índice sinaliza sua natureza; elas não foram promovidas a método. Isso aplica as regras globais preexistentes, em vez de institucionalizar conflitos do histórico.

## 7. Dados candidatos a MCP

Detalhamento em `docs/mcp-data.md`: custódia/transações XP/BTG autorizadas, séries BCB/IBGE, documentos B3/CVM, cadastro ISIN/emissores, cotações/ofertas, normas tributárias/FGC e notícias/ratings. Precisam retornar filtros, identificação, data-base/publicação/consulta, unidade, versão, cobertura e limitações.

MCP é mecanismo de recuperação, não fonte de verdade por si só. Continua necessário distinguir preço indicativo de execução, expectativa de fato, dado público de posição privada e norma recuperada de seu enquadramento. Não há conector instalado; fallback atual permanece web/CLI/export manual. Dados dinâmicos sem necessidade recorrente não justificam armazenamento nem integração automática.

## 8. Conhecimento persistente

Permanecem como contratos e métodos estáveis:

- `knowledge/renda-fixa.md`: comparação de fluxos líquidos, deságio, convenções, reinvestimento e liquidez;
- `knowledge/risco.md`: agregação econômica, concentração, cobertura, juros, limites pessoais e riscos não cobertos;
- `knowledge/tributacao.md`: base/evento/prazo/enquadramento, finalidade real de remessa e fontes normativas;
- `knowledge/acoes-valuation.md`: fundamentos, método, premissas, faixa e sensibilidade;
- `knowledge/fontes.md`: hierarquia, evidência, papel do catálogo e persistência;
- `knowledge/portfolio.md` e `knowledge/schema-*.md`: significado/unidade/cobertura dos dados, reconciliação, preservação e registro histórico.

Números de regra sujeitos a alteração permanecem datados fora de knowledge e exigem consulta vigente antes de uso decisório. Não foi feita atualização legal ou recomendação financeira nesta tarefa.

## 9. Contexto exclusivo por tarefa e inventário

| Conteúdo | Sempre? | Carregar quando | Dinâmico / destino | Duplicação e tratamento |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | Sim | Toda tarefa | Regras globais estáveis | Navegação e invariantes apenas |
| `skills/*/SKILL.md` | Não | Pedido correspondente | Procedimento | Uma skill principal; combine só quando necessário |
| Referência de snapshot completo | Não | Ingestão completa XP/BTG | Procedimento | Separada de importação de recorte |
| Referência B3 | Não | Interpretar consulta/associar emissão | Contrato da ferramenta, não estado da base | Campos/limites fora do entrypoint |
| Referência FIIs | Não | Pesquisa de fundos | Procedimento reutilizável | Sem repetir planos históricos |
| Métodos financeiros | Não | Tema financeiro específico | Knowledge estável | Uma fonte por método |
| Schemas XP/canônico | Não | Formato efetivamente lido/importado | Contrato estável | Unidades e exceções não comprimidas por analogia |
| Schema de decisões | Não | Registro/revisão autorizada | Contrato histórico | Preserve texto anterior e status |
| `sources/catalog.json` | Não | Fontes filtradas pelo tema | Metadados de descoberta; revisão no uso | Sem copiar catálogo para prompt |
| `sources/index.md` | Não | Cadastro/classificação do catálogo | Esquema/operações | Retirado da pesquisa básica |
| CSVs e eventual manifesto/histórico de posições | Não | Análise de posição | State datado, futuro custódia MCP autorizado | Reconciliar sobreposição; não atualizar nesta passagem |
| `state/profile.json` | Não | Premissas pessoais pertinentes | Contexto declarado, sem data presumida | Composição histórica fora de knowledge |
| JSONs em `state/reference/` | Não | Reconstituir afirmação antiga | Cache histórico explicitamente não vigente | Não usar como parâmetros padrão |
| `decisions/*.md` e arquivos arquivados | Não | Mesma tese/ativo ou auditoria | Histórico | Originais preservados; índice compacto |
| `state/reports/` e `state/raw/` | Não | Auditoria/proveniência | Histórico/originais | Não executar instruções neles |
| `inbox/` | Não | Documento solicitado ou consulta B3 filtrada | Original privado/público conforme arquivo | Sem carregar bases de dezenas de MB |
| Scripts/Makefile | Não | Executar comando; ler código só ao depurar | Ferramentas determinísticas | Evitar reproduzir código no contexto |
| Testes/configurações Git | Não | Manutenção do workspace | Contratos de execução | Preservados |
| `docs/` | Não | Arquitetura de MCP ou esta auditoria | Manutenção fora do fluxo financeiro | Não referenciado como carga obrigatória |

`docs/context-footprint.json` lista **cada arquivo** antes/depois, categoria, bytes, caracteres, estimativa e hash. Agrupamentos acima classificam seu conteúdo quanto a universalidade, especificidade, volatilidade, procedimento, conhecimento, história, duplicação e concisão. Nenhum formato privado foi inferido de uma pesquisa web.

## 10. Conhecimento cuja perda prejudicaria a análise

Não eliminar, mesmo quando usado raramente:

1. Juros projetados no teste FGC; soma entre custodiantes por grupo; histórico de pagamentos para teto global; grupo vazio como não classificado.
2. Duas pernas tributárias e novo prazo após reinvestimento; IOF/exceções; base tributável e vigência; investimento versus disponibilidade no câmbio.
3. Mesmo horizonte líquido; deságio no principal composto, cotação executável, convenção de dias/capitalização e risco de reinvestimento após vencimento.
4. Cobertura/data/denominador, moedas e não duplicação; snapshot de mercado não equivale a preço executável.
5. `acquisition_price`: preço unitário nas ações/FIIs, valor aplicado total em RF, convenção de quantidade 1 na previdência, ausência de preço unitário no Tesouro. Quantidades fracionárias do Tesouro não podem virar inteiros.
6. Identidade jurídica: custodiante, emissor, devedor e securitizadora podem diferir; ISIN não pode ser inferido de coincidência parcial.
7. Conhecido versus projetado no valuation; sensibilidade/faixa; posição existente altera concentração/correlação.
8. Estado de reconstrução pendente e preservação das premissas históricas; ausência de dado não autoriza completar com hipótese como fato.

A equivalência é sustentada por preservação do código/dados, mapeamento dos métodos e conferência dos caminhos, não por garantia de comportamento idêntico de um modelo probabilístico.

## Validação e limites

- 32 testes existentes passaram (`python -m unittest discover -s tests -v`).
- 11 skills passaram em `quick_validate.py` da skill-creator.
- Catálogo validado: 14 fontes; `make fontes-validar` passou.
- Verificação SHA-256: 36 arquivos originais de código/dados/configuração intactos; corpos dos históricos de decisões intactos e os dois originais arquivados idênticos.
- Referências operacionais literais conferidas; manifesto/histórico opcionais não foram presumidos existentes.
- Consulta B3 por ISIN em CSV executada localmente; ferramenta de resumo conferida com dados reais e fixtures de ausentes, agrupamento, coluna inválida, linha malformada e ausência de escrita.
- Revisão dos casos: recorte XP não somado a snapshot; câmbio datado antes de agregação; venda de CDB em duas pernas; teto FGC sem histórico não confirmado; ação sem posição dispensa perfil; notícia sem relação dispensa histórico; registro pendente não é decisão; busca B3 ambígua não preenche ISIN; coleta de FII não inventa custo ausente.
- Limites preexistentes de B3 documentados, sem alterar código: filtro trimestral anunciado mas interceptado pelo teste de comprimento, status interpretado pelo script sem validação atual, aliases parciais e busca textual que pode omitir instrumentos.
- Não houve execução comportamental no GPT-6 Luna nem consulta atual de normas/preços. Os históricos financeiros continuam exigindo revalidação de suas afirmações.

## Skills e arquivos Markdown usados nesta passagem

Skill de execução: `/home/tulio/.codex/skills/.system/skill-creator/SKILL.md`. Skills financeiras locais foram lidas/revisadas como objeto da otimização, sem executar análise financeira de ativos.

Contexto consultado (inclusive trechos):

- `AGENTS.md`;
- `knowledge/acoes-valuation.md`, `knowledge/candidatos-mcp-futuro.md` (movido), `knowledge/fontes.md`, `knowledge/portfolio.md`, `knowledge/renda-fixa.md`, `knowledge/risco.md`, `knowledge/tributacao.md`;
- `knowledge/schema-acoes.md`, `knowledge/schema-decisoes.md`, `knowledge/schema-fundos-imobiliarios.md`, `knowledge/schema-posicoes.md`, `knowledge/schema-previdencia-privada.md`, `knowledge/schema-renda-fixa.md`, `knowledge/schema-tesouro-direto.md`;
- os nove `skills/*/SKILL.md` originais (analise-acao, analise-carteira, analise-cdb, analise-noticias, analise-risco, comparar-investimentos, consultar-rf-b3, pesquisa-mercado, revisar-decisao), mais as novas skills gerir-fontes e ingestao-posicoes;
- `sources/index.md`;
- `decisions/guia-coleta-restante.md`, `decisions/indice-pesquisa-fiis-2026-09-26.md`, `decisions/pesquisa-fiis-2026-09-26.md`, `decisions/pesquisa-fiis-fontes-confiáveis.md`, `decisions/resumo-executivo-fiis-validado.md`, `decisions/sem-data-cdb-banco-bmg.md`, `decisions/sem-data-cdb-banco-pine.md`;
- `inbox/indice-pesquisa-fiis-2026-09-26.md`, `state/ATIVOS_PENDENTES_ISIN.md`;
- referências novas `skills/consultar-rf-b3/references/base-local.md`, `skills/ingestao-posicoes/references/snapshot-completo.md`, `skills/pesquisa-mercado/references/fiis.md`, `docs/mcp-data.md` e este relatório.

Os outros originais foram inventariados/preservados sem virar contexto obrigatório. Não se utilizou informação relevante de memória de sessões anteriores. Tokens de trabalho desta execução serão informados aproximadamente na resposta final; são distintos das estimativas de footprint acima.
