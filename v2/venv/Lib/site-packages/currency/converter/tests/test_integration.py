import os
import unittest
import doctest
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName
from currency.converter.tests import base

class CurrencyConverterIntegrationTestCase(base.CurrencyConverterTestCase):
    """Base class used for test cases
    """

    def afterSetUp( self ):
        """Code that is needed is the afterSetUp of both test cases.
        """
        ## Set up sessioning objects
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        portal = self.portal
#        tail = ['currency.converter', 'currency', 'converter', 'tests', 'sample-90d.xml']
#        current_path_list = os.path.dirname(__file__).split('/')
#        ind = current_path_list.index('src')
#        path_list = current_path_list[:1+ind]
#        path_list.extend(tail)
#        path = '/'.join(path_list)
#        xml_url = 'file://' + path
#        properties = getToolByName(portal, 'portal_properties')
#        properties.currency_converter_properties.currency_xml = xml_url
        xml = os.path.join(os.path.dirname(__file__), 'sample-90d.xml')
        xml_url = 'file://' + xml
        properties = getToolByName(portal, 'portal_properties')
        properties.currency_converter_properties.currency_xml = xml_url


def test_suite():
    return unittest.TestSuite([

        # Integration tests for adapters of MallShop Content Type.
        ztc.ZopeDocFileSuite(
            'tests/integration/adapters_integration.txt', package='currency.converter',
            test_class=CurrencyConverterIntegrationTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),


            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
