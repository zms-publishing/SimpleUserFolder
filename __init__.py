# Copyright (c) 2002 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: __init__.py,v 1.1.2.1 2003/07/22 19:02:03 chrisw Exp $

from SimpleUserFolder import SimpleUserFolder
from SimpleUserFolder import addSimpleUserFolder

def initialize( context ):
    context.registerClass(SimpleUserFolder,
                          constructors=(addSimpleUserFolder,),
                          icon='www/suf.gif')
