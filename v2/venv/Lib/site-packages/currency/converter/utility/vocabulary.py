from zope.interface import directlyProvides, alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from currency.converter.interfaces import ICurrencyData

def CurrencyVocabularyFactory(context):
    currency_data = getUtility(ICurrencyData)
    if currency_data.currencies != None:
        currency_code_tuples = currency_data.currency_code_tuples()
        items = [SimpleTerm(c[0], c[0], c[1][0]) for c in currency_code_tuples]
        return SimpleVocabulary(items)
    else:
        return False

directlyProvides(CurrencyVocabularyFactory, IVocabularyFactory)

