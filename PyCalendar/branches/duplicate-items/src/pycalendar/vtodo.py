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

import cStringIO as StringIO

from component import PyCalendarComponent
from componentrecur import PyCalendarComponentRecur
from datetime import PyCalendarDateTime
from property import PyCalendarProperty
import definitions
import itipdefinitions

class PyCalendarVToDo(PyCalendarComponentRecur):

    OVERDUE = 0

    DUE_NOW= 1

    DUE_LATER = 2

    DONE = 3

    CANCELLED= 4

    sBeginDelimiter = definitions.cICalComponent_BEGINVTODO

    sEndDelimiter = definitions.cICalComponent_ENDVTODO

    @staticmethod
    def getVBegin():
        return PyCalendarVToDo.sBeginDelimiter

    @staticmethod
    def getVEnd():
        return PyCalendarVToDo.sEndDelimiter

    @staticmethod
    def sort_for_display(e1, e2):
        s1 = e1.getMaster()
        s2 = e2.getMaster()

        # Check status first (convert None -> Needs action for tests)
        status1 = s1.self.mStatus
        status2 = s2.self.mStatus
        if status1 == definitions.eStatus_VToDo_None:
            status1 = definitions.eStatus_VToDo_NeedsAction
        if status2 == definitions.eStatus_VToDo_None:
            status2 = definitions.eStatus_VToDo_NeedsAction
        if status1 != status2:
            # More important ones at the top
            return status1 < status2

        # At this point the status of each is the same

        # If status is cancelled sort by start time
        if s1.self.mStatus == definitions.eStatus_VToDo_Cancelled:
            # Older ones at the bottom
            return s1.mStart > s2.mStart

        # If status is completed sort by completion time
        if s1.self.mStatus == definitions.eStatus_VToDo_Completed:
            # Older ones at the bottom
            return s1.self.mCompleted > s2.self.mCompleted

        # Check due date exists
        if s1.mHasEnd != s2.mHasEnd:
            now = PyCalendarDateTime()
            now.setToday()

            # Ones with due dates after today below ones without due dates
            if s1.hasEnd():
                return s1.mEnd <= now
            elif s2.hasEnd():
                return now < s2.mEnd

        # Check due dates if present
        if s1.mHasEnd:
            if s1.mEnd != s2.mEnd:
                # Soonest dues dates above later ones
                return s1.mEnd < s2.mEnd

        # Check priority next
        if s1.self.mPriority != s2.self.mPriority:
            # Higher priority above lower ones
            return s1.self.mPriority < s2.self.mPriority

        # Just use start time - older ones at the top
        return s1.mStart < s2.mStart

    def __init__(self, calendar):
        super(PyCalendarVToDo, self).__init__(calendar=calendar)
        self.mPriority = 0
        self.mStatus = definitions.eStatus_VToDo_None
        self.mPercentComplete = 0
        self.mCompleted = PyCalendarDateTime()
        self.mHasCompleted = False

    def duplicate(self, calendar):
        other = super(PyCalendarVToDo, self).duplicate(calendar)
        other.mPriority = self.mPriority
        other.mStatus = self.mStatus
        other.mPercentComplete = self.mPercentComplete
        other.mCompleted = self.mCompleted.duplicate()
        other.mHasCompleted = self.mHasCompleted
        return other

    def getType(self):
        return PyCalendarComponent.eVTODO

    def getBeginDelimiter(self):
        return PyCalendarVToDo.sBeginDelimiter

    def getEndDelimiter(self):
        return PyCalendarVToDo.sEndDelimiter

    def getMimeComponentName(self):
        return itipdefinitions.cICalMIMEComponent_VTODO

    def addComponent(self, comp):
        # We can embed the alarm components only
        if comp.getType() == PyCalendarComponent.eVALARM:
            if self.mEmbedded is None:
                self.mEmbedded = []
            self.mEmbedded.append(comp)
            comp.setEmbedder(self)
            return True
        else:
            return False

    def getStatus(self):
        return self.mStatus

    def setStatus(self, status):
        self.mStatus = status

    def getStatusText(self):
        sout = StringIO()

        if self.mStatus in (definitions.eStatus_VToDo_NeedsAction, definitions.eStatus_VToDo_InProcess):
            if self.hasEnd():
                # Check due date
                today = PyCalendarDateTime()
                today.setToday()
                if self.getEnd() > today:
                    sout.append("Due: ")
                    whendue = self.getEnd() - today
                    if (whendue.getDays() > 0) and (whendue.getDays() <= 7):
                        sout.write(whendue.getDays())
                        sout.write(" days")
                    else:
                        sout.write(self.getEnd().getLocaleDate(PyCalendarDateTime.NUMERICDATE))
                elif self.getEnd() == today:
                    sout.write("Due today")
                else:
                    sout.write("Overdue: ")
                    overdue = today - self.getEnd()
                    if overdue.getWeeks() != 0:
                        sout.write(overdue.getWeeks())
                        sout.write(" weeks")
                    else:
                        sout.write(overdue.getDays() + 1)
                        sout.write(" days")
            else:
                sout.write("Not Completed")
        elif self.mStatus == definitions.eStatus_VToDo_Completed:
            if self.hasCompleted():
                sout.write("Completed: ")
                sout.write(self.getCompleted().getLocaleDate(PyCalendarDateTime.NUMERICDATE))
            else:
                sout.write("Completed")
        elif definitions.eStatus_VToDo_Cancelled:
            sout.write("Cancelled")

        return sout.toString()

    def getCompletionState(self):
        if self.mStatus in (definitions.eStatus_VToDo_NeedsAction, definitions.eStatus_VToDo_InProcess):
            if self.hasEnd():
                # Check due date
                today = PyCalendarDateTime()
                today.setToday()
                if self.getEnd() > today:
                    return PyCalendarVToDo.DUE_LATER
                elif self.getEnd() == today:
                    return PyCalendarVToDo.DUE_NOW
                else:
                    return PyCalendarVToDo.OVERDUE
            else:
                return PyCalendarVToDo.DUE_NOW
        elif self.mStatus == definitions.eStatus_VToDo_Completed:
            return PyCalendarVToDo.DONE
        elif self.mStatus == definitions.eStatus_VToDo_Cancelled:
            return PyCalendarVToDo.CANCELLED

    def getPriority(self):
        return self.mPriority

    def setPriority(self, priority):
        self.mPriority = priority

    def getCompleted(self):
        return self.mCompleted

    def hasCompleted(self):
        return self.mHasCompleted

    def finalise(self):
        # Do inherited
        super(PyCalendarVToDo, self).finalise()

        # Get DUE
        temp = self.loadValueDateTime(definitions.cICalProperty_DUE)
        if temp is None:
            # Try DURATION instead
            temp = self.loadValueDuration(definitions.cICalProperty_DURATION)
            if temp is not None:
                self.mEnd = self.mStart + temp
                self.mHasEnd = True
            else:
                self.mHasEnd = False
        else:
            self.mHasEnd = True
            self.mEnd = temp

        # Get PRIORITY
        self.mPriority = self.loadValueInteger(definitions.cICalProperty_PRIORITY)

        # Get STATUS
        temp = self.loadValueString(definitions.cICalProperty_STATUS)
        if temp is not None:
            if temp == definitions.cICalProperty_STATUS_NEEDS_ACTION:
                self.mStatus = definitions.eStatus_VToDo_NeedsAction
            elif temp == definitions.cICalProperty_STATUS_COMPLETED:
                self.mStatus = definitions.eStatus_VToDo_Completed
            elif temp == definitions.cICalProperty_STATUS_IN_PROCESS:
                self.mStatus = definitions.eStatus_VToDo_InProcess
            elif temp == definitions.cICalProperty_STATUS_CANCELLED:
                self.mStatus = definitions.eStatus_VToDo_Cancelled

        # Get PERCENT-COMPLETE
        self.mPercentComplete = self.loadValueInteger(definitions.cICalProperty_PERCENT_COMPLETE)

        # Get COMPLETED
        temp = self.loadValueDateTime(definitions.cICalProperty_COMPLETED)
        self.mHasCompleted = temp is not None
        if self.mHasCompleted:
            self.mCompleted = temp

    # Editing
    def editStatus(self, status):
        # Only if it is different
        if self.mStatus != status:
            # Updated cached values
            self.mStatus = status

            # Remove existing STATUS & COMPLETED items
            self.removeProperties(definitions.cICalProperty_STATUS)
            self.removeProperties(definitions.cICalProperty_COMPLETED)
            self.mHasCompleted = False

            # Now create properties
            value = None
            if status == definitions.eStatus_VToDo_NeedsAction:
                value = definitions.cICalProperty_STATUS_NEEDS_ACTION
            if status == definitions.eStatus_VToDo_Completed:
                value = definitions.cICalProperty_STATUS_COMPLETED
                # Add the completed item
                self.mCompleted.setNowUTC()
                self.mHasCompleted = True
                prop = PyCalendarProperty(definitions.cICalProperty_STATUS_COMPLETED, self.mCompleted)
                self.addProperty(prop)
            elif status == definitions.eStatus_VToDo_InProcess:
                value = definitions.cICalProperty_STATUS_IN_PROCESS
            elif status == definitions.eStatus_VToDo_Cancelled:
                value = definitions.cICalProperty_STATUS_CANCELLED
            prop = PyCalendarProperty(definitions.cICalProperty_STATUS, value)
            self.addProperty(prop)

    def editCompleted(self, completed):
        # Remove existing COMPLETED item
        self.removeProperties(definitions.cICalProperty_COMPLETED)
        self.mHasCompleted = False

        # Always UTC
        self.mCompleted = completed.duplicate()
        self.mCompleted.adjustToUTC()
        self.mHasCompleted = True
        prop = PyCalendarProperty(definitions.cICalProperty_STATUS_COMPLETED, self.mCompleted)
        self.addProperty(prop)
