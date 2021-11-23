import transaction
from zope.component import getUtility
from Products.CMFPlone.utils import log
#from Products.CMFCore.utils import getToolByName
from currency.converter.interfaces import ICurrencyData

#def setupVarious(context):
#    
#    # Ordinarily, GenericSetup handlers check for the existence of XML files.
#    # Here, we are not parsing an XML file, but we use this text file as a 
#    # flag to check that we actually meant for this import step to be run.
#    # The file is found in profiles/default.
#    
#    if context.readDataFile('mall.mallcontent_various.txt') is None:
#        return

#    portal = context.getSite()
#    setupGroups(portal)
#    register_shopping_cart_utility(portal)


def removeUtility(portal):
    currency_data = getUtility(ICurrencyData)
    portal.getSiteManager().unregisterUtility(currency_data)
    del currency_data
    transaction.commit()
    log("Uninstalled CurrencyData")


def uninstallVarious(context):

    if context.readDataFile('currency.converter_uninstall.txt') is None:
        return

    portal = context.getSite()
    removeUtility(portal)
