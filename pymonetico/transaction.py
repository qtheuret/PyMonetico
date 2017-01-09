# coding: utf-8

from time import strptime
from time import mktime
from datetime import datetime


class Transaction(object):

    def __init__(self, state, tpe, site, reference, payment_date,
                 amount, currency, payment_method, network):
        """
        Initialize a new instance of Transaction
        :param state: State of the transaction
        :param tpe: PaymentTerminal instance
        :param site: Code of the site on which the payment has been made
        :param reference: Reference of the transaction
        :param payment_date: Payment date of the transaction
        :param amount: Amount of the transaction
        :param currency: Currency of the transaction
        :param payment_method: Payment method
        :param network: Network of the credit card (Visa, MasterCard...)
        """
        self.state = state
        self.tpe = tpe
        self.site = site
        self.reference = reference
        self.payment_date = datetime.fromtimestamp(mktime(strptime(payment_date, '%Y-%m-%dT%H:%M:%S')))
        self.amount = amount and float(amount.replace(',', '.'))
        self.currency = currency
        self.payment_method = payment_method
        self.network = network

    def __repr__(self):
        params = {
            'reference': self.reference,
            'payment_date': self.payment_date,
            'tpe_id': self.tpe.tpe_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'site': self.site,
            'network': self.network,
        }
        return '<Transaction Reference=%(reference)s DatePaiement=%(payment_date)s TPE=%(tpe_id)s ' \
               'Montant=%(amount)s Devise=%(currency)s MethodePaiement=%(payment_method)s ' \
               'CodeSite=%(site)s ReseauCarte=%(network)s' % params