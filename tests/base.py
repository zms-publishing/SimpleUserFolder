# Copyright (c) 2002 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: base.py,v 1.1.4.2 2003/08/05 17:24:30 chrisw Exp $

import Zope

from unittest import TestCase
from security import PermissiveSecurityPolicy, OmnipotentUser

from Acquisition import aq_base
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from AccessControl.User import UnrestrictedUser
from OFS.Folder import manage_addFolder
from Products.SimpleUserFolder.SimpleUserFolder import addSimpleUserFolder
from Products.SimpleUserFolder.User import User
from os.path import join, abspath, dirname
from os import curdir

class Base(TestCase):

    def setUp( self ):
        get_transaction().begin()
        self._policy = PermissiveSecurityPolicy()
        self._oldPolicy = setSecurityPolicy(self._policy)
        self.connection = Zope.DB.open()
        self.root =  self.connection.root()[ 'Application' ]
        newSecurityManager( None, OmnipotentUser().__of__( self.root ) )
    
    def tearDown( self ):
        get_transaction().abort()
        self.connection.close()
        noSecurityManager()
        setSecurityPolicy(self._oldPolicy)

    def _createFolder(self,creatUserFolder=0):
        root = self.root
        try: root._delObject('suf_test_folder')
        except AttributeError: pass
        root.manage_addFolder('suf_test_folder',
                              createUserF=creatUserFolder)
        f = self.folder = root.suf_test_folder
        return f

class SUFBase(Base):

    def setUp(self):
        Base.setUp(self)
        self._createFolder()
        addSimpleUserFolder(self.folder)
        self.suf = self.folder.acl_users

class UsageBase(SUFBase):

    brain_damaged = 0

    def _setup(self):
        # this method needs to make sure the following
        # attributes are available:
        # self.suf - the user folder, wrapped in any
        #            necessary acquisiton content
        # self.users - a dictionary-ish object that
        #              provides access to the sample users
        raise NotImplemented
        
    def setUp(self):
        SUFBase.setUp(self)
        self._setup()
        
    def test_getUser(self):
        user = self.suf.getUser('test_user')
        self.failUnless(isinstance(user,User))

    def test_getUserNames(self):        
        self.assertEqual(list(self.suf.getUserNames()),['test_user'])

    def test_getUsers(self):
        users = self.suf.getUsers()
        self.assertEqual([user.getUserName() for user in users],
                         ['test_user'])
        self.failUnless(isinstance(users[0],User))
        
    def test__doAddUserWithKW(self):        
        self.assertRaises(ValueError,
                          self.suf._doAddUser,
                          'testname',
                          'testpassword',
                          [], # roles
                          '', # domains
                          x=1,
                          y=2,
                          )

    def test__doAddUserWithDomains(self):        
        self.assertRaises(ValueError,
                          self.suf._doAddUser,
                          'testname',
                          'testpassword',
                          [], # roles
                          'fish', # domains
                          )

    def test__doAddUser(self):
        self.suf._doAddUser(
                          'testname',
                          'testpassword',
                          ['one','two'], # roles
                          [], # domains
                          )
        user = self.users['testname']
        self.assertEqual(user.password,'testpassword')
        self.assertEqual(user.roles,['one','two'])
        # order of names is not ensured
        names = list(self.suf.getUserNames())
        names.sort()
        self.assertEqual(names,['test_user','testname'])
        self.assertEqual(self.suf.getUser('testname').roles,['one','two'])

    def test__doAddUserDuplicate(self):
        self.suf._doAddUser(
                          'testname',
                          'testpassword',
                          ['one','two'], # roles
                          [], # domains
                          )
        try:
            self.suf._doAddUser(
                'testname',
                'testpasswordnot',
                [], # roles
                [], # domains
                )
        except:
            pass
        else:
            # tests can admit their brain damaged, like gadfly
            if not self.brain_damaged:
                self.fail('UserFolder allowed duplicate')

    def test__doChangeUserWithKW(self):        
        self.assertRaises(ValueError,
                          self.suf._doChangeUser,
                          'testname',
                          'testpassword',
                          [], # roles
                          '', # domains
                          x=1,
                          y=2,
                          )

    def test__doChangeUserWithDomains(self):        
        self.assertRaises(ValueError,
                          self.suf._doChangeUser,
                          'testname',
                          'testpassword',
                          [], # roles
                          'fish', # domains
                          )

    def test__doChangeUser(self):        
        self.suf._doChangeUser(
                          'test_user',
                          'newpassword',
                          ['some','roles'], # roles
                          '', # domains
                          )
        user = self.users['test_user']
        self.assertEqual(user.password,'newpassword')
        self.assertEqual(user.roles,['some','roles'])
        self.assertEqual(list(self.suf.getUserNames()),['test_user'])
        self.assertEqual(self.suf.getUser('test_user').roles,['some','roles'])

    def test__doDelUsers(self):        
        self.suf._doDelUsers(['test_user'])
        self.assertRaises(KeyError,self.users.__getitem__,'test_user')
        self.assertEqual(self.suf.getUser('test_user'),None)
    
# where we exist on the file system
try:
    __file__
except NameError:
    # Test was called directly, so no __file__ global exists.
    test_dir = abspath(curdir)
else:
    # Test was called by another test.
    test_dir = abspath(dirname(__file__))

        


