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
from zope.component import getUtility
from zope.dublincore.interfaces import IDCTimes
from zope.index.text.parsetree import ParseError

from zojax.batching.batch import Batch
from zojax.catalog.interfaces import ICatalog
from zojax.filefield.interfaces import IImage
from zojax.ownership.interfaces import IOwnership
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.company.interfaces import _
from zojax.company.types import types


class BrowseCompanies(object):

    batch = Batch((), 15)
    folders = []
    hasGroups = False

    def update(self):
        context = self.context
        request = self.request

        self.hasGroups = bool(len(context))
        if not self.hasGroups:
            return

        if 'form.search.clear' in request:
            self.redirect('./index.html')
            return

        catalog = getUtility(ICatalog)

        if 'form.search' in request:
            s = request.get('form.searchText', u'').strip()
            if s:
                query = {
                    'type': {'any_of': ('content.company',)},
                    'searchContext': (context,),
                    'searchableText': s}

                try:
                    results = catalog.searchResults(**query)
                except ParseError, e:
                    IStatusMessage(request).add(e, 'error')
                    return

                self.batch = Batch(
                    results, size=15, context=context, request=request)
            else:
                IStatusMessage(request).add(
                    _('Please enter one or more words for search.'), 'warning')
            return

        results = catalog.searchResults(
            type = {'any_of': ('content.company',)},
            searchContext = (context,), sort_on='title')
        
        self.folders = catalog.searchResults(
            type = {'any_of': ('companies.folder',)},
            searchContext = (context,), sort_on='title')

        if not results:
            self.hasGroups = False
            return

        self.batch = Batch(results, size=15, context=context, request=request)

    def getGroupInfo(self, company):
        dc = IDCTimes(company)
        principal = getattr(IOwnership(company, None), 'owner', None)

        info = {
            'id': id,
            'title': company.title,
            'description': company.description,
            'owner': principal,
            'created': dc.created,
            'members': len(company['members']),
            'default': not bool(company.logo),
            'type': types.getTerm(company.type)}
        return info
