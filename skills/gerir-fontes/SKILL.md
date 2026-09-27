---
name: gerir-fontes
description: Cadastra, reclassifica ou retira fontes recorrentes do catálogo local; não é necessário para apenas pesquisar.
---

# Manter fontes

Leia `knowledge/fontes.md` para inclusão/persistência e `sources/index.md` para esquema e comandos.

1. Confira link, papel e limites. Use ID curto e estável e tags pela pergunta/material publicado, não afinidade ampla.
2. Cadastre com `make fontes-adicionar`; corrija campos com `make fontes-atualizar ID=... FIELD=... VALUE=...`. Retirada preserva ID e registra motivo/sucessora em `limitations`; não reutilize IDs.
3. Rode `make fontes-validar`. Revise no uso; não há atualização automática.

Informe alterações e validação. Não confunda cadastro do canal com validação de todo seu conteúdo.
