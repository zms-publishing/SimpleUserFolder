# Copyright (c) 2001 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: SimpleUserFolder.py,v 1.1.2.1 2003/07/22 19:02:03 chrisw Exp $

ManageUsersPermission = 'Manage users'

from AccessControl import ClassSecurityInfo
from AccessControl.User import BasicUserFolder
from Globals import InitializeClass
from Shared.DC.ZRDB.Results import Results
from User import User

def addSimpleUserFolder(self,REQUEST=None):
    """Add a SimpleUserFolder to a container as acl_users"""
    ob=SimpleUserFolder()
    self._setObject('acl_users', ob)
    if REQUEST is not None:
        return self.manage_main(self,REQUEST)

class SimpleUserFolder(BasicUserFolder):

    meta_type="Simple User Folder"

    security = ClassSecurityInfo()

    manage_options=(
        BasicUserFolder.manage_options[0:1]
        + BasicUserFolder.manage_options[2:]
        )

    security.declareProtected(ManageUsersPermission,'getUserNames')
    def getUserNames(self):
        """Return a list of usernames"""
        getUserNames = getattr(self.aq_parent,'getUserNames',None)
        if getUserNames is None:
            return []
        names = getUserNames()
        if isinstance(names,Results):
            # extract names from the multiple rows returned
            names = [n.NAME for n in names]
        return names

    security.declareProtected(ManageUsersPermission,'getUser')
    def getUser(self,name):
        """Return the named user object or None"""
        getUser = getattr(self,'getUserDetails',None)
        if getUser is None:
            return None
        try:
            dict = getUser(name=name)
        except:
            return None
        if not dict:
            return None
        if isinstance(dict,Results):
            # extract roles from the multiple rows returned
            rows = dict
            row = rows[0]
            dict = {
                'name':row.NAME,
                'password':row.PASSWORD
                }
            roles = []
            for row in rows:
                role = row.ROLE
                if role:
                    roles.append(role)
            dict['roles']=roles
        dict['name']=name
        return User(dict)

    security.declareProtected(ManageUsersPermission,'getUser')
    def getUsers(self):
        """Return a list of user objects"""
        return map(self.getUser,self.getUserNames())
        
    def _doAddUser(self, name, password, roles, domains, **kw):
        """Create a new user. The 'password' will be the
           original input password, unencrypted. This
           method is responsible for performing any needed encryption."""
        
        if kw:
            raise ValueError, 'keyword arguments passed to _doAddUser'
        
        if domains:
            raise ValueError, 'Simple User Folder does not support domains'

        addUser = getattr(self,'addUser',None)
        if addUser is None:
            raise UnconfiguredException, 'Addition of users has not been configured'
        
        addUser(name=name,password=password,roles=roles)

    def _doChangeUser(self, name, password, roles, domains, **kw):
        """Modify an existing user. The 'password' will be the
           original input password, unencrypted. The implementation of this
           method is responsible for performing any needed encryption."""

        if kw:
            raise ValueError, 'keyword arguments passed to _doChangeUser'
        
        if domains:
            raise ValueError, 'Simple User Folder does not support domains'

        changeUser = getattr(self,'editUser',None)
        if changeUser is None:
            raise UnconfiguredException, 'Editing of users has not been configured'

        changeUser(name=name,password=password,roles=roles)

    def _doDelUsers(self, names):
        """Delete one or more users."""
        
        delUser = getattr(self,'deleteUser',None)
        if delUser is None:
            raise UnconfiguredException, 'Deleting of users has not been configured'
        
        for name in names:
            delUser(name=name)

InitializeClass(SimpleUserFolder)

class UnconfiguredException (Exception):
    """Exception raised when a SimpleUserFolder needs configuration"""
    pass
