##
#    Copyright (c) 2007-2011 Cyrus Daboo. All rights reserved.
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#        http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##

# vCard ADR value

import cStringIO as StringIO

from pycalendar import utils

class Adr(object):
    """
    mValue is a tuple of seven str or tuples of str
    """

    (
        POBOX,
        EXTENDED,
        STREET,
        LOCALITY,
        REGION,
        POSTALCODE,
        COUNTRY,
        MAXITEMS
    ) = range(8)

    def __init__(self, value = None):
        self.mValue = value if value else tuple(["" for _ignore in range(Adr.MAXITEMS)])

    def duplicate(self):
        return Adr(self.mValue)

    def __hash__(self):
        return hash(self.mValue)

    def __repr__(self):
        return "ADR %s" % (self.getText(),)

    def __str__(self):
        return self.getText()

    def __eq__( self, comp ):
        return self.mValue == comp.mValue

    def parse(self, data):
        self.mValue = utils.parseDoubleNestedList(data, Adr.MAXITEMS)

    def getText(self):
        os = StringIO.StringIO()
        self.generate(os)
        return os.getvalue()

    def generate(self, os):
        utils.generateDoubleNestedList(os, self.mValue)

    def getValue(self):
        return self.mValue

    def setValue(self, value):
        self.mValue = value
