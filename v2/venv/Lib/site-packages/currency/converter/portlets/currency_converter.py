from zope.component import (getMultiAdapter,
                            queryUtility,
                            getUtility)

from zope.interface import implements
from zope import schema
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from currency.converter import CurrencyConverterMessageFactory as _
from currency.converter.browser.currency_manager import CurrencyManagerView
from currency.converter.browser.currency_converter_viewlet import CurrencyConverterViewlet

from currency.converter.interfaces import ICurrencyData
from currency.converter.currencies import currencies

from zope.interface import implements, directlyProvides

class ICurrencyConverterPortlet(IPortletDataProvider):
    """ICurrencyConverterPortlet"""

class Assignment(base.Assignment):
    implements(ICurrencyConverterPortlet)

    @property
    def title(self):
        return _(u'Currency Converter')

class Renderer(base.Renderer, CurrencyConverterViewlet):

    render = ViewPageTemplateFile('currency_converter.pt')

    def update(self):
         CurrencyConverterViewlet.update(self)

    def current_url(self):
        """Returns current url"""
        context= aq_inner(self.context)
        context_state = self.context.restrictedTraverse("@@plone_context_state")
        url = context_state.current_page_url()
        return '%s' % (url,)

    @property
    def available(self):
        currency_data = getUtility(ICurrencyData)
        if currency_data.currencies:
            return True
        else:
            return False

    def link_to_currency_converter(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal_url = portal_state.portal_url()
        return '%s/@@currency-converter' % portal_url


#class AddForm(base.AddForm):
#    form_fields = form.Fields(ICurrencyConverterPortlet)
#    label = _(u"Add Currency Converter portlet")
#    description =_(u"This portlet displays currencies where you can check various of currency rates.")

#    def create(self, data):
#        assignment = Assignment()
#        form.applyChanges(assignment, self.form_fields, data)
#        return assignment

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()

#class EditForm(base.EditForm):
#    form_fields = form.Fields(ICurrencyConverterPortlet)
#    label = _(u"Edit Currency Converter portlet")
#    description =_(u"This portlet displays currencies where you can check various of currency rates.")
