# Dados candidatos a MCP — desenho sob demanda

Não há MCP instalado; estas são fronteiras propostas, não integrações disponíveis. Até existir conector autorizado, continue com web, CLI local e exports manuais. Ser dinâmico não basta para justificar MCP: priorize consulta recorrente/estruturada que reduza extração manual.

| Dados | Origem/candidato | Contrato mínimo e limite |
| --- | --- | --- |
| Posições e transações XP/BTG | Conector de custódia autorizado, somente leitura | Custodiante, lote, moeda, data-base, cobertura/completude, origem, versão; conciliar com snapshots, não somar recortes. Não enviar carteira a pesquisa pública. |
| Selic, CDI, inflação, câmbio e expectativas | Séries oficiais BCB/IBGE e fonte primária do índice | Código da série, período, unidade, data de publicação/revisão; distinguir meta, realizado e expectativa. |
| Documentos, resultados e eventos por emissor/fundo | B3/CVM e divulgação do emissor | Identidade jurídica, período, publicação/reapresentação e link/documento primário; extrair somente campos solicitados. |
| ISIN, características e emissores/conglomerados | Cadastro B3 e registros oficiais pertinentes | Versão/layout, data, código de emissão e identidade inequívoca; ausência de resultado não prova inexistência. Base local via CLI continua fallback. |
| Cotações, preços/taxas e ofertas | B3/Tesouro/corretora autorizada | Horário, moeda, unidade, lado/condições, acesso e validade; preço indicativo separado de execução. |
| FGC, alíquotas, faixas, isenções e regras cambiais | FGC, Receita e legislação oficial | Dispositivo, vigência, produto/enquadramento e data de consulta. MCP recupera evidência; interpretação permanece no método. |
| Notícias e ratings | Publicador/agência identificados | Data do evento/publicação, versão e instrumento; confirmar afirmações materiais na fonte primária pertinente. |

Retorno deve permitir filtro por ativo/período/campos, expor lacunas/erros e guardar proveniência. Não substituir desconhecido por zero, nem tratar cache expirado como atual. Consulta pública não acessa estado pessoal; uma futura custódia autenticada exige autorização própria e reconciliação.

Persistem localmente: métodos de risco/fluxos/valuation/tributação, contratos de dados, política de fontes e decisões históricas. Snapshots/cache datados ficam em JSON/CSV; o conector não deve reescrever o raciocínio passado. Não implementar nem instalar MCP nesta otimização.
