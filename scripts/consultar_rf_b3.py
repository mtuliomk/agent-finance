#!/usr/bin/env python3
"""Consulta títulos de renda fixa na base B3 (NUMERACA.TXT)."""

import argparse
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

ROOT = Path(__file__).parent.parent
B3_NUMERACA = ROOT / "inbox" / "B3" / "isinp" / "NUMERACA.TXT"

# Mapeamento de códigos de remuneração
TIPOS_REMUNERACAO = {
    'PRE': 'Pré-fixado',
    'DI1': 'CDI',
    'IPCA': 'IPCA',
    'ZERO': 'Zero-cupom',
    '': 'Sem informação',
}

TIPOS_INVESTIMENTO = ['CDB', 'CRA', 'CRI', 'DEB', 'LCA', 'LCD', 'LF', 'FND']

# Mapeamento de código emissor para nomes conhecidos
MAPEO_EMISSOR = {
    'AGBK': 'AGIBANK',
    'XPCE': 'XP',
}


class ConsultadorRFB3:
    def __init__(self, arquivo: Path = B3_NUMERACA):
        self.arquivo = arquivo
        self.titulos = []
        self._carregar_dados()

    def _carregar_dados(self):
        """Carrega dados do arquivo NUMERACA.TXT."""
        if not self.arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.arquivo}")

        with self.arquivo.open('r', encoding='utf-8') as f:
            for line in f:
                parts = [p.strip('"') for p in line.strip().split('","')]
                if len(parts) < 12:
                    continue

                # NUMERACA.TXT tem 45 campos:
                # 0: data_ref, 1: ativo, 2: isin, 3: cod_emissor, 4: ticker,
                # 5: descricao, 6: ano_inicio, 7: data_inicio, 8: ano_venc, 9: data_venc,
                # 10: taxa, 11: moeda, 12-17: taxas especiais, 18-43: outros

                titulo = {
                    'data_ref': parts[0],
                    'ativo': parts[1] == 'A',
                    'isin': parts[2],
                    'codigo_emissor': parts[3],
                    'ticker_bmf': parts[4],
                    'descricao': parts[5],
                    'ano_inicio': parts[6],
                    'data_inicio': self._formatar_data(parts[7]),
                    'ano_vencimento': parts[8],
                    'data_vencimento': self._formatar_data(parts[9]),
                    'taxa': parts[10],
                    'percentual': parts[15] if len(parts) > 15 else '',
                    'moeda': parts[11] if len(parts) > 11 else 'BRL',
                    'tipo_remuneracao': parts[14] if len(parts) > 14 else '',  # CDI, IPCA, PRE, etc
                }
                self.titulos.append(titulo)

    def _formatar_data(self, data_str: str) -> str:
        """Formata data de YYYYMMDD para YYYY-MM-DD."""
        if not data_str or len(data_str) != 8:
            return None
        try:
            return f"{data_str[0:4]}-{data_str[4:6]}-{data_str[6:8]}"
        except:
            return None

    def _eh_renda_fixa(self, descricao: str) -> bool:
        """Verifica se é titulo de renda fixa."""
        descricao_upper = descricao.upper()
        return any(tipo in descricao_upper for tipo in ['CERTIFICADO', 'DEBENTURE', 'LETRA FINANCEIRA'])

    def buscar(
        self,
        isin: str = None,
        emissor: str = None,
        tipo: str = None,
        vencimento: str = None,
        apenas_ativos: bool = False
    ) -> List[Dict]:
        """Busca títulos com os filtros especificados.

        Se ISIN for fornecido, busca apenas por ISIN (ignora outros filtros).
        Por padrão, inclui inativos (apenas_ativos=False) pois muitos títulos
        no banco B3 estão inativados mas ainda com dados válidos.
        """
        resultados = []

        for titulo in self.titulos:
            # Filtro prioritário: ISIN
            if isin:
                if titulo['isin'].upper() == isin.upper():
                    resultados.append(titulo)
                continue
            # Filtro: apenas ativos (desabilitado por padrão)
            if apenas_ativos and not titulo['ativo']:
                continue

            # Filtro: renda fixa
            if not self._eh_renda_fixa(titulo['descricao']):
                continue

            # Filtro: emissor (busca flexível)
            if emissor:
                emissor_upper = emissor.upper()
                codigo_upper = titulo['codigo_emissor'].upper()
                descricao_upper = titulo['descricao'].upper()
                nome_mapeado = MAPEO_EMISSOR.get(codigo_upper, '').upper()

                # Busca: código contém emissor, emissor contém código,
                # descrição contém emissor, ou nome mapeado contém emissor
                match = (
                    emissor_upper in codigo_upper or
                    codigo_upper in emissor_upper or
                    emissor_upper in descricao_upper or
                    (nome_mapeado and emissor_upper in nome_mapeado) or
                    (nome_mapeado and nome_mapeado in emissor_upper)
                )
                if not match:
                    continue

            # Filtro: tipo de investimento
            if tipo:
                tipo_upper = tipo.upper()
                # CDB: procurar em CERTIFICADO DE DEPOSITO BANCARIO
                if tipo_upper == 'CDB':
                    if 'CERTIFICADO DE DEPOSITO BANCARIO' not in titulo['descricao'].upper():
                        continue
                else:
                    if tipo_upper not in titulo['descricao'].upper():
                        continue

            # Filtro: vencimento
            if vencimento and titulo['data_vencimento']:
                if not self._filtrar_vencimento(titulo['data_vencimento'], vencimento):
                    continue

            resultados.append(titulo)

        return sorted(resultados, key=lambda x: x['data_vencimento'] or '')

    def _filtrar_vencimento(self, data_titulo: str, filtro: str) -> bool:
        """Verifica se a data do título corresponde ao filtro."""
        if not data_titulo:
            return False

        filtro = filtro.upper()

        # Filtro por ano: "2027"
        if len(filtro) == 4 and filtro.isdigit():
            return data_titulo.startswith(filtro)

        # Filtro por ano-mês: "2027-07" ou "2027/07"
        if len(filtro) == 7:
            filtro_normalizado = filtro.replace('/', '-')
            return data_titulo.startswith(filtro_normalizado)

        # Filtro por período: "2027-Q3" (trimestral)
        if 'Q' in filtro:
            ano, trimestre = filtro.split('-Q')
            mes_inicio = (int(trimestre) - 1) * 3 + 1
            mes_fim = int(trimestre) * 3
            mes_titulo = int(data_titulo[5:7])
            return data_titulo.startswith(ano) and mes_inicio <= mes_titulo <= mes_fim

        # Filtro por data exata: "2027-07-21"
        return data_titulo == filtro

    def formatar_saida(self, resultados: List[Dict]) -> str:
        """Formata resultados para exibição."""
        if not resultados:
            return "❌ Nenhum título encontrado com os critérios especificados."

        output = f"✅ Encontrados {len(resultados)} título(s):\n\n"

        for i, titulo in enumerate(resultados, 1):
            tipo_rem = TIPOS_REMUNERACAO.get(titulo['tipo_remuneracao'], titulo['tipo_remuneracao'])

            output += f"{i}. {titulo['isin']}\n"
            output += f"   Descrição: {titulo['descricao']}\n"
            output += f"   Emissor: {titulo['codigo_emissor']}\n"
            output += f"   Vencimento: {titulo['data_vencimento']}\n"

            if titulo['taxa']:
                output += f"   Taxa: {titulo['taxa']}%\n"
            if titulo['percentual']:
                output += f"   Percentual: {titulo['percentual']}\n"
            if titulo['tipo_remuneracao']:
                output += f"   Remuneração: {tipo_rem}\n"

            output += f"   Moeda: {titulo['moeda']}\n"
            output += f"   Ativo: {'Sim' if titulo['ativo'] else 'Não (inativo)'}\n"
            output += "\n"

        return output


