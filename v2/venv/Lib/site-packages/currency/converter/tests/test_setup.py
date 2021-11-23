import unittest
from Products.CMFCore.utils import getToolByName
from currency.converter.tests.base import CurrencyConverterTestCase
from currency.converter.interfaces import ICurrencyData
from zope.component import queryUtility

class TestSetup(CurrencyConverterTestCase):

    def afterSetUp(self):
        self.types = getToolByName(self.portal, 'portal_types')
        self.properties = getToolByName(self.portal, 'portal_properties')

    ## componentregistry.xml
    def test_utility(self):
        utility = queryUtility(ICurrencyData)
        self.assertNotEquals(None, utility)

    ## Propertiestool.xml
    def test_currency_xml(self):
        self.assertEquals('', self.properties.currency_converter_properties.getProperty('currency_xml'))

#    def test_base_currency(self):
#        self.assertEquals('EUR', self.properties.currency_converter_properties.getProperty('base_currency'))

#    def test_days_for_avarage(self):
#        self.assertEquals(1, self.properties.currency_converter_properties.getProperty('days_for_avarage'))

#    def test_margin_for_avarage(self):
#        self.assertEquals(0, self.properties.currency_converter_properties.getProperty('margin_for_avarage'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
