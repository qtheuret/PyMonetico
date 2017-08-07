# coding: utf-8

TRANSACTION_TYPES = ['Achat', 'Recouvrement', 'Recredit', 'Impaye', 'Reference']


class TransactionsSearch(object):

    def __init__(self, type=None, ref=None, date_from=None, date_to=None, amount_from=None, amount_to=None,
                 paid=True, refused=True, recorded=True, no_card=True, in_progress=True):
        """
        A Monetico search with some parameters
        :param type: Type of the search (achat, recouvrement, recredit, impaye)
        :param ref: Reference of the transaction
        :param date_from: Search transactions after this date
        :param date_to: Search transactions before this date
        :param amount_from: Minimum amount of the transaction
        :param amount_to: Maximum amount of the transaction
        :param paid: If True, search paid transactions
        :param refused: If True, search refused transactions
        :param recorded: If True, search recorded transactions
        :param no_card: If True, search transactions with no card filled
        :param in_progress: If True, search in progress transactions
        """
        self._type = type
        self.ref = ref
        self.date_from = date_from
        self.date_to = date_to
        self._amount_from = amount_from
        self._amount_to = amount_to
        self.paid = paid
        self.refused = refused
        self.recorded = recorded
        self.no_card = no_card
        self.in_progress = in_progress

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in TRANSACTION_TYPES:
            raise ValueError('\'%s\' is not a valid transaction type. Possible types: %s' % (
                value,
                ' / '.join(str(x) for x in TRANSACTION_TYPES),
            ))
        else:
            self._type = value

    @property
    def amount_from(self):
        return self._amount_from

    @amount_from.setter
    def amount_from(self, value):
        if value < 0.00:
            raise ValueError('\'From amount\' value should be positive')
        else:
            self._amount_from = value

    @property
    def amount_to(self):
        return self._amount_to

    @amount_from.setter
    def amount_to(self, value):
        if value is not None and value < 0.00:
            raise ValueError('\'To amount\' value should be positive')
        else:
            self._amount_to = value

    @property
    def search_string(self):
        """
        Build the search string to put on the Monetico URI
        :return: A string to put on the Monetico URI to make the search
        """
        if self.type == 'Reference' and not self.ref:
            raise ValueError('If you search transaction by \'Reference\', '
                             'you should define a reference on the search instance')

        params = {
            'Date_Debut': self.date_from and self.date_from.strftime('%d/%m/%Y') or '',
            'Date_Fin': self.date_to and self.date_to.strftime('%d/%m/%Y') or '',
            'SelectionCritere': self.type,
            'dnfta_Reference': self.type == 'Reference' and self.ref or '',
            'Paye': self.paid and 'on' or None,
            'Paye.p': '',
            'Refuse': self.refused and 'on' or None,
            'Refuse.p': '',
            'Enregistre': self.recorded and 'on' or None,
            'Enregistre.p': '',
            'CarteNonSaisie': self.no_card and 'on' or None,
            'CarteNonSaisie.p': '',
            'EnCours': self.in_progress and 'on' or None,
            'EnCours.p': '',
            'Montant_Min': self.amount_from or '',
            'Montant_Max': self.amount_to or '',
            'Currency': 'EUR',
            'SelectionAffichage': 'Ecran',
        }

        return '&'.join('%s=%s' % (k, v) for k, v in params.iteritems() if v is not None)
