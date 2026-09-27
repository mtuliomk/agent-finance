---
name: consultar-rf-b3
description: Localiza candidatos a títulos de renda fixa na base B3 local por ISIN, emissor, tipo ou vencimento.
---

# Consulta RF B3

Execute `python scripts/consultar_rf_b3.py --help` para opções. Use ISIN exato quando disponível (ignora outros filtros); senão combine emissor, tipo e vencimento. Restrinja a consulta antes de abrir resultados extensos; prefira `--formato csv`, que inclui `data_ref`.

A base é `inbox/B3/isinp/NUMERACA.TXT`, sem atualização automática. Não leia o arquivo inteiro no contexto. Padrão inclui inativos; opções e campos/limitações estão em `skills/consultar-rf-b3/references/base-local.md`, obrigatório antes de interpretar resultados ou associar posição.

Retorne candidatos, data da base, ISIN, descrição, código de emissor, vencimento, taxa, percentual, remuneração, moeda e status conforme fonte. Ausência na busca não prova inexistência do título.

Para conciliar com carteira, leia `knowledge/portfolio.md` e `knowledge/schema-renda-fixa.md`. Pendências atuais do CSV: `python scripts/positions_summary.py --file state/positions/renda_fixa.csv --missing isin --group investment_type`. Só associe ISIN com identificação inequívoca de emissão, emissor e condições; semelhança de nome/data não basta. Preserve ambiguidades como pendentes.
