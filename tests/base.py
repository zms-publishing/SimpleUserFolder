# Copyright (c) 2004 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import Zope

from unittest import TestCase
from security import PermissiveSecurityPolicy, OmnipotentUser

from Acquisition import aq_base
from AccessControl import AuthEncoding
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

    def _setup(self):
        # this method needs to make sure the following
        # attributes are available:
        # self.suf - the user folder, wrapped in any
        #            necessary acquisiton content
        # self.users - a dictionary-ish object that
        #              provides access to the sample users
        # two test users
        #
        # One, with the following:
        # username: 'test_user'
        # password: 'password'
        # roles:    []
        #
        # And the other with:
        # username: 'test_user_with_extras'
        # password: 'password'
        # roles:    []
        # ...and 'extra' attributes as follows:
        # extra1:'extra1value'
        # extra2:2
        raise NotImplementedError
        
    def setUp(self):
        # The try/except is to catch failure here
        # without chewing up ZODB connections
        try:
            SUFBase.setUp(self)
            self._setup()
        except:
            print "Exception during setUp:"
            import sys,traceback
            traceback.print_exception(*sys.exc_info())
        
    ### THE TEST SUITE
        
    def test_getUser(self):
        user = self.suf.getUser('test_user')
        self.failUnless(isinstance(user,User))
        self.assertEqual(user.__,'password')
        self.assertEqual(user.name,'test_user')
        self.assertEqual(user.roles,[])

    def test_getUserWithExtras(self):
        user = self.suf.getUser('test_user_with_extras')
        self.failUnless(isinstance(user,User))
        self.assertEqual(user.__,'password')
        self.assertEqual(user.name,'test_user_with_extras')
        self.assertEqual(user.roles,[])
        self.assertEqual(user['extra1'],'extra1value')
        self.assertEqual(user['extra2'],2)
        # A final check that we get a KeyError
        # if we go for an extra that isn't there
        self.assertRaises(KeyError,user.__getitem__,'extra3')

    def test_getUserNames(self):        
        self.assertEqual(list(self.suf.getUserNames()),['test_user','test_user_with_extras'])

    def test_getUsers(self):
        users = self.suf.getUsers()
        self.assertEqual([user.getUserName() for user in users],
                         ['test_user','test_user_with_extras'])
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
        self.failUnless(AuthEncoding.pw_validate(user.password,'testpassword' ))
        self.assertEqual(user.roles,['one','two'])
        # order of names is not ensured
        names = list(self.suf.getUserNames())
        names.sort()
        self.assertEqual(names,['test_user','test_user_with_extras','testname'])
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
        self.assertEqual(list(self.suf.getUserNames()),['test_user','test_user_with_extras'])
        self.assertEqual(self.suf.getUser('test_user').roles,['some','roles'])

    def test__doChangeUserSamePassword(self):        
        self.suf._doChangeUser(
                          'test_user',
                          None,
                          ['some','roles'], # roles
                          '', # domains
                          )
        user = self.users['test_user']
        self.assertEqual(user.password,'password')
        self.assertEqual(user.roles,['some','roles'])
        self.assertEqual(list(self.suf.getUserNames()),['test_user','test_user_with_extras'])
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

        


