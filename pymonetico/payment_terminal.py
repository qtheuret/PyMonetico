# coding: utf-8

import mechanize
import cookielib

from lxml import etree

from exceptions import LoginException
from transaction import Transaction


LOGOUT_URL = 'https://www.monetico-services.com/fr/identification/deconnexion/deconnexion.cgi'
LOGIN_URL = 'https://www.monetico-services.com/fr/identification/authentification.html'
HOME_URL = 'https://www.monetico-services.com/fr/client/Accueil.aspx'
SEARCH_URL = 'https://www.monetico-services.com/fr/client/Paiement/Paiement_RechercheAvancee.aspx' \
             '?__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE='


class PaymentTerminal(object):

    def __init__(self, tpe_id, user_id, password):
        """
        Create a new instance of a PaymentTerminal
        :param tpe_id: The ID of the TPE
        :param user_id: The username to access to the web interface of Monetico
        :param password: The password to access to the web interface of Monetico
        """
        self.tpe_id = tpe_id
        self.user_id = user_id
        self.password = password
        self.browser = self._prepare_browser()

    @property
    def is_connected(self):
        """
        Check if the TPE interface is connected
        :return: True or False
        """
        r = self.browser.open(HOME_URL)
        root = self.parse_response(r)
        tpe_list = root.xpath('//select[@name=\'ChoixTPE\']')
        if not tpe_list:
            return False

        for tpe in tpe_list[0]:
            if tpe.attrib and tpe.attrib.get('value') == self.tpe_id:
                return True

        return False

    @staticmethod
    def _prepare_browser():
        """
        Prepare a web browser
        :return: A mechanize.Browser() instance prepared for Monetico connection
        """
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # User-Agent (this is cheating, ok ?)
        br.addheaders = [('User-agent',
                          '''Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)
                          Gecko/2008071615 Fedobra/3.0.1-1.fc9 Firefox/34.0''')]

        return br

    def login(self):
        """
        Make a login on the Monetico web interface
        :return:
        """
        self.browser.open(LOGIN_URL)

        self.browser.select_form(name='bloc_ident')
        self.browser.form['_cm_user'] = self.user_id
        self.browser.form['_cm_pwd'] = self.password

        auth_response = self.browser.submit()

        root = self.parse_response(auth_response)
        err_msg = root.xpath('//div[@class=\'blocmsg err\']/p')
        not_connected_msg = []
        if err_msg:
            for msg in err_msg:
                not_connected_msg.append(msg.text)

        if not_connected_msg:
            raise LoginException('\n'.join(x for x in not_connected_msg))

    def logout(self):
        """
        Logout for web interface
        :return:
        """
        self.browser.open(LOGOUT_URL)

    @staticmethod
    def parse_response(response):
        """
        Parse the HTTP response result of the browser
        :param response: HTTP Browse response
        :return: A XML root
        """
        parser = etree.XMLParser(encoding='iso-8859-1', recover=True)
        return etree.XML(response.read(), parser)

    def search(self, search):
        """
        Make a search by calling search URL and return a list of transactions
        :param search: TransactionsSearch instance
        :return: A list of MoneticoTransactions returned by the search
        """
        if not self.is_connected:
            raise BaseException('You are not logged on Monetico interface. Please do PaymentTerminal.login() before'
                                'using search() method.')

        search_url = '%(base_url)s&tpe_id=%(tpe_id)s&ChoixTPE=%(tpe_id)s&%(search_string)s&export=XML' % {
            'base_url': SEARCH_URL,
            'tpe_id': self.tpe_id,
            'search_string': search.search_string,
        }
        response = self.browser.open(search_url)
        xml_export = etree.XML(response.read())

        transactions = []

        for element in xml_export.iter("IEnumerableOfCommandeFormatExport"):
            for t in element.iter("Commande"):
                transactions.append(Transaction(
                    state=t.find('Etat').text,
                    tpe=self,
                    site=t.find('CodeSite').text,
                    reference=t.find('Reference').text,
                    payment_date=t.find('DatePaiement').text,
                    amount=t.find('Montant').find('Valeur').text,
                    currency=t.find('Montant').find('Devise').text,
                    payment_method=t.find('MethodePaiement').text,
                    network=t.find('ReseauCarte').text,
                ))

        return transactions
