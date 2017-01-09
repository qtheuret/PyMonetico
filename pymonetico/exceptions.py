# coding: utf-8

class MoneticoException(Exception):

    def __repr__(self):
        return unicode(self.message).encode("utf-8")

    def __str__(self):
        return unicode(self.message).encode("utf-8")

    def __unicode__(self):
        return unicode(self.message).encode("utf-8")

class LoginException(MoneticoException):

    def __init__(self, message):
        super(MoneticoException, self).__init__(self)
        self.message = 'Error(s) during login at Monetico interface: \n%s' % message