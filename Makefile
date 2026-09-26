.DEFAULT_GOAL := help
.PHONY: help fontes-listar fontes-adicionar fontes-atualizar fontes-validar posicoes-previa posicoes-publicar xp-import-position xp-import-previdencia xp-import-fii xp-import-acoes xp-import-rf

PYTHON ?= python3
export TOPIC TYPE ALL ID FIELD VALUE NAME URL TOPICS CONTENT_TYPES PUBLISHER_TYPE ROLE PURPOSE LIMITATIONS STATUS VERIFIED_ON
export CSV SOURCE CUSTODIAN AS_OF CONFIRMED_COMPLETE ACCEPT_REMOVALS FILE

help: ## Lista todos os alvos e os parâmetros principais
	@awk 'BEGIN { FS = ":.*## " } /^[a-z][a-z0-9-]*:.*## / { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

fontes-listar: ## Lista fontes (TOPIC=credito TYPE=norma ALL=yes opcionais)
	@set --; \
	if [ -n "$$TOPIC" ]; then set -- "$$@" --topic "$$TOPIC"; fi; \
	if [ -n "$$TYPE" ]; then set -- "$$@" --type "$$TYPE"; fi; \
	if [ "$$ALL" = "yes" ]; then set -- "$$@" --all; fi; \
	$(PYTHON) scripts/sources.py list "$$@"

fontes-adicionar: ## Cadastra fonte (guiado ou com variáveis do catálogo)
	@set --; \
	if [ -n "$$ID" ]; then set -- "$$@" --id "$$ID"; fi; \
	if [ -n "$$NAME" ]; then set -- "$$@" --name "$$NAME"; fi; \
	if [ -n "$$URL" ]; then set -- "$$@" --url "$$URL"; fi; \
	if [ -n "$$TOPICS" ]; then set -- "$$@" --topics "$$TOPICS"; fi; \
	if [ -n "$$CONTENT_TYPES" ]; then set -- "$$@" --content-types "$$CONTENT_TYPES"; fi; \
	if [ -n "$$PUBLISHER_TYPE" ]; then set -- "$$@" --publisher-type "$$PUBLISHER_TYPE"; fi; \
	if [ -n "$$ROLE" ]; then set -- "$$@" --role "$$ROLE"; fi; \
	if [ -n "$$PURPOSE" ]; then set -- "$$@" --purpose "$$PURPOSE"; fi; \
	if [ -n "$$LIMITATIONS" ]; then set -- "$$@" --limitations "$$LIMITATIONS"; fi; \
	if [ -n "$$STATUS" ]; then set -- "$$@" --status "$$STATUS"; fi; \
	if [ -n "$$VERIFIED_ON" ]; then set -- "$$@" --verified-on "$$VERIFIED_ON"; fi; \
	$(PYTHON) scripts/sources.py add "$$@"

fontes-atualizar: ## Atualiza um campo (ID=... FIELD=topics VALUE=credito,produtos)
	@test -n "$$ID" && test -n "$$FIELD" || { echo 'Informe ID e FIELD' >&2; exit 2; }
	@case "$$FIELD" in name|url|topics|content-types|publisher-type|role|purpose|limitations|verified-on|status) ;; *) echo 'FIELD inválido' >&2; exit 2;; esac
	@$(PYTHON) scripts/sources.py update --id "$$ID" "--$$FIELD" "$$VALUE"

fontes-validar: ## Valida esquema, URLs, datas e duplicatas do catálogo
	@$(PYTHON) scripts/sources.py validate

posicoes-previa: ## Valida sem publicar (CSV=... SOURCE=... CUSTODIAN=XP AS_OF=AAAA-MM-DD)
	@test -n "$$CSV" && test -n "$$SOURCE" && test -n "$$CUSTODIAN" && test -n "$$AS_OF" || { echo 'Informe CSV, SOURCE, CUSTODIAN e AS_OF' >&2; exit 2; }
	@$(PYTHON) scripts/ingest_positions.py --csv "$$CSV" --source "$$SOURCE" --custodian "$$CUSTODIAN" --as-of "$$AS_OF"

posicoes-publicar: ## Publica após conciliação (mesmos dados + CONFIRMED_COMPLETE=yes; ACCEPT_REMOVALS=yes opcional)
	@test -n "$$CSV" && test -n "$$SOURCE" && test -n "$$CUSTODIAN" && test -n "$$AS_OF" || { echo 'Informe CSV, SOURCE, CUSTODIAN e AS_OF' >&2; exit 2; }
	@test "$$CONFIRMED_COMPLETE" = "yes" || { echo 'Confirme conciliação e completude com CONFIRMED_COMPLETE=yes' >&2; exit 2; }
	@set -- --csv "$$CSV" --source "$$SOURCE" --custodian "$$CUSTODIAN" --as-of "$$AS_OF" --commit --confirmed-complete; \
	if [ "$$ACCEPT_REMOVALS" = "yes" ]; then set -- "$$@" --accept-removals; fi; \
	$(PYTHON) scripts/ingest_positions.py "$$@"

xp-import-position: ## Importa Tesouro Direto da XP (FILE=nome.xlsx em inbox/XP)
	@test -n "$$FILE" || { echo 'Informe FILE=nome.xlsx de inbox/XP' >&2; exit 2; }
	@$(PYTHON) scripts/xp_import_position.py "$$FILE"

xp-import-previdencia: ## Importa Previdência Privada da XP (FILE=nome.xlsx em inbox/XP)
	@test -n "$$FILE" || { echo 'Informe FILE=nome.xlsx de inbox/XP' >&2; exit 2; }
	@$(PYTHON) scripts/xp_import_previdencia.py "$$FILE"

xp-import-fii: ## Importa Fundos Imobiliários da XP (FILE=nome.xlsx em inbox/XP)
	@test -n "$$FILE" || { echo 'Informe FILE=nome.xlsx de inbox/XP' >&2; exit 2; }
	@$(PYTHON) scripts/xp_import_fii.py "$$FILE"

xp-import-acoes: ## Importa Ações da XP (FILE=nome.xlsx em inbox/XP)
	@test -n "$$FILE" || { echo 'Informe FILE=nome.xlsx de inbox/XP' >&2; exit 2; }
	@$(PYTHON) scripts/xp_import_acoes.py "$$FILE"

xp-import-rf: ## Importa Renda Fixa da XP (FILE=nome.xlsx em inbox/XP)
	@test -n "$$FILE" || { echo 'Informe FILE=nome.xlsx de inbox/XP' >&2; exit 2; }
	@$(PYTHON) scripts/xp_import_rf.py "$$FILE"
