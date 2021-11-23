from Acquisition import aq_inner
#from zope.component import getUtility
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from currency.converter.interfaces import IPortalCurrency

class PortalCurrency(object):

    implements(IPortalCurrency)

    def __init__(self, context):
        self.context = context

    @property
    def portal_currency_code(self):
        """Returns default currency code of portal."""
        context = aq_inner(self.context)
        properties = getToolByName(context, 'portal_properties')
        return properties.currency_converter_properties.getProperty('portal_currency')

    @property
    def member_currency_code(self, proprety_name='currency'):
        """Returns member's currency code."""
        context = aq_inner(self.context)
        portal_currency_code = self.portal_currency_code
        membership = getToolByName(context, u'portal_membership')
        member = membership.getAuthenticatedMember()
        if proprety_name in member.propertyIds():
            currency_code = member.getProperty(proprety_name)
            if currency_code is not None or currency_code != '':
                return currency_code
        else:
            return portal_currency_code

    @property
    def selected_currency_code(self, session_key='selected_currency_code'):
        """Returns selected currency code from session."""  
        context = aq_inner(self.context)
        sdm = getToolByName(context, "session_data_manager")
        member_currency_code = self.member_currency_code
        session = sdm.getSessionData(create=False)
        if (session is not None and session.get(session_key) is not None):
            return session.get(session_key)
        else:
            return member_currency_code

