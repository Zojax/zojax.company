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
from zope import interface, component
from zojax.content.type.container import ContentContainer
from zojax.content.space.interfaces import IRootSpace
from zojax.content.space.workspace import WorkspaceFactory

from interfaces import _, ICompanies, ICompaniesFactory


class Companies(ContentContainer):
    interface.implements(ICompanies)


class CompaniesFactory(WorkspaceFactory):
    component.adapts(IRootSpace)
    interface.implements(ICompaniesFactory)

    name = 'companies'
    weight = 99990
    description = _('Container for companies.')
    factory = Companies

    @property
    def title(self):
        if self.isInstalled():
            return self.space['companies'].title
        else:
            return _(u'Companies')
