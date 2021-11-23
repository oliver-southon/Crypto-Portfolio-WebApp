from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_currency_converter():
    """Set up the additional products required for currency converter
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for the optilux.policy package.
    # This includes the other products below as well.
    
    fiveconfigure.debug_mode = True
    import currency.converter
    zcml.load_config('configure.zcml', currency.converter)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage('currency.converter')

# The order here is important: We first call the (deferred) function which
# installs the products we need for the currency converter package. Then, we let 
# PloneTestCase set up this product on installation.

setup_currency_converter()
ptc.setupPloneSite(products=['currency.converter'])

class CurrencyConverterTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """

    def afterSetUp( self ):
        """Code that is needed is the afterSetUp of both test cases.
        """

        # Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)

class CurrencyConverterFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
