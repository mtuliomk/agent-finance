# Contrato de posições v1

`state/positions/{XP|BTG}.csv` contém o **último snapshot completo aceito por custodiante**; `manifest.json` registra origem e versões. `history/` guarda snapshots anteriores. Dados de `state/` são privados; não presuma que estejam ignorados pelo Git. Sem arquivo real, não existe carteira atual na workspace.

## CSV canônico

UTF-8, cabeçalho obrigatório abaixo, uma linha por lote/posição distinguível, datas `YYYY-MM-DD`, números decimais com ponto, sem separador de milhar; valores monetários na moeda da linha. Campo desconhecido fica vazio, nunca zero presumido. `custodian`, `position_id`, `asset_class`, `instrument_name`, `currency`, `valuation_date`, `source_locator` são obrigatórios. `market_value` e `cost_basis` podem faltar, mas análises de exposição/retorno ficam limitadas.

```csv
custodian,position_id,asset_class,instrument_name,instrument_id,issuer,conglomerate,currency,quantity,cost_basis,market_value,valuation_date,acquisition_date,maturity_date,rate_type,rate_value,rate_basis,liquidity_terms,source_locator,notes
```

- `custodian`: `XP` ou `BTG`; é local de custódia, não emissor.
- `position_id`: chave estável do lote dentro do custodiante, preferindo identificador do export; sem ID, atribuir manualmente e manter mapa estável. Não derive de quantidade/valor.
- `asset_class`: `CDB`, `LCA`, `CRI`, `ACAO`, `FII` ou `OUTRO`. Produto e cobertura FGC exigem confirmação própria.
- `instrument_id`: ISIN, ticker ou código do produto quando disponível. `issuer` e `conglomerate` identificam risco econômico; ausência fica vazia e deve ser sinalizada.
- `quantity`, `cost_basis`, `market_value`: número não negativo; `cost_basis` é custo total ainda aplicado no lote, `market_value` é valor reportado na data, não preço executável de venda.
- `valuation_date`: data da fotografia do documento, igual à data informada na importação. `acquisition_date` e `maturity_date` só quando constam da origem.
- `rate_type`: `PREFIXADO`, `PCT_CDI`, `CDI_MAIS`, `IPCA_MAIS`, `OUTRO` ou vazio. `rate_value` é número em pontos percentuais; `rate_basis` registra convenção da taxa, por exemplo `aa_252_du` ou `aa_365_dc`. Sem esses três elementos, não simule retorno contratual.
- `liquidity_terms`: texto fiel do contrato/export, sem converter "vencimento" em "liquidez".
- `source_locator`: aba+linha do XLSX ou página+item do PDF; permite conferência. `notes`: ambiguidade de extração, unidade, premissa ou classificação.

## Proveniência

`manifest.json` registra data da foto, importação, hash SHA-256/caminho privado da origem, versão/caminho do snapshot, contagem e avisos. Não armazena cotações externas ou transações. Procedimento de extração, conciliação e publicação: `skills/ingestao-posicoes/SKILL.md`.
