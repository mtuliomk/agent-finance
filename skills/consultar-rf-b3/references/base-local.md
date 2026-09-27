# Contrato e limites da consulta local

`scripts/consultar_rf_b3.py` lê apenas `NUMERACA.TXT`; `EMISSOR.TXT` e `Leiame.pdf`, na mesma pasta `inbox/B3/isinp/`, são referências para conferir nomes/layout. Não execute `scripts/update_rf_fields.py` para consultar: ele grava posições. `scripts/parse_b3_isin.py` contém busca exploratória específica, não valida identidade de qualquer emissão.

Filtros: ISIN prioritário; emissor por texto/código e aliases locais; tipos aceitos CDB, CRA, CRI, DEB, LCA, LCD, LF, FND. Vencimento por ano, mês ou dia. Para trimestre, use os três meses: embora o help anuncie `AAAA-Qn`, a implementação trata sete caracteres antes do trimestre. ISIN também ignora `--apenas-ativos`.

Saída CSV: `data_ref`, `ativo`, `isin`, `codigo_emissor`, `ticker_bmf`, `descricao`, ano/data de início e vencimento, `taxa`, `percentual`, `moeda`, `tipo_remuneracao`. Taxa nominal e percentual do indexador são campos diferentes; não os confunda com cotação executável ou taxa do lote pessoal. Confira unidades/códigos no `Leiame.pdf` antes de cálculo; PRE, DI1/CDI, IPCA e ZERO são rótulos de remuneração, não intercambiáveis.

Limitações verificáveis no código: `ativo` testa se o campo bruto é `A`; não valida situação atual. A documentação antiga descrevia esse campo como ação N/A/D (novo/alterado/inativado): confirme significado no layout antes de interpretar. Busca por tipo usa texto, com pré-filtro CERTIFICADO/DEBENTURE/LETRA FINANCEIRA, podendo omitir instrumentos. Datas ausentes podem atravessar filtro de vencimento. Emissor usa correspondência parcial e só dois aliases fixos (AGBK/AGIBANK, XPCE/XP); confirme nome jurídico/grupo separadamente.

Contagens, datas e resultados de exemplo antigos foram preservados em `state/reference/b3-legacy-observations.json`, sem validade como estado atual. Consulte só para reconstrução histórica.
