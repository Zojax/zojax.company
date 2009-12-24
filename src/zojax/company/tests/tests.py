##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os
import unittest, doctest
from zope import interface, component, event
from zope.app.rotterdam import Rotterdam
from zope.app.testing import functional
from zope.app.component.hooks import setSite
from zope.app.component.site import LocalSiteManager
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.security.interfaces import IAuthentication
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.ownership.interfaces import IOwnerAware, IOwnership
from zojax.authentication.interfaces import IAuthenticationConfiglet
from zojax.portlet.interfaces import IPortletManager, ENABLED
from zope.lifecycleevent import ObjectCreatedEvent
from zope.publisher.browser import TestRequest
from zojax.company.tests.content import Portal
from zojax.personal.space.manager import PersonalSpaceManager, IPersonalSpaceManager


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


zojaxCompany = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxCompany', allow_teardown=True)


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxCompany

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()
        interface.alsoProvides(root, IOwnerAware)

        # IIntIds
        root['ids'] = IntIds()
        sm.registerUtility(root['ids'], IIntIds)
        root['ids'].register(root)

        # catalog
        root['catalog'] = Catalog()
        sm.registerUtility(root['catalog'], ICatalog)

        # auth
        authconfiglet = sm.getUtility(IAuthenticationConfiglet)
        authconfiglet.installUtility()

        auth = sm.getUtility(IAuthentication)
        auth._caching = False

        # portal
        portal = Portal()
        event.notify(ObjectCreatedEvent(portal))
        root['portal'] = portal
        root['portal'].setSiteManager(LocalSiteManager(portal))

        # home folder manager
        manager = PersonalSpaceManager(title=u'People')
        event.notify(ObjectCreatedEvent(manager))

        root['people'] = manager
        sm.registerUtility(root['people'], IPersonalSpaceManager)

        request = TestRequest()
        request.setPrincipal(auth.getPrincipal('zope.mgr'))

        portlets = sm.queryMultiAdapter(
            (portal, TestRequest(), None), IPortletManager, 'columns.left')
        portlets.status = ENABLED
        portlets.portletIds = ('portlet.actions',)

        setSite(None)

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite



def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("./workspace.txt"),
            FunctionalDocFileSuite("./testbrowser.txt"),
            ))
