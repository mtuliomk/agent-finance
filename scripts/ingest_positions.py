#!/usr/bin/env python3
"""Validate a canonical position CSV and publish one complete custodian snapshot."""

import argparse
import csv
import hashlib
import json
import shutil
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSITIONS = ROOT / "state" / "positions"
RAW = ROOT / "state" / "raw"
FIELDS = [
    "custodian", "position_id", "asset_class", "instrument_name", "instrument_id",
    "issuer", "conglomerate", "currency", "quantity", "cost_basis", "market_value",
    "valuation_date", "acquisition_date", "maturity_date", "rate_type", "rate_value",
    "rate_basis", "liquidity_terms", "source_locator", "notes",
]
REQUIRED = {"custodian", "position_id", "asset_class", "instrument_name", "currency", "valuation_date", "source_locator"}
CLASSES = {"CDB", "LCA", "CRI", "ACAO", "FII", "OUTRO"}
RATE_TYPES = {"", "PREFIXADO", "PCT_CDI", "CDI_MAIS", "IPCA_MAIS", "OUTRO"}


def parse_date(value, label):
    try:
        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError("formato inválido")
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label}: data inválida {value!r}; use YYYY-MM-DD") from exc


def load_rows(path, custodian, as_of):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError("Cabeçalho diferente do schema-posicoes.md; preserve a ordem e os nomes")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV sem posições; não publique snapshot vazio sem revisar o fluxo")
    seen = set()
    totals = {}
    warnings = []
    for number, row in enumerate(rows, start=2):
        if None in row:
            raise ValueError(f"Linha {number}: colunas extras")
        row = {key: value.strip() for key, value in row.items()}
        rows[number - 2] = row
        missing = sorted(key for key in REQUIRED if not row[key])
        if missing:
            raise ValueError(f"Linha {number}: obrigatórios vazios: {', '.join(missing)}")
        if row["custodian"] != custodian:
            raise ValueError(f"Linha {number}: custodiante diferente de {custodian}")
        if row["asset_class"] not in CLASSES or row["rate_type"] not in RATE_TYPES:
            raise ValueError(f"Linha {number}: classe ou tipo de taxa desconhecido")
        if len(row["currency"]) != 3 or not row["currency"].isalpha() or row["currency"] != row["currency"].upper():
            raise ValueError(f"Linha {number}: moeda deve ser código ISO 4217 em maiúsculas")
        if row["position_id"] in seen:
            raise ValueError(f"Linha {number}: position_id duplicado {row['position_id']}")
        seen.add(row["position_id"])
        if parse_date(row["valuation_date"], f"Linha {number} valuation_date") != as_of:
            raise ValueError(f"Linha {number}: valuation_date difere de --as-of")
        for key in ("acquisition_date", "maturity_date"):
            if row[key]:
                parse_date(row[key], f"Linha {number} {key}")
        if row["acquisition_date"] and row["maturity_date"] and row["acquisition_date"] > row["maturity_date"]:
            raise ValueError(f"Linha {number}: aquisição posterior ao vencimento")
        for key in ("quantity", "cost_basis", "market_value", "rate_value"):
            if not row[key]:
                continue
            try:
                value = Decimal(row[key])
            except InvalidOperation as exc:
                raise ValueError(f"Linha {number}: {key} não é decimal com ponto") from exc
            if not value.is_finite() or (key != "rate_value" and value < 0):
                raise ValueError(f"Linha {number}: {key} inválido")
            if key == "market_value":
                group = (row["currency"], row["asset_class"])
                totals[group] = totals.get(group, Decimal(0)) + value
        if row["rate_type"] and (not row["rate_value"] or not row["rate_basis"]):
            warnings.append(f"{row['position_id']}: taxa incompleta")
        if row["asset_class"] in {"CDB", "LCA", "CRI"} and not row["issuer"]:
            warnings.append(f"{row['position_id']}: emissor desconhecido")
        if row["asset_class"] in {"CDB", "LCA"} and not row["conglomerate"]:
            warnings.append(f"{row['position_id']}: conglomerado não classificado")
        if not row["market_value"]:
            warnings.append(f"{row['position_id']}: valor de mercado ausente")
    return rows, totals, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True, help="Arquivo original XLSX ou PDF")
    parser.add_argument("--custodian", choices=("XP", "BTG"), required=True)
    parser.add_argument("--as-of", required=True, help="Data da fotografia YYYY-MM-DD")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--confirmed-complete", action="store_true")
    parser.add_argument("--accept-removals", action="store_true")
    args = parser.parse_args()
    as_of = parse_date(args.as_of, "--as-of")
    if not args.csv.is_file() or not args.source.is_file():
        parser.error("--csv e --source devem apontar para arquivos existentes")
    rows, totals, warnings = load_rows(args.csv, args.custodian, as_of)
    previous = POSITIONS / f"{args.custodian}.csv"
    old_ids = set()
    if previous.exists():
        with previous.open(encoding="utf-8", newline="") as handle:
            old_ids = {row["position_id"] for row in csv.DictReader(handle)}
    new_ids = {row["position_id"] for row in rows}
    removals = sorted(old_ids - new_ids)
    print(f"{args.custodian} {as_of}: {len(rows)} posições; novas={len(new_ids-old_ids)}; removidas={len(removals)}")
    for (currency, asset_class), value in sorted(totals.items()):
        print(f"  {currency} {asset_class}: {value}")
    for warning in warnings:
        print(f"  ATENÇÃO: {warning}")
    if removals:
        print("  IDs removidos: " + ", ".join(removals))
    if not args.commit:
        print("Prévia apenas; nenhum state atualizado")
        return
    if not args.confirmed_complete:
        parser.error("--commit exige --confirmed-complete após conciliar com o original")
    if removals and not args.accept_removals:
        parser.error("remoções exigem --accept-removals após conferência")
    manifest_path = POSITIONS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"schema_version": 1, "custodians": {}}
    last = manifest["custodians"].get(args.custodian)
    if last and as_of < parse_date(last["as_of"], "manifest as_of"):
        parser.error("snapshot anterior ao atual; não substitua por fotografia mais antiga")
    source_hash = hashlib.sha256(args.source.read_bytes()).hexdigest()
    csv_hash = hashlib.sha256(args.csv.read_bytes()).hexdigest()
    RAW.mkdir(parents=True, exist_ok=True)
    POSITIONS.mkdir(parents=True, exist_ok=True)
    archived = RAW / f"{source_hash[:16]}-{args.source.name}"
    if not archived.exists():
        shutil.copy2(args.source, archived)
    history = POSITIONS / "history" / args.custodian
    history.mkdir(parents=True, exist_ok=True)
    snapshot = history / f"{as_of}-{csv_hash[:16]}.csv"
    with snapshot.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    snapshot_hash = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    shutil.copy2(snapshot, previous)
    manifest["custodians"][args.custodian] = {
        "as_of": str(as_of), "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": source_hash, "source_path": str(archived.relative_to(ROOT)),
        "snapshot_sha256": snapshot_hash, "snapshot_path": str(snapshot.relative_to(ROOT)),
        "position_count": len(rows), "warnings": warnings,
    }
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest_path)
    print("State atualizado: " + str(previous.relative_to(ROOT)))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, csv.Error) as exc:
        raise SystemExit(f"Erro: {exc}") from exc
