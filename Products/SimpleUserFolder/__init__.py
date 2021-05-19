# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

# VERY IMPORTANT HINT:
# Copyright (c) 2021 SNTL Publishing GmbH & Co KG
# This is just a dysfunctional fake product based on the
# Simplistix SimpleUserFolder to avoid destructive GUI effects
# of lost SimpleUserFolder instances after updating to Python3/Zope5.
# It's only purpose is to be able to delete forgotten instances
# with the Zope-GUI.

from AccessControl import ClassSecurityInfo
from AccessControl.User import BasicUserFolder
from AccessControl.class_init import InitializeClass
from OFS.ObjectManager import ObjectManager
from Shared.DC.ZRDB.Results import Results
from sys import exc_info
from AccessControl.users import User

ManageUsersPermission = 'Manage users'
ViewManagementPermission = 'View management screens'

def addSimpleUserFolder(self,REQUEST=None):
    return None

def initialize( context ):
    context.registerClass(SimpleUserFolder,
                          constructors=(addSimpleUserFolder,),
                          )


class SimpleUserFolder(ObjectManager,BasicUserFolder):
    '''Just a dummy class to provide a view of the class'''
    security = ClassSecurityInfo()
    meta_type='Simple User Folder'
    zmi_icon = 'fas fa-users text-danger'

    def getUser():
        return None

    def getUsers(self):
        return []

    def getUserNames(self):
        return []

InitializeClass(SimpleUserFolder)