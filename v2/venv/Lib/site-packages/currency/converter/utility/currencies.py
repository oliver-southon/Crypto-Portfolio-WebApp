from zope.component import getUtility
from zope.interface import implements
from currency.converter.interfaces import (
    ICurrencyCodeDecimal,
    ICurrencyData,
)

class CurrencyCodeDecimal(object):
    """
    A component which provides dictionary of {code:decimal}.
    """

    implements(ICurrencyCodeDecimal)

    def __call__(self):
        """Returns list of dictionaries for currency code and name."""
        currency_data = getUtility(ICurrencyData)
        currency_data_list = currency_data.currency_data_list()
        results = {}
        for i in currency_data_list:
            results.update({i['code']:i['decimal']})
        return results

