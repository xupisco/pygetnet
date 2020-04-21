## Cartões de teste

Observação: Ao utilizar os cartões de teste, é necessário ter atenção em alguns pontos:
- Utilize uma data de vencimento válida, ou seja, posterior à data atual.
- O nome do portador não deve ter caracteres especiais, como acento e Ç.
- O valor do CVV pode ser qualquer valor numérico com três dígitos.
- Para operações de tipo Débito, deve-se utilizar somente o cartão Visa: 4012001037141112.

| Bandeira   | Número            | Retorno                   | Mensagem                     |
| ---------- | ----------------- | ------------------------- | ---------------------------- |
| Master     | 5155901222280001  | Transação Autorizada	     | Transação Aprovada           |
| Master     | 5155901222270002  | Transação Não Autorizada  | Cartão Inválido              |
| Master     | 5155901222260003  | Transação Não Autorizada  | Cartão Vencido               |
| Master     | 5155901222250004  | Transação Não Autorizada  | Estabelecimento Inválido     |
| Master     | 5155901222240005  | Transação Não Autorizada  | Saldo Insuficiente           |
| Master     | 5155901222230006  | Transação Não Autorizada  | Autorização Recusada         |
| Master     | 5155901222220007  | Transação Não Autorizada  | Transacao Não Processada     |
| Master     | 5155901222210008  | Transação Não Autorizada  | Excede o Limite de Retiradas |
| VISA       | 4012001037141112  | Transação Autorizada      | Transação Aprovada           |

### Compras parceladas

**Mastercard**

| Transaction_type	    | # installments      | amount  |
| --------------------- | ------------------- | ------- |
| INSTALL_NO_INTEREST   | 3	                  | nnn0303 |
| INSTALL_NO_INTEREST   | 4	                  | nnn0404 |
| INSTALL_NO_INTEREST   | 5	                  | nnn0505 |
| INSTALL_NO_INTEREST   | 6	                  | nnn0606 |
| INSTALL_WITH_INTEREST | 3	                  | nnn0303 |
| INSTALL_WITH_INTEREST | 4	                  | nnn0404 |
| INSTALL_WITH_INTEREST | 5	                  | nnn0505 |
| INSTALL_WITH_INTEREST | 6	                  | nnn0606 |

**VISA**

| Transaction_type	    | # installments      | amount  |
| --------------------- | ------------------- | ------- |
| INSTALL_NO_INTEREST   | 3	                  | nnn0303 |
| INSTALL_NO_INTEREST   | 4	                  | nnn0404 |
| INSTALL_NO_INTEREST   | 5	                  | nnn0505 |
| INSTALL_NO_INTEREST   | 6	                  | nnn0606 |
| INSTALL_WITH_INTEREST | 2	                  | 20221   |
| INSTALL_WITH_INTEREST | 3	                  | 30221   |
| INSTALL_WITH_INTEREST | 4	                  | 40221   |
| INSTALL_WITH_INTEREST | 5	                  | 50221   |
