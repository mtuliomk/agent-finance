# Importação XP: Fundos Imobiliários

`make xp-import-fii FILE=nome.xlsx` lê a aba `Sua carteira` do arquivo em `inbox/XP/` e acrescenta a `state/positions/fundos_imobiliarios.csv` somente FIIs com `ticker` novo. IDs existentes são preservados integralmente; uma reimportação sem FIIs novos não regrava o CSV.

O importador lê o bloco **Fundos Imobiliários** e confere a soma da coluna `Saldo` com o total da seção. Cada ticker deve ser único na origem. O CSV usa UTF-8, datas `YYYY-MM-DD` quando disponíveis, inteiros sem separador de milhar e preços decimais com ponto, sem `R$`.

| Campo | Origem/regra |
| --- | --- |
| `ticker` | ticker da coluna A; é o ID obrigatório e único |
| `description` | ticker da coluna A |
| `type` | sempre `variavel` |
| `investment_date` | `[pending]`: a seção não informa data de compra |
| `due_date` | sempre vazio |
| `quantity` | `Qtd. total` da coluna F |
| `available` | `Quantidade de Cotas` da coluna G |
| `acquisition_price` | `Preço médio (abertura)` da coluna D; `Indefinido` ou vazio vira `[pending]` |

Este arquivo é um recorte da XP. Ele não substitui o snapshot canônico da carteira nem deve ser somado a outro recorte da mesma posição sem conciliação.
