#!/usr/bin/env python3
"""List, add, update and validate curated web source entry points."""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "sources" / "catalog.json"
TOPICS = {"macroeconomia", "acoes", "fundos", "credito", "tributacao", "produtos", "noticias"}
CONTENT_TYPES = {"indicador", "expectativa", "documento", "cadastro", "norma", "orientacao", "oferta", "noticia"}
PUBLISHERS = {"orgao-publico", "entidade-setorial", "emissor", "corretora", "imprensa", "outro"}
ROLES = {"primaria", "secundaria", "descoberta"}
STATUSES = {"ativa", "candidata", "retirada"}
FIELDS = {"id", "name", "url", "topics", "content_types", "publisher_type", "role", "purpose", "limitations", "verified_on", "status"}


def parse_tags(value):
    return [part.strip() for part in value.split(",") if part.strip()]


def validate_entry(entry, number):
    label = f"fonte {number}"
    if not isinstance(entry, dict) or set(entry) != FIELDS:
        raise ValueError(f"{label}: campos diferentes do esquema em sources/index.md")
    for field in ("id", "name", "url", "publisher_type", "role", "purpose", "limitations", "verified_on", "status"):
        if not isinstance(entry[field], str):
            raise ValueError(f"{label}: {field} deve ser texto")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["id"]):
        raise ValueError(f"{label}: id deve usar letras minúsculas, números e hífens")
    for field in ("name", "purpose", "limitations"):
        if not entry[field].strip():
            raise ValueError(f"{label}: {field} não pode ser vazio")
    parsed = urlsplit(entry["url"])
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f"{label}: URL HTTPS pública inválida ou com credenciais")
    for field, allowed in (("topics", TOPICS), ("content_types", CONTENT_TYPES)):
        tags = entry[field]
        if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or tag not in allowed for tag in tags) or len(tags) != len(set(tags)):
            raise ValueError(f"{label}: {field} inválido; consulte sources/index.md")
    for field, allowed in (("publisher_type", PUBLISHERS), ("role", ROLES), ("status", STATUSES)):
        if entry[field] not in allowed:
            raise ValueError(f"{label}: {field} inválido; consulte sources/index.md")
    if entry["verified_on"]:
        try:
            verified = date.fromisoformat(entry["verified_on"])
        except ValueError as exc:
            raise ValueError(f"{label}: verified_on inválido") from exc
        if verified.isoformat() != entry["verified_on"] or verified > date.today():
            raise ValueError(f"{label}: verified_on deve ser data YYYY-MM-DD já ocorrida")
    elif entry["status"] == "ativa":
        raise ValueError(f"{label}: fonte ativa exige verified_on")


def load_catalog(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"schema_version", "sources"} or data["schema_version"] != 1 or not isinstance(data["sources"], list):
        raise ValueError("catálogo inválido ou versão não suportada")
    ids = set()
    urls = set()
    for number, entry in enumerate(data["sources"], 1):
        validate_entry(entry, number)
        if entry["id"] in ids or entry["url"] in urls:
            raise ValueError(f"fonte {number}: id ou URL duplicado")
        ids.add(entry["id"])
        urls.add(entry["url"])
    return data


def save_catalog(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def ask(label, value, default=None):
    if value is not None:
        return value
    if not sys.stdin.isatty():
        raise ValueError(f"add requer --{label.replace('_', '-')} em modo não interativo")
    suffix = f" [{default}]" if default else ""
    answer = input(f"{label}{suffix}: ").strip()
    return answer or default or ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="Valida o catálogo local sem acessar a web")
    listing = commands.add_parser("list", help="Mostra fontes por classificação")
    listing.add_argument("--topic", choices=sorted(TOPICS))
    listing.add_argument("--type", dest="content_type", choices=sorted(CONTENT_TYPES))
    listing.add_argument("--all", action="store_true", help="Inclui candidatas e retiradas")
    adding = commands.add_parser("add", help="Cadastra uma fonte; sem argumentos, guia pelo terminal")
    for field in ("id", "name", "url", "topics", "content_types", "publisher_type", "role", "purpose", "limitations", "verified_on", "status"):
        adding.add_argument("--" + field.replace("_", "-"))
    updating = commands.add_parser("update", help="Altera classificação ou dados de uma fonte existente")
    updating.add_argument("--id", required=True)
    for field in ("name", "url", "topics", "content_types", "publisher_type", "role", "purpose", "limitations", "verified_on", "status"):
        updating.add_argument("--" + field.replace("_", "-"))
    args = parser.parse_args()
    data = load_catalog(args.catalog)
    if args.command == "validate":
        print(f"Catálogo válido: {len(data['sources'])} fontes")
    elif args.command == "list":
        matches = [entry for entry in data["sources"] if (args.all or entry["status"] == "ativa") and (not args.topic or args.topic in entry["topics"]) and (not args.content_type or args.content_type in entry["content_types"])]
        for entry in sorted(matches, key=lambda item: item["id"]):
            print(f"{entry['id']} [{entry['status']}; {entry['role']}] {entry['name']}")
            print(f"  Temas: {', '.join(entry['topics'])}; tipos: {', '.join(entry['content_types'])}")
            print(f"  {entry['url']}")
            print(f"  Uso: {entry['purpose']} Limite: {entry['limitations']}")
        print(f"{len(matches)} fonte(s)")
    elif args.command == "update":
        entry = next((item for item in data["sources"] if item["id"] == args.id), None)
        if entry is None:
            raise ValueError(f"id não encontrado: {args.id}")
        changes = {field: getattr(args, field) for field in FIELDS - {"id"} if getattr(args, field) is not None}
        if not changes:
            raise ValueError("update exige ao menos um campo para alterar")
        for field in ("topics", "content_types"):
            if field in changes:
                changes[field] = parse_tags(changes[field])
        revised = {**entry, **changes}
        validate_entry(revised, args.id)
        if any(old["id"] != args.id and old["url"] == revised["url"] for old in data["sources"]):
            raise ValueError("URL já cadastrada em outra fonte")
        data["sources"][data["sources"].index(entry)] = revised
        save_catalog(args.catalog, data)
        print(f"Fonte atualizada: {args.id}")
    else:
        status = ask("status", args.status, "candidata")
        verified_on = args.verified_on if args.verified_on is not None else (ask("verified_on", None, "") if sys.stdin.isatty() else "")
        entry = {
            "id": ask("id", args.id),
            "name": ask("name", args.name),
            "url": ask("url", args.url),
            "topics": parse_tags(ask("topics", args.topics)),
            "content_types": parse_tags(ask("content_types", args.content_types)),
            "publisher_type": ask("publisher_type", args.publisher_type),
            "role": ask("role", args.role),
            "purpose": ask("purpose", args.purpose),
            "limitations": ask("limitations", args.limitations),
            "verified_on": verified_on,
            "status": status,
        }
        validate_entry(entry, entry["id"])
        if any(old["id"] == entry["id"] or old["url"] == entry["url"] for old in data["sources"]):
            raise ValueError("id ou URL já cadastrado")
        data["sources"].append(entry)
        data["sources"].sort(key=lambda item: item["id"])
        save_catalog(args.catalog, data)
        print(f"Fonte cadastrada: {entry['id']} ({entry['status']})")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Erro: {exc}") from exc
