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

from xml.etree.ElementTree import Element
from pycalendar.xmlhelpers import elementToString
from pycalendar.calendar import PyCalendar
import StringIO

import unittest

class TestXMLWrite(unittest.TestCase):
    
    def testGenerate(self):
        
        caldata = """BEGIN:VCALENDAR
CALSCALE:GREGORIAN
PRODID:-//Apple Computer\, Inc//iCal 2.0//EN
VERSION:2.0
BEGIN:VEVENT
UID:C3184A66-1ED0-11D9-A5E0-000A958A3252
DTSTART;VALUE=DATE:20020101
DTEND;VALUE=DATE:20020102
RRULE:FREQ=YEARLY;INTERVAL=1;UNTIL=20031231;BYMONTH=1
SUMMARY:New Year's Day
END:VEVENT
END:VCALENDAR
"""
        pycal = PyCalendar()
        pycal.parse(StringIO.StringIO(caldata))
        root = Element("icalendar")
        pycal.generateXML(root, False)
        print ""
        print elementToString(root)
        