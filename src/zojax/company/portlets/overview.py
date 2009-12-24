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
from zope.dublincore.interfaces import IDCTimes

from zojax.company.types import types
from zojax.company.interfaces import ICompany
from zojax.members.interfaces import IMembersAware
from zojax.ownership.interfaces import IOwnership


class CompanyOverviewPortlet(object):

    def getContext(self):
        context = self.context

        while not ICompany.providedBy(context):
            context = context.__parent__
            if context is None:
                return

        return context

    def getProjectInfo(self):
        context = self.getContext()

        dc = IDCTimes(context)
        principal = getattr(IOwnership(context, None), 'owner', None)

        info = {
            'title': context.title,
            'description': context.description,
            'owner': principal,
            'created': dc.created,
            'members': None,
            'default': not bool(context.logo),
            'type': types.getTerm(context.type),
            'company': context}

        if IMembersAware.providedBy(context):
            info['members'] = len(context.members)

        return info

    def isAvailable(self):
        return self.getContext() is not None
