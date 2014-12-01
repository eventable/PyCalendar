##
#    Copyright (c) 2007-2013 Cyrus Daboo. All rights reserved.
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

from pycalendar.datetime import DateTime
from pycalendar.icalendar.calendar import Calendar
from pycalendar.timezone import Timezone
import unittest

class TestCalendar(unittest.TestCase):

    def testOffsets(self):

        data = (
            (
                """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:-//calendarserver.org//Zonal//EN
BEGIN:VTIMEZONE
TZID:America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:STANDARD
DTSTART:18831118T120358
RDATE:18831118T120358
TZNAME:EST
TZOFFSETFROM:-045602
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19180331T020000
RRULE:FREQ=YEARLY;UNTIL=19190330T070000Z;BYDAY=-1SU;BYMONTH=3
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19181027T020000
RRULE:FREQ=YEARLY;UNTIL=19191026T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:STANDARD
DTSTART:19200101T000000
RDATE:19200101T000000
RDATE:19420101T000000
RDATE:19460101T000000
RDATE:19670101T000000
TZNAME:EST
TZOFFSETFROM:-0500
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19200328T020000
RDATE:19200328T020000
RDATE:19740106T020000
RDATE:19750223T020000
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19201031T020000
RDATE:19201031T020000
RDATE:19450930T020000
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19210424T020000
RRULE:FREQ=YEARLY;UNTIL=19410427T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19210925T020000
RRULE:FREQ=YEARLY;UNTIL=19410928T060000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19420209T020000
RDATE:19420209T020000
TZNAME:EWT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19450814T190000
RDATE:19450814T190000
TZNAME:EPT
TZOFFSETFROM:-0400
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19460428T020000
RRULE:FREQ=YEARLY;UNTIL=19660424T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19460929T020000
RRULE:FREQ=YEARLY;UNTIL=19540926T060000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:STANDARD
DTSTART:19551030T020000
RRULE:FREQ=YEARLY;UNTIL=19661030T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19670430T020000
RRULE:FREQ=YEARLY;UNTIL=19730429T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19671029T020000
RRULE:FREQ=YEARLY;UNTIL=20061029T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19760425T020000
RRULE:FREQ=YEARLY;UNTIL=19860427T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19870405T020000
RRULE:FREQ=YEARLY;UNTIL=20060402T070000Z;BYDAY=1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:20070311T020000
RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:20071104T020000
RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
END:VTIMEZONE
END:VCALENDAR
""",
                (
                    (DateTime(1942, 2, 8), False, -5),
                    (DateTime(1942, 2, 10), False, -4),
                    (DateTime(2011, 1, 1), False, -5),
                    (DateTime(2011, 4, 1), False, -4),
                    (DateTime(2011, 10, 24), False, -4),
                    (DateTime(2011, 11, 8), False, -5),
                    (DateTime(2006, 1, 1), False, -5),
                    (DateTime(2006, 4, 1), False, -5),
                    (DateTime(2006, 5, 1), False, -4),
                    (DateTime(2006, 10, 1), False, -4),
                    (DateTime(2006, 10, 24), False, -4),
                    (DateTime(2006, 11, 8), False, -5),
                    (DateTime(2014, 3, 8, 23, 0, 0), False, -5),
                    (DateTime(2014, 3, 9, 0, 0, 0), False, -5),
                    (DateTime(2014, 3, 9, 3, 0, 0), False, -4),
                    (DateTime(2014, 3, 9, 8, 0, 0), False, -4),
                    (DateTime(2014, 3, 8, 23, 0, 0), True, -5),
                    (DateTime(2014, 3, 9, 0, 0, 0), True, -5),
                    (DateTime(2014, 3, 9, 3, 0, 0), True, -5),
                    (DateTime(2014, 3, 9, 8, 0, 0), True, -4),
                    (DateTime(2014, 11, 1, 23, 0, 0), False, -4),
                    (DateTime(2014, 11, 2, 0, 0, 0), False, -4),
                    (DateTime(2014, 11, 2, 3, 0, 0), False, -5),
                    (DateTime(2014, 11, 2, 8, 0, 0), False, -5),
                    (DateTime(2014, 11, 1, 23, 0, 0), True, -4),
                    (DateTime(2014, 11, 2, 0, 0, 0), True, -4),
                    (DateTime(2014, 11, 2, 3, 0, 0), True, -4),
                    (DateTime(2014, 11, 2, 8, 0, 0), True, -5),
                )
            ),
            (
                """BEGIN:VCALENDAR
CALSCALE:GREGORIAN
PRODID:-//calendarserver.org//Zonal//EN
VERSION:2.0
BEGIN:VTIMEZONE
TZID:Etc/GMT+8
X-LIC-LOCATION:Etc/GMT+8
BEGIN:STANDARD
DTSTART:18000101T000000
RDATE:18000101T000000
TZNAME:GMT+8
TZOFFSETFROM:-0800
TZOFFSETTO:-0800
END:STANDARD
END:VTIMEZONE
END:VCALENDAR
""",
                (
                    (DateTime(1942, 2, 8), False, -8),
                    (DateTime(1942, 2, 10), False, -8),
                    (DateTime(2011, 1, 1), False, -8),
                    (DateTime(2011, 4, 1), False, -8),
                )
            ),
        )

        for tzdata, offsets in data:

            cal = Calendar.parseText(tzdata.replace("\n", "\r\n"))
            tz = cal.getComponents()[0]

            for dt, relative_to_utc, offset in offsets:
                tzoffset = tz.getTimezoneOffsetSeconds(dt, relative_to_utc)
                self.assertEqual(tzoffset, offset * 60 * 60, "Failed to match offset for %s at %s with caching" % (tz.getID(), dt,))
            for dt, relative_to_utc, offset in reversed(offsets):
                tzoffset = tz.getTimezoneOffsetSeconds(dt, relative_to_utc)
                self.assertEqual(tzoffset, offset * 60 * 60, "Failed to match offset for %s at %s with caching, reversed" % (tz.getID(), dt,))

            for dt, relative_to_utc, offset in offsets:
                tz.mCachedExpandAllMax = None
                tzoffset = tz.getTimezoneOffsetSeconds(dt, relative_to_utc)
                self.assertEqual(tzoffset, offset * 60 * 60, "Failed to match offset for %s at %s without caching" % (tz.getID(), dt,))
            for dt, relative_to_utc, offset in reversed(offsets):
                tz.mCachedExpandAllMax = None
                tzoffset = tz.getTimezoneOffsetSeconds(dt, relative_to_utc)
                self.assertEqual(tzoffset, offset * 60 * 60, "Failed to match offset for %s at %s without caching, reversed" % (tz.getID(), dt,))


    def testConversions(self):

        tzdata = """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:-//calendarserver.org//Zonal//EN
BEGIN:VTIMEZONE
TZID:America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:STANDARD
DTSTART:18831118T120358
RDATE:18831118T120358
TZNAME:EST
TZOFFSETFROM:-045602
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19180331T020000
RRULE:FREQ=YEARLY;UNTIL=19190330T070000Z;BYDAY=-1SU;BYMONTH=3
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19181027T020000
RRULE:FREQ=YEARLY;UNTIL=19191026T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:STANDARD
DTSTART:19200101T000000
RDATE:19200101T000000
RDATE:19420101T000000
RDATE:19460101T000000
RDATE:19670101T000000
TZNAME:EST
TZOFFSETFROM:-0500
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19200328T020000
RDATE:19200328T020000
RDATE:19740106T020000
RDATE:19750223T020000
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19201031T020000
RDATE:19201031T020000
RDATE:19450930T020000
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19210424T020000
RRULE:FREQ=YEARLY;UNTIL=19410427T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19210925T020000
RRULE:FREQ=YEARLY;UNTIL=19410928T060000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19420209T020000
RDATE:19420209T020000
TZNAME:EWT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19450814T190000
RDATE:19450814T190000
TZNAME:EPT
TZOFFSETFROM:-0400
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19460428T020000
RRULE:FREQ=YEARLY;UNTIL=19660424T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19460929T020000
RRULE:FREQ=YEARLY;UNTIL=19540926T060000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:STANDARD
DTSTART:19551030T020000
RRULE:FREQ=YEARLY;UNTIL=19661030T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19670430T020000
RRULE:FREQ=YEARLY;UNTIL=19730429T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19671029T020000
RRULE:FREQ=YEARLY;UNTIL=20061029T060000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19760425T020000
RRULE:FREQ=YEARLY;UNTIL=19860427T070000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19870405T020000
RRULE:FREQ=YEARLY;UNTIL=20060402T070000Z;BYDAY=1SU;BYMONTH=4
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:20070311T020000
RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3
TZNAME:EDT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:20071104T020000
RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11
TZNAME:EST
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
END:STANDARD
END:VTIMEZONE
BEGIN:VTIMEZONE
TZID:America/Los_Angeles
X-LIC-LOCATION:America/Los_Angeles
BEGIN:STANDARD
DTSTART:18831118T120702
RDATE:18831118T120702
TZNAME:PST
TZOFFSETFROM:-075258
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19180331T020000
RRULE:FREQ=YEARLY;UNTIL=19190330T100000Z;BYDAY=-1SU;BYMONTH=3
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19181027T020000
RRULE:FREQ=YEARLY;UNTIL=19191026T090000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19420209T020000
RDATE:19420209T020000
TZNAME:PWT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19450814T160000
RDATE:19450814T160000
TZNAME:PPT
TZOFFSETFROM:-0700
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19450930T020000
RDATE:19450930T020000
RDATE:19490101T020000
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:STANDARD
DTSTART:19460101T000000
RDATE:19460101T000000
RDATE:19670101T000000
TZNAME:PST
TZOFFSETFROM:-0800
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19480314T020000
RDATE:19480314T020000
RDATE:19740106T020000
RDATE:19750223T020000
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19500430T020000
RRULE:FREQ=YEARLY;UNTIL=19660424T100000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19500924T020000
RRULE:FREQ=YEARLY;UNTIL=19610924T090000Z;BYDAY=-1SU;BYMONTH=9
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:STANDARD
DTSTART:19621028T020000
RRULE:FREQ=YEARLY;UNTIL=19661030T090000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19670430T020000
RRULE:FREQ=YEARLY;UNTIL=19730429T100000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19671029T020000
RRULE:FREQ=YEARLY;UNTIL=20061029T090000Z;BYDAY=-1SU;BYMONTH=10
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19760425T020000
RRULE:FREQ=YEARLY;UNTIL=19860427T100000Z;BYDAY=-1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:19870405T020000
RRULE:FREQ=YEARLY;UNTIL=20060402T100000Z;BYDAY=1SU;BYMONTH=4
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:DAYLIGHT
DTSTART:20070311T020000
RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3
TZNAME:PDT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:20071104T020000
RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11
TZNAME:PST
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
END:STANDARD
END:VTIMEZONE
END:VCALENDAR
"""
        data = (
            (
                DateTime(2014, 3, 8, 23, 0, 0, Timezone(tzid="America/New_York")),
                DateTime(2014, 3, 8, 20, 0, 0, Timezone(tzid="America/Los_Angeles")),
            ),
            (
                DateTime(2014, 3, 9, 3, 0, 0, Timezone(utc=True)),
                DateTime(2014, 3, 8, 19, 0, 0, Timezone(tzid="America/Los_Angeles")),
            ),
            (
                DateTime(2014, 3, 9, 13, 0, 0, Timezone(utc=True)),
                DateTime(2014, 3, 9, 6, 0, 0, Timezone(tzid="America/Los_Angeles")),
            ),
        )

        Calendar.parseText(tzdata.replace("\n", "\r\n"))

        for dtfrom, dtto in data:

            self.assertEqual(dtfrom, dtto)

            newdtfrom = dtfrom.duplicate()
            newdtfrom.adjustTimezone(dtto.getTimezone())
            self.assertEqual(newdtfrom, dtto)
            self.assertEqual(newdtfrom.getHours(), dtto.getHours())
