# Copyright (c) 2004 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import Zope

from base import UsageBase
from unittest import makeSuite,main
from dummyUserSource import dummyUserSource

class Tests(UsageBase):

    def _setup(self):
        self.users = dummyUserSource()
        # insert dummyUserSource in aquisition chain
        self.suf = self.suf.aq_base.__of__(
                     self.users.__of__(
                       self.suf.aq_parent
                       )
                     )
        
def test_suite():
    return makeSuite(Tests)

if __name__=='__main__':
    main(defaultTest='test_suite')
