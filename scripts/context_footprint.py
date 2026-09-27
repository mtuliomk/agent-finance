#!/usr/bin/env python3
"""Estimate workspace context with ceil(Unicode characters / 4), not a model tokenizer."""

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".agents", ".codex", "__pycache__", ".pytest_cache", ".venv"}
AUDIT_FILES = {
    "docs/context-baseline.json", "docs/context-footprint.json",
    "docs/context-optimization.md",
}
SCENARIOS = {
    "pesquisa_mercado_basica": (
        ["skills/pesquisa-mercado/SKILL.md", "knowledge/fontes.md"],
        ["skills/pesquisa-mercado/SKILL.md", "knowledge/fontes.md"],
    ),
    "noticia_sem_posicao": (
        ["skills/analise-noticias/SKILL.md", "knowledge/fontes.md"],
        ["skills/analise-noticias/SKILL.md", "knowledge/fontes.md"],
    ),
    "acao_sem_posicao": (
        ["skills/analise-acao/SKILL.md", "knowledge/acoes-valuation.md", "knowledge/portfolio.md"],
        ["skills/analise-acao/SKILL.md", "knowledge/acoes-valuation.md"],
    ),
    "cdb_cenario_sem_posicao": (
        ["skills/analise-cdb/SKILL.md", "knowledge/portfolio.md", "knowledge/renda-fixa.md", "knowledge/tributacao.md", "knowledge/risco.md"],
        ["skills/analise-cdb/SKILL.md", "knowledge/renda-fixa.md", "knowledge/tributacao.md", "knowledge/risco.md"],
    ),
    "comparacao_renda_fixa_sem_posicao": (
        ["skills/comparar-investimentos/SKILL.md", "knowledge/portfolio.md", "knowledge/renda-fixa.md", "knowledge/tributacao.md", "knowledge/risco.md"],
        ["skills/comparar-investimentos/SKILL.md", "knowledge/renda-fixa.md", "knowledge/tributacao.md", "knowledge/risco.md"],
    ),
    "risco_carteira_base": (
        ["skills/analise-risco/SKILL.md", "knowledge/portfolio.md", "knowledge/risco.md"],
        ["skills/analise-risco/SKILL.md", "knowledge/portfolio.md", "knowledge/risco.md"],
    ),
    "carteira_com_schema_canonico_sem_credito": (
        ["skills/analise-carteira/SKILL.md", "knowledge/portfolio.md", "knowledge/schema-posicoes.md"],
        ["skills/analise-carteira/SKILL.md", "knowledge/portfolio.md", "knowledge/schema-posicoes.md"],
    ),
    "consulta_b3_sem_posicao": (
        ["skills/consultar-rf-b3/SKILL.md"],
        ["skills/consultar-rf-b3/SKILL.md", "skills/consultar-rf-b3/references/base-local.md"],
    ),
    "importacao_tesouro": (
        ["knowledge/schema-tesouro-direto.md"],
        ["skills/ingestao-posicoes/SKILL.md", "knowledge/schema-tesouro-direto.md"],
    ),
    "ingestao_snapshot_completo": (
        ["knowledge/portfolio.md", "knowledge/schema-posicoes.md"],
        ["skills/ingestao-posicoes/SKILL.md", "skills/ingestao-posicoes/references/snapshot-completo.md", "knowledge/portfolio.md", "knowledge/schema-posicoes.md"],
    ),
    "revisao_decisao_base": (
        ["skills/revisar-decisao/SKILL.md", "knowledge/schema-decisoes.md"],
        ["skills/revisar-decisao/SKILL.md", "knowledge/schema-decisoes.md"],
    ),
}


def category(name):
    if name == "AGENTS.md":
        return "global"
    if name.startswith(("knowledge/", "skills/", "sources/")):
        return "on_demand_guidance_and_catalog"
    if name.startswith("decisions/"):
        return "history"
    if name.startswith(("state/", "inbox/")):
        return "data_and_originals"
    if name.startswith("docs/"):
        return "optional_maintenance_docs"
    return "code_tests_and_config"


def inventory():
    result = {}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        name = relative.as_posix()
        if not path.is_file() or SKIP_PARTS.intersection(relative.parts):
            continue
        if name in AUDIT_FILES or path.name.startswith(".env"):
            continue
        data = path.read_bytes()
        try:
            characters = len(data.decode("utf-8"))
        except UnicodeDecodeError:
            characters = None
        result[name] = {
            "bytes": len(data), "characters": characters,
            "estimated_tokens": math.ceil(characters / 4) if characters is not None else None,
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    return result


def totals(files):
    groups = {}
    for name, record in files.items():
        group = groups.setdefault(category(name), {"files": 0, "bytes": 0, "estimated_text_tokens": 0})
        group["files"] += 1
        group["bytes"] += record["bytes"]
        group["estimated_text_tokens"] += record["estimated_tokens"] or 0
    return {
        "groups": groups,
        "files": len(files),
        "bytes": sum(row["bytes"] for row in files.values()),
        "estimated_text_tokens": sum(row["estimated_tokens"] or 0 for row in files.values()),
        "estimated_markdown_tokens": sum(row["estimated_tokens"] or 0 for name, row in files.items() if name.endswith(".md")),
    }


def scenarios(before, after):
    result = {}
    for name, (old_paths, new_paths) in SCENARIOS.items():
        old_paths = ["AGENTS.md", *old_paths]
        new_paths = ["AGENTS.md", *new_paths]
        old = sum(before[path]["estimated_tokens"] for path in old_paths)
        new = sum(after[path]["estimated_tokens"] for path in new_paths)
        result[name] = {
            "before_files": old_paths, "after_files": new_paths,
            "before_tokens": old, "after_tokens": new,
            "reduction_percent": round((old - new) * 100 / old, 1),
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=ROOT / "docs/context-baseline.json")
    args = parser.parse_args()
    before = json.loads(args.baseline.read_text(encoding="utf-8"))
    after = inventory()
    changes = {}
    for name in sorted(before.keys() | after.keys()):
        old, new = before.get(name), after.get(name)
        changes[name] = {
            "category": category(name),
            "before": old,
            "after": new,
            "change": "added" if old is None else "removed_or_moved" if new is None else "unchanged" if old["sha256"] == new["sha256"] else "modified",
        }
    print(json.dumps({
        "method": "sum per file ceil(Unicode characters / 4); estimate, not GPT-6 Luna tokenization; binary tokens unestimated",
        "excluded": sorted(AUDIT_FILES | SKIP_PARTS) + [".env*"],
        "before": totals(before), "after": totals(after), "files": changes,
        "task_guidance_scenarios": scenarios(before, after),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
