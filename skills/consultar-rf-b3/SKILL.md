---
name: consultar-rf-b3
description: Consulta dados de títulos de renda fixa no banco de dados B3 (ISIN, vencimento, taxa, etc) a partir de emissor, tipo e vencimento.
---

# Consulta RF - Base B3

Pesquisa no banco de dados da B3 (arquivo NUMERACA.TXT v1.0) para encontrar títulos de renda fixa com dados estruturados.

## Entrada

Forneça pelo menos um filtro:
- **ISIN** (opcional): Código ISIN (ex: BRAGBKC00JG1) - busca prioritária, ignora outros filtros
- **Emissor**: nome ou código (ex: AGIBANK, AGBK, BANCO XP, BMG)
- **Tipo**: CDB, CRA, CRI, DEB, LCA, LCD, LF, FND
- **Vencimento**: data ou período (ex: 2027-07-21, 2027-07, 2027, 2027-Q3)

## Saída

Para cada título encontrado:
- **ISIN**: Código internacional (12 caracteres: BR + 4 emissor + 3 tipo + 2 garantia + 1 controle)
- **Descrição**: Nome conforme registrado na B3
- **Emissor**: Código (ex: AGBK) 
- **Vencimento**: Data exata (YYYY-MM-DD)
- **Taxa**: Taxa nominal em % (quando aplicável)
- **Percentual**: Percentual do indexador (ex: 100%, 120% CDI)
- **Remuneração**: PRE (pré-fixado), DI1/CDI, IPCA, ZERO (zero-cupom), etc
- **Moeda**: BRL (padrão)
- **Ativo**: Sim/Não conforme status na B3

## Campos do NUMERACA.TXT (conforme Leiame.pdf)

| Campo | Descrição |
|-------|-----------|
| DATA DA GERAÇÃO | Data de referência do arquivo |
| AÇÃO | N=Novo, A=Alterado, D=Inativado |
| ISIN | Código internacional |
| CÓDIGO EMISSOR | 4 caracteres (ex: AGBK=AGIBANK) |
| DESCRIÇÃO | Nome do título (até 120 chars) |
| EMISSÃO/VENCIMENTO | Ano e data |
| TAXA JUROS | Valor em % (pré-fixado) ou indexador |
| PERCENTUAL INDEXADOR | % CDI, % IPCA, etc |
| TIPO DE JUROS | Z=Zero-cupom, F=Fixo, V=Variável |
| INDEXADOR | PRE, DI1, IPCA, IGPD, TR, SELIC, DOL, etc |

## Como usar

```bash
# Buscar por ISIN (busca prioritária e rápida)
python scripts/consultar_rf_b3.py --isin BRAGBKC00JG1
# Retorna 1 registro com dados completos

# Buscar todos os CDBs do AGIBANK com vencimento em julho/2027
python scripts/consultar_rf_b3.py --emissor AGIBANK --tipo CDB --vencimento 2027-07
# Retorna 41 registros

# Buscar por tipo apenas
python scripts/consultar_rf_b3.py --tipo CRA --vencimento 2027

# Saída em CSV
python scripts/consultar_rf_b3.py --tipo CDB --formato csv

# Múltiplos ISINs (requer múltiplas execuções)
for isin in BRAGBKC00JG1 BRAGBKC010E5; do
  python scripts/consultar_rf_b3.py --isin $isin
done
```

## Observações

- **Base**: `/inbox/B3/isinp/NUMERACA.TXT` + `EMISSOR.TXT` (381.794 títulos, 69.404 emissores)
- **Atualização**: Frequência definida pela B3 (arquivo incluído tem data 2026-09-25)
- **Status**: Por padrão inclui inativos (D) pois maioria do histórico está inativa
- **Precisão de vencimento**: Todos os CDBs do arquivo estão vencidos ou em 2027 (base histórica)
- **Correlação com posições**: Use ISIN para atualizar `state/positions/renda_fixa.csv`
- **Mapeamento**: Código AGBK↔AGIBANK, XPCE↔XP (via MAPEO_EMISSOR)
