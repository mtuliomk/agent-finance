# Catálogo de fontes web

`sources/catalog.json` guarda **um registro por ponto de entrada estável**. Este arquivo explica como classificar e cadastrar; a seleção por tema é feita com `make fontes-listar TOPIC=credito`. Rode `make` para listar todos os atalhos disponíveis.

## Classificação

Cada registro tem ID estável, nome, URL, `topics` (para qual pergunta serve), `content_types` (que dado oferece), `publisher_type`, `role` para o uso descrito, finalidade, limite/contraprova, `verified_on` e `status`. Uma fonte pode ter vários temas e tipos. Valores aceitos pelo validador:

| Campo | Valores |
| --- | --- |
| `topics` | `macroeconomia`, `acoes`, `fundos`, `credito`, `tributacao`, `produtos`, `noticias` |
| `content_types` | `indicador`, `expectativa`, `documento`, `cadastro`, `norma`, `orientacao`, `oferta`, `noticia` |
| `publisher_type` | `orgao-publico`, `entidade-setorial`, `emissor`, `corretora`, `imprensa`, `outro` |
| `role` | `primaria`, `secundaria`, `descoberta` — relativa à finalidade registrada |
| `status` | `ativa`, `candidata`, `retirada` |

`candidata` permite guardar site ainda não conferido; não o trate como fonte validada. Uma fonte `ativa` exige data em `verified_on`, que confirma **somente o link e o papel descrito**, não a atualidade de cada publicação. `retirada` preserva o ID histórico.

Classifique `topics` pela **pergunta que a fonte responde** e `content_types` pelo **material que ela publica**. Use `primaria` quando a própria entidade publica o dado ou documento citado, `secundaria` quando o reproduz ou analisa, e `descoberta` quando serve para localizar algo a confirmar. Uma fonte pode receber mais de uma tag se tiver uso recorrente em cada tema; evite tags apenas por afinidade ampla.

## Operações

- `make fontes-listar TOPIC=macroeconomia`: mostra fontes ativas e seus limites; use `TYPE=documento` para filtrar tipo e `ALL=yes` para incluir candidatas e retiradas.
- `make fontes-adicionar`: cadastro guiado, grava um registro no JSON após validar. Para uso não interativo, passe as variáveis `ID`, `NAME`, `URL`, `TOPICS`, `CONTENT_TYPES`, `PUBLISHER_TYPE`, `ROLE`, `PURPOSE`, `LIMITATIONS` e, se aplicável, `STATUS` e `VERIFIED_ON`.
- `make fontes-atualizar ID=ID FIELD=topics VALUE=credito,produtos`: altera um campo por vez. Para retirar, altere `status` para `retirada` e registre motivo/sucessora em `limitations`.
- `make fontes-validar`: verifica esquema, duplicatas, classificação, URL e datas após edição manual.

Consulte só os resultados do tema relevante. Na análise, cite o documento/dado concreto aberto, com data e período, não o registro do catálogo. Critérios para incluir, revisar e armazenar informação estão em `knowledge/fontes.md`. Ofertas e notícias efêmeras ficam como evidência da análise; só o **site ou canal recorrente** entra aqui.
