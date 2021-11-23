import warnings
from datetime import datetime
from persistent import Persistent
from zope.interface import implements
from currency.converter.interfaces import (
                                            ICurrencyData,
                                            IRateAgainstBaseRate,
                                            ICurrencyCodeName,
                                            ICurrencyCodeNameTuples,
                                            )
from elementtree.ElementTree import ElementTree
import urllib2
from currencies import currencies
from zope.component import getUtility

class CurrencyData(Persistent):
    implements(ICurrencyData)

    def __init__(self):
        self.currencies = None
        self.selected_base_currency = "EUR"
        self.selected_days = 1
        self.margin = 0.00
        self.date = None
        self.codes = ['EUR']
        self.amount_of_days = [1]

    def currency_data(self, xml_url='http://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'):
        """Returns the most recent currency data with tuples."""
        now = datetime.now()
        today = u'-'.join([unicode(now.year), unicode(now.month), unicode(now.day)])
        if today == self.updated_date():
            return
        etree90 = ElementTree()
        try:
            data90 = urllib2.urlopen(xml_url)
            root90 = ElementTree.parse(etree90, data90)
            DATA90 = root90[2]
            DATA_list = []
            for DATA in DATA90:
                daily_data_list = []
                for daily_data in DATA:
                    daily_data_tuple = (daily_data.get('currency'), daily_data.get('rate'))
                    daily_data_list.append(daily_data_tuple)
                ddl = (DATA.get('time'), dict(daily_data_list))
                DATA_list.append(ddl)
                date = DATA_list[0][0]
            try:
                if self.date != date:
                    self.currencies = DATA_list
                    self.date = date
                    for date in self.currencies:
                        for key in date[1].keys():
                            if key not in self.codes:
                                self.codes.append(key)
                    self.amount_of_days = range(1,len(self.currencies)+1)
            except AttributeError:
                self.currencies = DATA_list
        except:
            pass

    def currency_data_list(self):
        """Returns the most recent currency data as a list of dictionaries.
        ex)
        [
            {
            code: "EUR",
            rate: ['156.05', '160.25', ...],
            name: u"Euro",
            unit: u"\u20ac"
            },
            {...},{...},...
        ]
        """
        if self.currencies is not None:
            daily_data_list = [daily_data[1] for daily_data in self.currencies]
            results = []
            for code in self.currency_codes():
                rate_list = [d.get(code) for d in daily_data_list if d.get(code) != None]
                try:
                    if code == "EUR":
                        results.append(
                    {
                    'code': code, 
                    'rate': [1],
                    'name': currencies.get(code)[0],
                    'unit': currencies.get(code)[1],
                    'decimal' : currencies.get(code)[2],
                    }
                    )
                    else:
                        results.append(
                    {
                    'code': code, 
                    'rate': rate_list,
                    'name': currencies.get(code)[0],
                    'unit': currencies.get(code)[1],
                    'decimal' : currencies.get(code)[2],
                    }
                    )
                except:
                    results.append(
                    {
                    'code': code, 
                    'rate': rate_list,
                    'name': currencies.get(code)[0],
                    'unit': currencies.get(code)[1],
                    'decimal' : 2,
                    }
                    )
            return results
        else:
            return False

    def updated_date(self):
        """Returns updated date."""
        warnings.warn(
            ("'update_date' is deprecated and will be removed"),
            DeprecationWarning
        )
        if self.currencies != None:
            return self.currencies[0][0]
        else:
            return False

    def currency_codes(self):
        """Retrurns currency codes."""
        warnings.warn(
            ("'update_date' is deprecated and will be removed"),
            DeprecationWarning
        )
        codes = ['EUR']
        if self.currencies is not None:
            for date in self.currencies:
                for key in date[1].keys():
                    if key not in codes:
                        codes.append(key)
        return codes

    def currency_code_tuples(self):
        """Returns currency code and its tuples."""
        results = []
        for code in self.currency_codes():
            t = (code, currencies[code])
            results.append(t)
        return results

    def currency_code_data(self):
        """Returns dictionary of currency code and rate list."""
        if self.currencies is not None:
            currency_data_withought_date = []
            for data in self.currencies:
                currency_data_withought_date.append(data[1])
            r = {}
            for code in self.currency_codes():
                results = []
                for data in currency_data_withought_date:
                    for key in data.keys():
                        if code == key:
                            results.append(data[key])
                r.update({code:results})
            return r
        else:
            return False

    def currency_code_average(self, days):
        """Returns code and average rate of days."""
        if self.currencies is not None:
            results = {}
            for (code, L) in self.currency_code_data().items():
                if code == 'EUR':
                    rate = 1
                    results.update({code:rate})
                elif len(L) >= days > 0:
                    L = L[0:days]
                    S = 0
                    for l in L:
                        S = S + float(l)
                    rate = S / days
                    results.update({code:rate})
                elif days > len(L) > 0:
                    S = 0
                    for l in L:
                        S = S + float(l)
                    rate = S / len(L)
                    results.update({code:rate})
                else:
                    pass
            return results
        else:
            return False

    def days(self):
        """Returns maximum gotten days."""
        warnings.warn(
            ("'update_date' is deprecated and will be removed"),
            DeprecationWarning
        )
        if self.currencies is not None:
            return range(1,len(self.currencies)+1)
        else:
            return [1]

    def currency_rate_against_base_code(self, days, code):
        """Returns currency rate gainst base code."""
        if self.currencies != None:
            if code == "EUR":
                cca = self.currency_code_average(days)
                del cca[code]
                return cca
            else:
                cca = self.currency_code_average(days)
                code_value = float(cca[code])
                del cca[code]
                results = {}
                for (k, v) in cca.items():
                    v = float(v) / code_value
                    results.update({k:v})
                return results
        else:
            return False

    def currency_rate_against_base_code_with_margin(self, days, code, margin):
        """Returns currency rate gainst base code with margin."""
        if self.currencies != None:
            results = {}
            for (k, v) in self.currency_rate_against_base_code(days, code).items():
                v = v * (100 + margin) / 100
                results.update({k:v})
            return results
        else:
            return False

    def currency_rate(self, days=1, margin=0, base_currency_code="EUR", base_rate=1, currency_code="USD", currency_rate=10):
        """Returns calculated currency rate."""
        if base_currency_code == "EUR":
            for cd in self.currency_data_list():
                if cd['code'] == currency_code:
                    rates = cd['rate']
                    decimal = cd['decimal']
                    break


