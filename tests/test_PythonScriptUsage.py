# Copyright (c) 2002 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: test_PythonScriptUsage.py,v 1.1.2.1 2003/07/22 19:02:03 chrisw Exp $

import Zope
import Globals

from base import UsageBase, test_dir
from unittest import makeSuite,main
from os.path import abspath
from dummyUserSource import dummyUserFolder

from Products.PythonScripts.PythonScript import manage_addPythonScript

def addPythonScript(obj,id):
    f=open(test_dir+'/'+id+'.pys')     
    file=f.read()     
    f.close()     
    manage_addPythonScript(obj,id)
    obj._getOb(id).write(file)
    return getattr(obj,id)     

class Tests(UsageBase):

    def _setup(self):

        f = self.folder
        # config
        addPythonScript(f,'addUser')
        addPythonScript(f,'deleteUser')
        addPythonScript(f,'editUser')
        addPythonScript(f,'getUserDetails')
        addPythonScript(f,'getUserNames')
        self.users = f
        # initial users
        f.addUser('test_user', 'password',[])

def test_suite():
    return makeSuite(Tests)

if __name__=='__main__':
    main(defaultTest='test_suite')
