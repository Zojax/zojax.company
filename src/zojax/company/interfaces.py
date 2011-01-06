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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.widget.list import SimpleList
from zojax.richtext.field import RichText
from zojax.filefield.field import ImageField
from zojax.widget.radio.field import RadioChoice
from zojax.widget.checkbox.field import CheckboxList
from zojax.content.type.interfaces import IItem
from zojax.content.space.interfaces import ISpace, IWorkspace, IWorkspaceFactory

_ = MessageFactory('zojax.company')

import types, vocabulary


class ICompany(ISpace):
    """ company object """

    members = interface.Attribute('IGroupMembers object')

    title = schema.TextLine(
        title = _(u'Company Name'),
        required = True)

    address = SimpleList(
        title = _(u'Address'),
        required = False)

    country = schema.Choice(
        title = _(u'Country'),
        vocabulary = vocabulary.countries,
        required = False)

    text = RichText(
        title = _(u'Text'),
        description = _(u'Company long description.'),
        required = False)

    type = RadioChoice(
        title = _(u'Company type'),
        description = _(u'Select type for this company.'),
        vocabulary = types.types,
        default = 'open',
        required = False)

    logo = ImageField(
        title = _('Logo'),
        description = _('Project logo'),
        maxWidth = 250, maxHeight = 190, scale = True,
        required = False)


class ICompanies(IItem, IWorkspace):
    """ companies workspace """
    

class ICompaniesContainer(IItem):
    """ companies container """
    

class ICompaniesFactory(IWorkspaceFactory):
    """ companies workspace factory """