class RateAgainstBaseRate(object):
    """A component which provides rate agains base currency rate."""

    implements(IRateAgainstBaseRate)

    def __call__(self, base_currency_rate, base_currency_code, currency_code):
        """Returns currency rate for base currency rate, margin and days."""
        currency_data = getUtility(ICurrencyData)
        days = currency_data.selected_days
        margin = currency_data.margin
        currency_dictionary = currency_data.currency_rate_against_base_code_with_margin(days, base_currency_code, margin)
#        if currency_code == None:
#            return None
#        if currency_code == '':
#            return None
#        elif base_currency_code != currency_code:
#            result = currency_dictionary[currency_code] * base_currency_rate
#            return '%.2f' %result
#        else:
#            return None
        if self.in_float(base_currency_rate, base_currency_code, currency_code) is not None:
            result = currency_dictionary[currency_code] * base_currency_rate
            return '%.2f' %result
        else:
            return None

    def in_float(self, base_currency_rate, base_currency_code, currency_code):
        currency_data = getUtility(ICurrencyData)
        days = currency_data.selected_days
        margin = currency_data.margin
        currency_dictionary = currency_data.currency_rate_against_base_code_with_margin(days, base_currency_code, margin)
        if currency_code == None:
            return None
        if currency_code == '':
            return None
        elif base_currency_code != currency_code:
            return currency_dictionary[currency_code] * base_currency_rate
        else:
            return None

class CurrencyCodeName(object):
    """
    A component which provides list of dictionaries for currency code and name.
    """

    implements(ICurrencyCodeName)

    def __call__(self):
        """Returns list of dictionaries for currency code and name."""
        currency_data = getUtility(ICurrencyData)
        currency_data_list = currency_data.currency_data_list()
        return [{'code':i['code'],'name':i['name']} for i in currency_data_list]

class CurrencyCodeNameTuples(object):

    implements(ICurrencyCodeNameTuples)

    def __call__(self):
        """Returns tuple of tuples for currency code and name."""
        currency_data = getUtility(ICurrencyData)
        currency_data_list = currency_data.currency_data_list()
        l = [(i['code'],i['name']) for i in currency_data_list]
        t = tuple(l)
        return t
