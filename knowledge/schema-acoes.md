# Importação XP: Ações

`make xp-import-acoes FILE=nome.xlsx` lê a aba `Sua carteira` do arquivo em `inbox/XP/` e acrescenta a `state/positions/acoes.csv` somente ações com `ticker` novo. IDs existentes são preservados integralmente; uma reimportação sem tickers novos não regrava o CSV.

O importador lê o bloco **Ações** da posição, identificado pelo cabeçalho `Saldo | % Alocação | Rentabilidade | Preço médio | Último preço (R$) | Qtd. total`, sem confundi-lo com o bloco de proventos também chamado **Ações**. Confere a soma da coluna `Saldo` com o total da seção. Cada ticker deve ser único na origem. O CSV usa UTF-8, datas `YYYY-MM-DD` quando disponíveis, inteiros sem separador de milhar e preços decimais com ponto, sem `R$`.

| Campo | Origem/regra |
| --- | --- |
| `ticker` | ticker da coluna A; é o ID obrigatório e único |
| `description` | ticker da coluna A |
| `type` | sempre `variavel` |
| `investment_date` | `[pending]`: a seção não informa data de compra |
| `due_date` | sempre vazio |
| `quantity` | `Qtd. total` da coluna G |
| `available` | repete `Qtd. total` da coluna G, conforme regra definida para esta importação |
| `acquisition_price` | `Preço médio` da coluna E; `Indefinido` ou vazio vira `[pending]` |

Este arquivo é um recorte da XP. Ele não substitui o snapshot canônico da carteira nem deve ser somado a outro recorte da mesma posição sem conciliação.
