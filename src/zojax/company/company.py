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
from zope import interface, component, event
from zope.component import getUtility, queryMultiAdapter
from zope.security.proxy import removeSecurityProxy
from zope.app.intid.interfaces import IIntIds, IIntIdAddedEvent
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.catalog.utils import getRequest
from zojax.richtext.field import RichTextProperty
from zojax.filefield.field import FileFieldProperty
from zojax.members.interfaces import IMembersAware
from zojax.content.type.container import ContentContainer
from zojax.content.type.searchable import ContentSearchableText
from zojax.content.space.interfaces import IWorkspacesManagement
from zojax.content.permissions.utils import updatePermissions
from zojax.permissionsmap.interfaces import IObjectPermissionsMapsManager

from interfaces import ICompany


class Company(ContentContainer):
    interface.implements(ICompany, IMembersAware, IWorkspacesManagement)

    showTabs = True
    showHeader = True
    workspaces = ('overview',)
    enabledWorkspaces = ()
    defaultWorkspace = 'overview'
    type = 'open'

    logo = FileFieldProperty(ICompany['logo'])
    text = RichTextProperty(ICompany['text'])

    @property
    def id(self):
        return getUtility(IIntIds).getId(self)

    @property
    def members(self):
        return self['members']

    def isEnabled(self, workspaceFactory):
        if workspaceFactory.name == 'members':
            return True

        return workspaceFactory.isAvailable() and \
            workspaceFactory.name in self.workspaces


@component.adapter(ICompany, IObjectModifiedEvent)
def companyModified(company, ev):
    if not company.type:
        company.type = u'open'

    IObjectPermissionsMapsManager(
        removeSecurityProxy(company)).set(('company.%s'%company.type,))

    updatePermissions(company)


class CompanySearchableText(ContentSearchableText):
    component.adapts(ICompany)

    def getSearchableText(self):
        text = super(CompanySearchableText, self).getSearchableText()

        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text
