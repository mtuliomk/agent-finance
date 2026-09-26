---
name: consultar-rf-b3
description: Consulta dados de títulos de renda fixa no banco de dados B3 (ISIN, vencimento, taxa, etc) a partir de emissor, tipo e vencimento.
---

# Consulta RF - Base B3

Pesquisa em tempo real no banco de dados da B3 (arquivo NUMERACA.TXT) para encontrar títulos de renda fixa com dados estruturados.

## Entrada

Forneça os filtros desejados (ao menos um):
- **Emissor**: nome ou código (ex: AGIBANK, AGBK, BANCO XP, BMG)
- **Tipo**: CDB, CRA, CRI, DEB, LCA, LCD, LF, FND
- **Vencimento**: data ou período (ex: 2027-07-21, julho/2027, 2027-Q3)

## Saída

Para cada título encontrado:
- **ISIN**: Código internacional
- **Descrição**: Nome completo do título
- **Tipo**: CDB/CRA/CRI/etc
- **Emissor**: Código e nome
- **Vencimento**: Data exacta (AAAA-MM-DD)
- **Taxa**: Taxa de remuneração (quando informada)
- **Tipo de remuneração**: Pré-fixado, CDI, IPCA, DI1, etc
- **Ativo**: Sim/Não na B3
- **Moeda**: BRL/USD/etc

## Como usar

```bash
# Buscar todos os CDBs do AGIBANK com vencimento em 2027-07
python scripts/consultar_rf_b3.py --emissor AGIBANK --tipo CDB --vencimento 2027-07

# Buscar por ISIN ou código específico
python scripts/consultar_rf_b3.py --emissor "BANCO XP" --tipo CDB

# Filtro amplo (apenas tipo)
python scripts/consultar_rf_b3.py --tipo CRA
```

## Observações

- Base de dados: `/inbox/B3/isinp/NUMERACA.TXT` (atualizada regularmente)
- Correlação com posições: use o ISIN para atualizar `state/positions/renda_fixa.csv`
- Dados históricos: arquivo cobre ativos e inativos
- Precisão: nomes de emissores podem estar abreviados; confirme com documento de custódia
