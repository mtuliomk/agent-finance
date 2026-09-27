---
name: ingestao-posicoes
description: Importa XLSX/PDF XP ou BTG como snapshot completo ou recorte XP, com conciliação e proveniência.
---

# Ingestão de posições

Escolha o modo pela cobertura do documento e pedido. Não carregue referências dos demais modos.

**Snapshot completo XP/BTG:** leia `knowledge/portfolio.md` e `skills/ingestao-posicoes/references/snapshot-completo.md`.

**Recorte XP:** original em `inbox/XP/`; `FILE` é só o nome do XLSX. Leia o schema da seção e execute o comando correspondente:

| Seção | Comando (`make ... FILE=nome.xlsx`) | Schema em `knowledge/` |
| --- | --- | --- |
| Tesouro Direto | `xp-import-position` | `schema-tesouro-direto.md` |
| Previdência Privada | `xp-import-previdencia` | `schema-previdencia-privada.md` |
| FIIs | `xp-import-fii` | `schema-fundos-imobiliarios.md` |
| Ações | `xp-import-acoes` | `schema-acoes.md` |
| Renda Fixa | `xp-import-rf` | `schema-renda-fixa.md` |

Scripts conciliam a seção e preservam IDs existentes; migrações/preenchimento RF constam do schema. Recorte incremental não atualiza toda a carteira. Informe arquivo, conciliação, preservações e lacunas; não presuma completude/data atual de custódia.
