##
#    Copyright (c) 2011 Cyrus Daboo. All rights reserved.
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

from component import PyCalendarComponent
import definitions
import itipdefinitions

class PyCalendarVAvailability(PyCalendarComponent):

    def __init__(self, parent=None):
        super(PyCalendarVAvailability, self).__init__(parent=parent)

    def duplicate(self, parent=None):
        return super(PyCalendarVAvailability, self).duplicate(parent=parent)

    def getType(self):
        return definitions.cICalComponent_VAVAILABILITY

    def getMimeComponentName(self):
        return itipdefinitions.cICalMIMEComponent_VAVAILABILITY

    def finalise(self):
        super(PyCalendarVAvailability, self).finalise()

    def addComponent(self, comp):
        # We can embed the available components only
        if comp.getType() == definitions.cICalComponent_AVAILABLE:
            super(PyCalendarVAvailability, self).addComponent(comp)
        else:
            raise ValueError

    def sortedPropertyKeyOrder(self):
        return (
            definitions.cICalProperty_UID,
            definitions.cICalProperty_DTSTART,
            definitions.cICalProperty_DURATION,
            definitions.cICalProperty_DTEND,
        )