def main():
    parser = argparse.ArgumentParser(
        description='Consulta títulos de renda fixa na base B3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  # Buscar por ISIN direto
  %(prog)s --isin BRAGBKC00JG1

  # Buscar por filtros
  %(prog)s --emissor AGIBANK --tipo CDB --vencimento 2027-07
  %(prog)s --emissor "BANCO XP" --tipo CDB
  %(prog)s --tipo CRA --vencimento 2027
        '''
    )

    parser.add_argument(
        '--isin',
        help='Código ISIN (ex: BRAGBKC00JG1) - busca prioritária, ignora outros filtros'
    )
    parser.add_argument(
        '--emissor',
        help='Nome ou código do emissor (ex: AGIBANK, BANCO XP, BMG)'
    )
    parser.add_argument(
        '--tipo',
        help='Tipo de investimento (CDB, CRA, CRI, DEB, LCA, LCD, LF, FND)'
    )
    parser.add_argument(
        '--vencimento',
        help='Data de vencimento (ex: 2027-07-21, 2027-07, 2027, 2027-Q3)'
    )
    parser.add_argument(
        '--apenas-ativos',
        action='store_true',
        help='Incluir apenas títulos ativos (padrão: inclui inativos)'
    )
    parser.add_argument(
        '--formato',
        choices=['texto', 'csv'],
        default='texto',
        help='Formato de saída (padrão: texto)'
    )

    args = parser.parse_args()

    # Validação: ao menos um filtro
    if not any([args.isin, args.emissor, args.tipo, args.vencimento]):
        parser.error('Especifique ao menos um filtro: --isin, --emissor, --tipo ou --vencimento')

    try:
        consultor = ConsultadorRFB3()
        resultados = consultor.buscar(
            isin=args.isin,
            emissor=args.emissor,
            tipo=args.tipo,
            vencimento=args.vencimento,
            apenas_ativos=args.apenas_ativos
        )

        if args.formato == 'csv':
            if resultados:
                writer = csv.DictWriter(
                    __import__('sys').stdout,
                    fieldnames=resultados[0].keys()
                )
                writer.writeheader()
                writer.writerows(resultados)
        else:
            print(consultor.formatar_saida(resultados))

    except Exception as exc:
        raise SystemExit(f"Erro: {exc}") from exc


if __name__ == '__main__':
    main()
