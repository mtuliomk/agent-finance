# Ingestão de snapshot completo

1. Leia `knowledge/schema-posicoes.md`. Preserve o original em `inbox/`. XLSX: inspecione abas/cabeçalhos; LibreOffice pode exportar a aba sem alterar a origem. PDF: `pdftotext -layout` auxilia extração, mas confira cada linha visualmente. Não há mapeamento universal XP/BTG.
2. Mapeie para CSV canônico em `inbox/`. Execute `make posicoes-previa CSV=... SOURCE=... CUSTODIAN=XP AS_OF=AAAA-MM-DD` (ou BTG).
3. Concilie contagens/totais por classe e moeda com a origem; confira remoções e grandes alterações contra snapshot anterior. PDF pode corroborar XLSX, nunca substituir valores silenciosamente: divergências ficam em `notes` ou bloqueiam publicação até resolução.
4. Só após confirmar cobertura de **toda** a custódia na data, execute `make posicoes-publicar` com as mesmas variáveis e `CONFIRMED_COMPLETE=yes`; `ACCEPT_REMOVALS=yes` apenas para saídas conferidas. Recorte não passa nesse fluxo como carteira completa.

O script arquiva origem com SHA-256, guarda histórico e atualiza apenas aquele custodiante/manifesto. Informe modo, data/cobertura, arquivo gerado, conciliação, preservações e lacunas. Não infira transações ou variação patrimonial de dois snapshots.
