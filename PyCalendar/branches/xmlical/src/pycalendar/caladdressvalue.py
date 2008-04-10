##
#    Copyright (c) 2007 Cyrus Daboo. All rights reserved.
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

# iCalendar UTC Offset value

from plaintextvalue import PyCalendarPlainTextValue
from value import PyCalendarValue
from pycalendar.xmlhelpers import SubElementWithData

class PyCalendarCalAddressValue( PyCalendarPlainTextValue ):

    def getType( self ):
        return PyCalendarValue.VALUETYPE_CALADDRESS

    def generateXML( self, parent ):
        try:
            SubElementWithData(parent, "cal-address", self.mValue )
        except:
            pass

PyCalendarValue.registerType(PyCalendarValue.VALUETYPE_CALADDRESS, PyCalendarCalAddressValue)
