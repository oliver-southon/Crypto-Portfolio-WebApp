from zope.i18nmessageid import MessageFactory
CurrencyConverterMessageFactory = MessageFactory('currency.converter')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
