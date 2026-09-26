# Contexto pessoal validado

- Carteira concentrada em CDBs prefixados e de crédito de bancos pequenos e médios; alocações menores em LCA, CRI, ações e FIIs. Não inferir pesos atuais sem snapshot.
- Custódia primária: XP Investimentos. Secundária: BTG Pactual.
- State atual é manual: `PosicaoDetalhada.xlsx` e PDF de posição da XP; eventualmente arquivos BTG. O formato canônico está em `schema-posicoes.md`.
- Desconto de saída antecipada composto ao longo do horizonte de reinvestimento pode consumir a vantagem de taxa nominal maior; em horizontes curtos, resgate tende a ser pouco atrativo. Testar com números do caso.
- Venda antecipada pode antecipar IR e reinvestimento inicia novo prazo para tabela regressiva; incluir ambas as pernas e datas.
- Risco de reinvestimento é real e pode superar o ganho matemático de esperar, sobretudo com Selic em queda. Explicitar cenários, sem predizer a taxa futura como fato.
- FGC por emissor/conglomerado é restrição estrutural de construção de carteira. Ver `risco.md`.
- Pitch de assessor exige verificação factual independente.
- Lei 14.754/2023 e distinção entre remessa para investimento e disponibilidade são pontos de atenção tributária. Aplicação e alíquotas vigentes exigem consulta atual; ver `tributacao.md`.

Este arquivo contém premissas fornecidas pelo titular, não posições ou cotações atuais.
