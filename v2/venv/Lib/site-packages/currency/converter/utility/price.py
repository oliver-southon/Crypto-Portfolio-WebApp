from decimal import Decimal, ROUND_HALF_UP
from zope.interface import implements
from currency.converter.interfaces import IDecimalPrice

class DecimalPrice(object):
    implements(IDecimalPrice)
    def __call__(self, price, number_of_decimal_places=2):
        if price is None:
            return None
        if type(price).__name__ == 'float':
            price = str(price)
        if number_of_decimal_places == 2:
            price = Decimal(price).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)
            price = Decimal(price).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            return price
        if number_of_decimal_places == 0:
            price = Decimal(price).quantize(Decimal('.1'), rounding=ROUND_HALF_UP)
            price = Decimal(price).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            return price
        else:
            try:
                raise DecimalPlaceError(number_of_decimal_places)
            except DecimalPlaceError as e:
                text = '%s is not valid number. Use either 0 or 2.' %(e.value)
                print text

class DecimalPlaceError(Exception):

    def __init__(self, number_of_decimal_places):
        self.value = number_of_decimal_places

    def __str__(self):
        return repr(self.value)

