from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from Acquisition import aq_inner, aq_chain

from Products.CMFCore.utils import getToolByName

from currency.converter import CurrencyConverterMessageFactory as _

from zope.component import (getMultiAdapter,
                            getUtility)
from currency.converter.interfaces import ICurrencyData

class CurrencyConverterViewlet(ViewletBase):

    render = ViewPageTemplateFile('templates/currency_converter_viewlet.pt')

    def update(self):
#        ## Defines.
        form = self.request.form
        context= aq_inner(self.context)
        context_state = self.context.restrictedTraverse("@@plone_context_state")
        url = context_state.view_url()
        currency_data = getUtility(ICurrencyData)

        self.view_url = '%s/@@currency-converter' % (url,)

        self.currency_data = currency_data.currencies
        self.updated_date = currency_data.updated_date()
        self.currency_code_tuples = currency_data.currency_code_tuples()
        self.days = currency_data.days()
        self.selected_base_currency = currency_data.selected_base_currency
        self.selected_days = currency_data.selected_days
        self.margin = currency_data.margin

        try:
            self.base_currency_rate = form.get('base_currency_rate', 1)
        except:
            self.base_currency_rate = 1
        try:
            self.selected_base_currency_code = form.get('base_currency_code', self.selected_base_currency)
        except:
            self.selected_base_currency_code = self.selected_base_currency
        try:
            self.selected_currency_code = form.get('currency_code', None)
        except:
            self.selected_currency_code = None


        self.calculated_rate = None

        self.error_message = None
        self.float_error_message = None

        ## Check buttons.
        convert_button = form.get('form.button.Convert', None) is not None

        if convert_button:
            if form.get('base_currency_code') != form.get('currency_code'):
                self.base_currency_rate = form.get('base_currency_rate')
                self.base_currency_code = form.get('base_currency_code')
                self.currency_code = form.get('currency_code')
                try:
                    self.calculated_rate = self.calculated_rate_against_base_rate(float(self.base_currency_rate), self.base_currency_code, self.currency_code)
                    return self.render()
                except ValueError:
                    self.float_error_message = _(u"Please input float like 5.00")
                    return self.render()
            else:
                self.error_message =_(u"Please choose different currencies.")
                return self.render()

        else:
            return self.render()

    def calculated_rate_against_base_rate(self, base_currency_rate, base_currency_code, currency_code):
        """Returns calculated rate against base currency rate."""
        currency_data = getUtility(ICurrencyData)
        days = currency_data.selected_days
        margin = currency_data.margin
        currency_dictionary = currency_data.currency_rate_against_base_code_with_margin(days, base_currency_code, margin)
        result = currency_dictionary[currency_code] * base_currency_rate
        return '%.2f' %result
