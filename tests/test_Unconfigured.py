# Copyright (c) 2002 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: test_Unconfigured.py,v 1.1.2.1 2003/07/22 19:02:03 chrisw Exp $

import Zope

from base import SUFBase
from unittest import makeSuite,main

from Products.SimpleUserFolder.SimpleUserFolder import UnconfiguredException

class Tests(SUFBase):

    def test_getUser(self):
        self.assertEqual(self.suf.getUser('test'),None)
    
    def test_getUserNames(self):
        self.assertEqual(self.suf.getUserNames(),[])

    def test__doAddUser(self):
        self.assertRaises(UnconfiguredException,
                          self.suf._doAddUser,
                          'testname',
                          'testpassword',
                          [], # roles
                          '', # domains
                          )

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
        self.assertRaises(UnconfiguredException,
                          self.suf._doChangeUser,
                          'testname',
                          'testpassword',
                          [], # roles
                          '', # domains
                          )

    def test__doDelUsers(self):        
        self.assertRaises(UnconfiguredException,
                          self.suf._doDelUsers,
                          ['test_user'])

def test_suite():
    return makeSuite(Tests)

if __name__=='__main__':
    main(defaultTest='test_suite')
