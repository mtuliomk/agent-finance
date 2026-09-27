# Leitura da carteira

Posições canônicas: `state/positions/{XP|BTG}.csv` + `state/positions/manifest.json` (último snapshot completo aceito por custodiante); contrato em `knowledge/schema-posicoes.md`. Confira existência, data, custódias e cobertura. Ausência não significa posição zero. Histórico em `state/positions/history/`; originais em `state/raw/` ou `inbox/`.

Os cinco CSVs abaixo são **recortes XP incrementais**, sem atualização automática de IDs existentes; não comprovam posição atual nem carteira completa. Não os some entre si ou ao snapshot sem conciliar sobreposição e datas. Leia apenas o schema do recorte utilizado:

| CSV em `state/positions/` | Schema em `knowledge/` |
| --- | --- |
| `tesouro_direto.csv` | `schema-tesouro-direto.md` |
| `previdencia_privada.csv` | `schema-previdencia-privada.md` |
| `fundos_imobiliarios.csv` | `schema-fundos-imobiliarios.md` |
| `acoes.csv` | `schema-acoes.md` |
| `renda_fixa.csv` | `schema-renda-fixa.md` |

`acquisition_price` tem unidades diferentes por recorte: confirme o schema antes de calcular. Valores ausentes ou `[pending]` não são zero; custo não é cotação atual nem preço executável. Não agregue moedas sem câmbio datado nem snapshots de datas distintas sem declarar defasagem.

Contexto declarado pelo titular: `state/profile.json`, somente se a análise depender dele; não substitui snapshots. Limites pessoais não informados não devem ser inventados. Métodos condicionais: `knowledge/risco.md` (crédito/FGC), `knowledge/renda-fixa.md` (fluxos/reinvestimento), `knowledge/tributacao.md` (tributos).
