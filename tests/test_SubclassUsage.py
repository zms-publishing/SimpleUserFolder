# Copyright (c) 2002 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: test_SubclassUsage.py,v 1.1.2.1 2003/07/22 19:02:03 chrisw Exp $

import Zope

from base import UsageBase
from unittest import makeSuite,main
from dummyUserSource import dummyUserFolder

class Tests(UsageBase):

    def _setup(self):
        ob=dummyUserFolder()
        self.folder.manage_delObjects(ids=['acl_users'])
        self.folder._setObject('acl_users', ob)
        self.suf = self.users = self.folder.acl_users

    def test_correctUF(self):
        # test we really have a dummyUserFolder
        assert isinstance(self.suf,dummyUserFolder)
        assert isinstance(self.folder.acl_users,dummyUserFolder)

def test_suite():
    return makeSuite(Tests)

if __name__=='__main__':
    main(defaultTest='test_suite')
