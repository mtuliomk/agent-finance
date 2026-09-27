# Importação XP: Renda Fixa

`make xp-import-rf FILE=nome.xlsx` lê a aba `Sua carteira` do arquivo em `inbox/XP/` e acrescenta a `state/positions/renda_fixa.csv` somente títulos com `ticker` novo. IDs existentes são preservados; uma reimportação sem IDs novos não regrava o CSV, exceto para migrar cabeçalhos anteriores sem `isin` e/ou `issuer` ou preencher `issuer` ainda `[pending]` quando a descrição permitir.

O importador lê o bloco **Renda Fixa** e confere a soma da coluna `Saldo a mercado` com o total da seção. A conciliação aceita diferença de arredondamento de até R$ 0,05, limitada também a R$ 0,005 por linha mais R$ 0,005 para o total. Diferenças maiores interrompem a importação. Cada linha vira um registro; nomes repetidos recebem sufixos `_2`, `_3` etc. O CSV usa UTF-8, datas `YYYY-MM-DD`, inteiros sem separador de milhar e valores monetários decimais com ponto, sem `R$`.

| Campo | Origem/regra |
| --- | --- |
| `ticker` | descrição da coluna A, trocando espaços por `_`; ocorrências repetidas recebem `_2`, `_3` etc. |
| `description` | descrição da coluna A |
| `type` | classificação baseada no campo `Rentabilidade a mercado` (coluna F): `ipca` quando contém "IPC-A" ou "IPCA"; `pos` quando contém "CDI"; `pre` quando começa com "+" sem menção a CDI, ou contém "a.a." ou "a.m." (ao ano/mês) sem CDI/IPCA; `[pending]` quando a rentabilidade está indefinida ou não se encaixa nos padrões |
| `investment_date` | `Data aplicação` da coluna G |
| `due_date` | `Data vencimento` da coluna H |
| `quantity` | `Quantidade` da coluna I |
| `available` | repete `Quantidade` da coluna I |
| `acquisition_price` | `Valor aplicado` da coluna D, que é o valor total aplicado da linha |
| `market_rentability` | texto da coluna F, `Rentabilidade a mercado`, preservado como consta na origem |
| `isin` | `[pending]`, pois o export da XP não informa o código; o campo é acrescentado também aos registros já importados |
| `issuer` | nome entre o prefixo do tipo de investimento e o vencimento ` - MMM/AAAA`, sem o sufixo ` - JURO MENSAL`; `[pending]` para descrições fora desse padrão |
| `investment_type` | prefixo extraído da descrição: `CDB`, `CRA`, `CRI`, `DEB`, `LCA`, `LCD`, `LF` ou `FND`; `[pending]` para descrições fora desse padrão |

Campos sem dado na origem ficam `[pending]`, exceto o ID, que é obrigatório. O campo `market_rentability` é texto, por exemplo `IPC-A +5,35%`; o importador não o transforma em taxa numérica nem em rendimento realizado. Ao encontrar um cabeçalho anterior, o importador acrescenta os campos ausentes às linhas existentes e preserva os demais valores. Em reimportações, preenche somente `issuer` ainda `[pending]` e mantém valores preenchidos manualmente. O `issuer` extraído reproduz o nome da descrição, que pode estar abreviado; não confirma a razão social. Para CRI e CRA, o nome exibido pode se referir ao devedor ou à operação e não identifica com segurança a securitizadora emissora. Este arquivo é um recorte da XP e não substitui o snapshot canônico da carteira.
