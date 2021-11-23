import os
import unittest
import doctest
from doctest import DocFileSuite
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName
from currency.converter.tests import base

class TestSetup(base.CurrencyConverterFunctionalTestCase):

    def afterSetUp( self ):
        """Code that is needed is the afterSetUp of both test cases.
        """
        portal = self.portal
        xml = os.path.join(os.path.dirname(__file__), 'sample-90d.xml')
        xml_url = 'file://' + xml
        properties = getToolByName(portal, 'portal_properties')
        properties.currency_converter_properties.currency_xml = xml_url
        # Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)

def test_suite():
    return unittest.TestSuite([
        # Demonstrate the main content types
        ztc.FunctionalDocFileSuite(
            'tests/functional.txt', package='currency.converter',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

#        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'tests/integration.txt', package='currency.converter',
            test_class=base.CurrencyConverterTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        # Unit tests
        DocFileSuite(
            'tests/unittest.txt', package='currency.converter',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
