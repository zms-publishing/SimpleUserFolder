# Copyright (c) 2002 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: test_SQLUsage.py,v 1.1.4.2 2003/08/05 17:24:30 chrisw Exp $

import Zope
import Globals

from base import UsageBase, test_dir
from unittest import makeSuite,main,TestSuite
from os import mkdir
from os.path import abspath, exists, join
from shutil import rmtree
from dummyUserSource import User

from Products.ZSQLMethods.SQL import SQL

def addSQLMethod(obj,id):
    f=open(test_dir+'/'+id+'.sql')     
    data=f.read()     
    f.close()     

    # bits below lifted from FS ZSQL Methods

    # parse parameters
    parameters={}
    start = data.find('<dtml-comment>')
    end   = data.find('</dtml-comment>')
    if start==-1 or end==-1 or start>end:
        raise ValueError,'Could not find parameter block'
    block = data[start+14:end]

    for line in block.split('\n'):
        pair = line.split(':',1)
        if len(pair)!=2:
            continue
        parameters[pair[0].strip().lower()]=pair[1].strip()

    # check for required an optional parameters
    try:            
        title =         parameters.get('title','')
        connection_id = parameters.get('connection id',parameters['connection_id'])
        arguments =     parameters.get('arguments','')
        max_rows =      parameters.get('max_rows',1000)
        max_cache =     parameters.get('max_cache',100)
        cache_time =    parameters.get('cache_time',0)            
    except KeyError,e:
        raise ValueError,"The '%s' parameter is required but was not supplied" % e
        
    s = SQL(id,
            title,
            connection_id,
            arguments,
            data)
    s.manage_advanced(max_rows,
                      max_cache,
                      cache_time,
                      '',
                      '')
    
    obj._setObject(id, s)    
    return getattr(obj,id)     

class SQLUsers:

    def __init__(self,folder):
        self.folder = folder

    def __getitem__(self,name):
        rows = self.folder.getUserDetails(name=name)
        if not rows:
            raise KeyError,name
        password = rows[0].PASSWORD
        roles=[]
        for row in rows:
            role = row.ROLE
            if role:
                roles.append(role)
        return User(password,roles)
        
class Tests(UsageBase):

    # gadfly can't make a column only allow unique values
    brain_damaged = 1
    
    def _setup(self):
        
        f = self.folder
        # create test Gadfly DB
        gf_dir = join(Globals.data_dir,'gadfly')
        if not exists(gf_dir):
            mkdir(gf_dir)
        self.gf_dir = gf_dir = join(gf_dir,'suftests')
        if exists(gf_dir):
            # uh oh, lets not stomp on this db we know nothing about
            raise RuntimeError,"'suftests' gadfly database already exists!"
        mkdir(gf_dir)
        
        # add DB Connection
        f.manage_addZGadflyConnection(id='sufdb',
                                      title='',
                                      connection='suftests',
                                      check='yes')
        # create tables
        addSQLMethod(f,'createTables')
        f.createTables()
        
        # methods
        addSQLMethod(f,'addUser')
        addSQLMethod(f,'deleteUser')
        addSQLMethod(f,'editUser')
        addSQLMethod(f,'getUserDetails')
        addSQLMethod(f,'getUserNames')
        
        # initial users
        f.addUser(name='test_user',password='password',roles=[])

        self.users = SQLUsers(f)

    def tearDown(self):
        UsageBase.tearDown(self)
        rmtree(self.gf_dir)
        
def test_suite():
    return makeSuite(Tests)

if __name__=='__main__':
    main(defaultTest='test_suite')
