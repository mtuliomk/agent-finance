# Importação XP: Previdência Privada

`make xp-import-previdencia FILE=nome.xlsx` lê a aba `Sua carteira` do arquivo em `inbox/XP/` e acrescenta a `state/positions/previdencia_privada.csv` somente fundos com `ticker` novo. IDs existentes são preservados integralmente; uma reimportação sem fundos novos não regrava o CSV.

O importador lê o bloco **Previdência Privada**, identifica seus cabeçalhos por categoria e confere a soma da coluna `Saldo` com o total do bloco. Cada linha de fundo gera um registro. Quando o nome se repete, a primeira ocorrência mantém o ticker básico e as seguintes recebem `_2`, `_3` etc. O CSV usa UTF-8, datas `YYYY-MM-DD` e valores monetários decimais com ponto, sem `R$`.

| Campo | Origem/regra |
| --- | --- |
| `ticker` | nome do fundo na coluna A, trocando espaços por `_`; ocorrências repetidas recebem `_2`, `_3` etc.; é o ID obrigatório |
| `description` | nome do fundo na coluna A |
| `type` | cabeçalho `Pós-Fixado` → `pos`, `Prefixado` → `pre`, `Inflação` → `ipca`, `Multimercados` → `multi`; outras categorias → `[pending]` |
| `investment_date` | `[pending]`: a seção não informa a data de cada aplicação |
| `due_date` | sempre vazio, conforme regra desta importação |
| `quantity` | sempre `1` |
| `available` | sempre `1` |
| `acquisition_price` | `Valor aplicado` da coluna G da própria linha; sem dado, `[pending]` |

Este arquivo é um recorte da XP. Ele não substitui o snapshot canônico da carteira nem deve ser somado a outro recorte da mesma posição sem conciliação.
