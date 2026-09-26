# Importação XP: Renda Fixa

`make xp-import-rf FILE=nome.xlsx` lê a aba `Sua carteira` do arquivo em `inbox/XP/` e acrescenta a `state/positions/renda_fixa.csv` somente títulos com `ticker` novo. IDs existentes são preservados integralmente; uma reimportação sem IDs novos não regrava o CSV, exceto para migrar o cabeçalho antigo sem `isin`.

O importador lê o bloco **Renda Fixa** e confere a soma da coluna `Saldo a mercado` com o total da seção. O export atual apresenta diferença de R$ 0,03 entre a soma dos 174 saldos exibidos e o total; a conciliação aceita diferença de arredondamento de até R$ 0,05, limitada também a R$ 0,005 por linha mais R$ 0,005 para o total. Diferenças maiores interrompem a importação. Cada linha vira um registro; nomes repetidos recebem sufixos `_2`, `_3` etc. O CSV usa UTF-8, datas `YYYY-MM-DD`, inteiros sem separador de milhar e valores monetários decimais com ponto, sem `R$`.

| Campo | Origem/regra |
| --- | --- |
| `ticker` | descrição da coluna A, trocando espaços por `_`; ocorrências repetidas recebem `_2`, `_3` etc. |
| `description` | descrição da coluna A |
| `type` | sempre `variavel`, conforme regra definida para esta importação |
| `investment_date` | `Data aplicação` da coluna G |
| `due_date` | `Data vencimento` da coluna H |
| `quantity` | `Quantidade` da coluna I |
| `available` | repete `Quantidade` da coluna I |
| `acquisition_price` | `Valor aplicado` da coluna D, que é o valor total aplicado da linha |
| `market_rentability` | texto da coluna F, `Rentabilidade a mercado`, preservado como consta na origem |
| `isin` | `[pending]`, pois o export da XP não informa o código; a coluna é acrescentada ao fim do CSV, inclusive para registros já importados |

Campos sem dado na origem ficam `[pending]`, exceto o ID, que é obrigatório. O campo `market_rentability` é texto, por exemplo `IPC-A +5,35%`; o importador não o transforma em taxa numérica nem em rendimento realizado. Ao encontrar o cabeçalho anterior, o importador acrescenta `isin` com `[pending]` às linhas existentes e preserva os demais valores. Este arquivo é um recorte da XP e não substitui o snapshot canônico da carteira.
