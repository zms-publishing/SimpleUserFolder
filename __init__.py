# Copyright (c) 2002 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: __init__.py,v 1.1.4.2 2003/08/05 17:24:30 chrisw Exp $

from SimpleUserFolder import SimpleUserFolder
from SimpleUserFolder import addSimpleUserFolder

def initialize( context ):
    context.registerClass(SimpleUserFolder,
                          constructors=(addSimpleUserFolder,),
                          icon='www/suf.gif')
