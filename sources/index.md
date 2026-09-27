# Esquema do catálogo de fontes

`sources/catalog.json`: um registro por canal estável. Para pesquisar, basta `make fontes-listar TOPIC=TEMA`; manutenção: `skills/gerir-fontes/SKILL.md`. Política: `knowledge/fontes.md`.

Cada registro: `id`, `name`, `url`, `topics`, `content_types`, `publisher_type`, `role`, `purpose`, `limitations`, `verified_on`, `status`. Valores aceitos:

| Campo | Valores |
| --- | --- |
| `topics` | `macroeconomia`, `acoes`, `fundos`, `credito`, `tributacao`, `produtos`, `noticias` |
| `content_types` | `indicador`, `expectativa`, `documento`, `cadastro`, `norma`, `orientacao`, `oferta`, `noticia` |
| `publisher_type` | `orgao-publico`, `entidade-setorial`, `emissor`, `corretora`, `imprensa`, `outro` |
| `role` | `primaria` (publica o dado), `secundaria` (reproduz/analisa), `descoberta` (localiza para confirmar); relativo à finalidade |
| `status` | `ativa`, `candidata` (não conferida), `retirada` (ID histórico) |

Temas classificam perguntas; tipos classificam materiais. Multitag só para uso recorrente em cada tema. `ativa` exige `verified_on`, que confirma link/papel, não atualidade de cada publicação.

## Comandos

- `make fontes-listar TOPIC=credito TYPE=documento`: filtros opcionais; `ALL=yes` inclui candidatas/retiradas.
- `make fontes-adicionar`: guiado; não interativo usa `ID`, `NAME`, `URL`, `TOPICS`, `CONTENT_TYPES`, `PUBLISHER_TYPE`, `ROLE`, `PURPOSE`, `LIMITATIONS`, opcionalmente `STATUS` e `VERIFIED_ON`.
- `make fontes-atualizar ID=... FIELD=topics VALUE=credito,produtos`: um campo por vez; campos permitidos em `make`.
- `make fontes-validar`: esquema, URLs, datas, classificação e IDs/URLs duplicados.
