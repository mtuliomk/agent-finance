# Importação XP: Tesouro Direto

`make xp-import-position FILE=nome.xlsx` lê o arquivo em `inbox/XP/` e acrescenta a `state/positions/tesouro_direto.csv` apenas títulos com `ticker` novo. Registros existentes são preservados integralmente; uma reimportação sem IDs novos não regrava o arquivo. Se a descrição se repetir no Excel, a primeira linha mantém o ticker básico e as seguintes recebem sufixos sequenciais `_2`, `_3` etc.; um sufixo é pulado caso conflite com outro ticker derivado diretamente da origem. Todas as linhas entram na conciliação do saldo. O importador foi ajustado ao export `PosicaoDetalhada.xlsx` com aba `Sua carteira`: localiza o cabeçalho `Saldo | % Alocação | Valor aplicado | Quantidade | Disponível | Vencimento`, lê cada título e concilia a soma dos saldos com o total da seção antes de gravar. Mudança de layout interrompe a importação; tipo de título que não pode ser classificado fica `[pending]`.

O CSV usa UTF-8, datas `YYYY-MM-DD`, decimais com ponto e valores monetários sem `R$`. Em registros novos, campo de saída sem dado na origem fica literalmente `[pending]`; `ticker` é o identificador e é obrigatório. Zero informado pela origem continua zero. Campos vazios de registros antigos permanecem como estão, pois a importação não atualiza IDs existentes.

| Campo | Origem/regra |
| --- | --- |
| `ticker` | descrição da coluna A, trocando espaços por `_`; ocorrências repetidas recebem `_2`, `_3` etc. |
| `description` | descrição da coluna A sem alteração |
| `type` | `LFT`/Tesouro Selic → `pos`; `LTN`/`NTN-F` → `pre`; `NTN-B`/`NTN-B1` → `ipca` |
| `investment_date` | `[pending]`: o export de posição não informa a data de cada compra |
| `due_date` | coluna G, vencimento |
| `quantity` | coluna E, decimal |
| `available` | coluna F, decimal |
| `acquisition_price` | `[pending]`: o export não informa preço unitário de compra |

As quantidades do arquivo real são fracionárias; convertê-las para inteiro perderia informação. `Valor aplicado` da coluna D é lido para validar o formato, mas não é usado como preço de aquisição. O valor do saldo (coluna B) serve apenas para conciliar o total da seção. Este CSV é um recorte da XP e não substitui o snapshot canônico da carteira em `state/positions/`.
