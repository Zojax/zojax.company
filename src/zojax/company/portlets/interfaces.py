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
from zope import schema, interface
from zojax.portlet.interfaces import _ as pMsg
from zojax.portlet.interfaces import \
    IPortletManagerWithStatus, ENABLED, statusVocabulary
from zojax.company.interfaces import _


class ICompaniesRightPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.actions','portlet.activity',),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class ICompaniesLeftPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = (),
        required = True)


class ICompanyLeftPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = (),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class ICompanyRightPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.actions',
                   'portlet.comments',),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class ICompanyContentPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.companyoverview',),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class ICompanySearchPortlet(interface.Interface):
    """ company search portlet """


class ICompanyOverviewPortlet(interface.Interface):
    """ company overview portlet """


class ICompanyOverviewContentPortlet(interface.Interface):
    """ company overview portlet """

    showLogo = schema.Bool(
        title = _('Show company logo'),
        default = True,
        required = True)
