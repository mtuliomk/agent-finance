#!/usr/bin/env python3
"""Parse B3 ISIN registry (NUMERACA.TXT) and enrich RF data with ISIN codes."""

import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
B3_NUMERACA = ROOT / "inbox" / "B3" / "isinp" / "NUMERACA.TXT"
B3_EMISSOR = ROOT / "inbox" / "B3" / "isinp" / "EMISSOR.TXT"
RF_CSV = ROOT / "state" / "positions" / "renda_fixa.csv"


def parse_numeraca():
    """Parse B3 NUMERACA file and return dict of securities."""
    securities = {}

    if not B3_NUMERACA.exists():
        print(f"⚠️  Arquivo não encontrado: {B3_NUMERACA}")
        return securities

    with B3_NUMERACA.open('r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            parts = [p.strip('"') for p in line.strip().split('","')]
            if len(parts) < 24:
                continue

            # Campos do NUMERACA.TXT
            date = parts[0]  # Data de referência
            status = parts[1]  # A/N (ativo/inativo)
            isin = parts[2]  # Código ISIN
            codigo_emissor = parts[3]  # Código do emissor
            ticker = parts[4]  # Código BVMFBovespa
            descricao = parts[5]  # Descrição
            dt_inicio = parts[6]  # Data início (AAAA)
            dt_inicio_full = parts[7]  # Data início completa (AAAAMMDD)
            dt_vencimento = parts[8]  # Data vencimento (AAAA)
            dt_vencimento_full = parts[9]  # Data vencimento completa (AAAAMMDD)
            taxa = parts[10]  # Taxa
            moeda = parts[11]  # Moeda

            # Armazenar informações
            if isin not in securities:
                securities[isin] = {
                    'isin': isin,
                    'codigo_emissor': codigo_emissor,
                    'ticker_bmf': ticker,
                    'descricao': descricao,
                    'data_inicio': dt_inicio_full,
                    'data_vencimento': dt_vencimento_full,
                    'taxa': taxa,
                    'moeda': moeda,
                    'ativo': status == 'A',
                }

    return securities


def encontrar_isin_para_rf(rf_description, rf_issuer, rf_due_date):
    """Encontra ISIN compatível para um título de renda fixa."""
    securities = parse_numeraca()

    candidatos = []

    for isin, data in securities.items():
        desc = data['descricao'].upper()

        # Critério 1: Descrição contém CERTIFICADO DE DEPOSITO BANCARIO (CDB)
        if 'CERTIFICADO DE DEPOSITO BANCARIO' not in desc:
            continue

        # Critério 2: Emissor (AGBK para AGIBANK)
        if rf_issuer.upper() not in desc and data['codigo_emissor'].upper() not in ['AGBK']:
            continue

        # Critério 3: Vencimento próximo (comparar ano/mês)
        if rf_due_date and data['data_vencimento']:
            try:
                due_date = datetime.strptime(rf_due_date, '%Y-%m-%d')
                b3_due = datetime.strptime(data['data_vencimento'], '%Y%m%d')

                # Aceitar vencimentos no mesmo mês (com tolerância de 3 dias)
                if abs((due_date - b3_due).days) > 3:
                    continue
            except:
                pass

        candidatos.append((isin, data))

    return candidatos


def main():
    """Listar CDBs de AGIBANK com vencimento em JUL/2027."""
    print("🔍 Procurando CDB AGIBANK - JUL/2027 no banco de dados B3...\n")

    # Encontrar candidatos
    candidatos = encontrar_isin_para_rf(
        'CDB AGIBANK - JUL/2027',
        'AGIBANK',
        '2027-07-21'  # Aproximação para julho/2027
    )

    if not candidatos:
        print("❌ Nenhum ISIN encontrado compatível")
        return

    print(f"✅ Encontrados {len(candidatos)} ISIN(s) compatível(is):\n")

    for isin, data in candidatos:
        print(f"ISIN: {isin}")
        print(f"  Descrição: {data['descricao']}")
        print(f"  Emissor: {data['codigo_emissor']}")
        print(f"  Vencimento: {data['data_vencimento']}")
        print(f"  Taxa: {data['taxa']}")
        print(f"  Moeda: {data['moeda']}")
        print(f"  Ativo: {'Sim' if data['ativo'] else 'Não'}")
        print()


if __name__ == '__main__':
    main()
