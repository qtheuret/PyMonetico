# coding: utf-8

from datetime import date

from pymonetico.payment_terminal import PaymentTerminal
from pymonetico.transactions_search import TransactionsSearch

USER = ''
PWD = ''
TPE_ID = ''

if __name__ == '__main__':
    tpe = PaymentTerminal(TPE_ID, USER, PWD)
    tpe.login()

    search = TransactionsSearch(
        type='Achat',
        date_from=date(2016, 01, 01),
        date_to=date(2016, 01, 31),
        paid=True,
    )

    tpe.search(search)
