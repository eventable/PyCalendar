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
import time

from duration import PyCalendarDuration
from timezone import PyCalendarTimezone
import definitions
import locale
import utils

class PyCalendarDateTime(object):

    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    
    FULLDATE = 0
    ABBREVDATE = 1
    NUMERICDATE = 2
    FULLDATENOYEAR = 3
    ABBREVDATENOYEAR = 4
    NUMERICDATENOYEAR = 5

    @staticmethod
    def sort(e1, e2):

        return e1.compareDateTime(e2)

    def __init__( self, year = None, month = None, day = None, hours = None, minutes = None, seconds = None, tzid = None, packed = None, copyit = None ):
        
        self.mYear = 1970
        self.mMonth = 1
        self.mDay = 1

        self.mHours = 0
        self.mMinutes = 0
        self.mSeconds = 0

        self.mDateOnly = False

        self.mTZUTC = True
        self.mTZID = None

        self.mPosixTimeCached = False
        self.mPosixTime = 0

        if (year is not None) and (month is not None) and (day is not None) and \
           (hours is not None) and (minutes is not None) and (seconds is not None):
            self.mYear = year
            self.mMonth = month
            self.mDay = day
            self.mHours = hours
            self.mMinutes = minutes
            self.mSeconds = seconds
            if tzid:
                self.mTZUTC = tzid.getUTC()
                self.mTZID = tzid.getTimezoneID()
        elif (year is not None) and (month is not None) and (day is not None):
            self.mYear = year
            self.mMonth = month
            self.mDay = day
            self.mDateOnly = True
            if tzid:
                self.mTZUTC = tzid.getUTC()
                self.mTZID = tzid.getTimezoneID()
        elif (packed is not None):
            # Unpack a packed date
            self.mYear = utils.unpackDateYear( packed )
            self.mMonth = utils.unpackDateMonth( packed )
            self.mDay = utils.unpackDateDay( packed )
            if self.mDay < 0:
                self.mDay = -self.mDay
            self.mDateOnly = True
    
            if tzid:
                self.mTZUTC = tzid.getUTC()
                self.mTZID = tzid.getTimezoneID()
    
            self.normalise()
        elif (copyit is not None):
            self.mYear = copyit.mYear
            self.mMonth = copyit.mMonth
            self.mDay = copyit.mDay
    
            self.mHours = copyit.mHours
            self.mMinutes = copyit.mMinutes
            self.mSeconds = copyit.mSeconds
    
            self.mDateOnly = copyit.mDateOnly
    
            self.mTZUTC = copyit.mTZUTC
            self.mTZID = copyit.mTZID
    
            self.mPosixTimeCached = copyit.mPosixTimeCached
            self.mPosixTime = copyit.mPosixTime
    
    def __repr__(self):
        return self.getText()

    def __hash__(self):
        return self.getPosixTime()
    
    # Operators
    def __add__( self, duration ):
        # Add duration seconds to temp object and normalise it
        result = PyCalendarDateTime(copyit=self)
        result.mSeconds += duration.getTotalSeconds()
        result.changed()
        result.normalise()
        return result
 
    def __sub__( self, date ):
        # Look for floating
        if self.floating() or date.floating():
            # Adjust the floating ones to fixed
            copy1 = PyCalendarDateTime(copyit=self)
            copy2 = PyCalendarDateTime(copyit=date)

            if copy1.floating() and copy2.floating():
                # Set both to UTC and do comparison
                copy1.setTimezoneUTC( True )
                copy2.setTimezoneUTC( True )
                return copy1 - copy2
            elif copy1.floating():
                # Set to be the same
                copy1.setTimezoneUTC( copy2.getTimezoneUTC() )
                copy1.setTimezoneID( copy2.getTimezoneID() )
                return copy1 - copy2
            else:
                # Set to be the same
                copy2.setTimezoneID( copy1.getTimezoneID() )
                copy2.setTimezoneUTC( copy1.getTimezoneUTC() )
                return copy1 - copy2
 
        else:
            # Do diff of date-time in seconds
            diff = self.getPosixTime() - date.getPosixTime()
            return PyCalendarDuration(duration=diff)

    # Comparators
    def __eq__( self, comp ):
        return self.compareDateTime( comp ) == 0

    def __ne__( self, comp ):
        return self.compareDateTime( comp ) != 0

    def __ge__( self, comp ):
        return self.compareDateTime( comp ) >= 0

    def __le__( self, comp ):
        return self.compareDateTime( comp ) <= 0

    def __gt__( self, comp ):
        return self.compareDateTime( comp ) > 0

    def __lt__( self, comp ):
        return self.compareDateTime( comp ) < 0

    def compareDateTime( self, comp ):
        # If either are date only, then just do date compare
        if self.mDateOnly or comp.mDateOnly:
            if self.mYear == comp.mYear:
                if self.mMonth == comp.mMonth:
                    if self.mDay == comp.mDay:
                        return 0
                    else:
                        if self.mDay < comp.mDay:
                            return -1
                        else:
                            return 1
                else:
                    if self.mMonth < comp.mMonth:
                        return -1
                    else:
                        return 1
            else:
                if self.mYear < comp.mYear:
                    return -1
                else:
                    return 1
 
        # If they have the same timezone do simple compare - no posix calc
        # needed
        elif ( PyCalendarTimezone.same( self.mTZUTC, self.mTZID, comp.mTZUTC, comp.mTZID ) ):
            if self.mYear == comp.mYear:
                if self.mMonth == comp.mMonth:
                    if self.mDay == comp.mDay:
                        if self.mHours == comp.mHours:
                            if self.mMinutes == comp.mMinutes:
                                if self.mSeconds == comp.mSeconds:
                                    return 0
                                else:
                                    if self.mSeconds < comp.mSeconds:
                                        return -1
                                    else:
                                        return 1
                            else:
                                if self.mMinutes < comp.mMinutes:
                                    return -1
                                else:
                                    return 1
                        else:
                            if self.mHours < comp.mHours:
                                return -1
                            else:
                                return 1
                    else:
                        if self.mDay < comp.mDay:
                            return -1
                        else:
                            return 1
                else:
                    if self.mMonth < comp.mMonth:
                        return -1
                    else:
                        return 1
            else:
                if self.mYear < comp.mYear:
                    return -1
                else:
                    return 1
        else:
            posix1 = self.getPosixTime()
            posix2 = comp.getPosixTime()
            if posix1 == posix2:
                return 0
            else:
                if posix1 < posix2:
                    return -1
                else:
                    return 1

    def compareDate( self, comp ):
        return ( self.mYear == comp.mYear ) and ( self.mMonth == comp.mMonth ) and ( self.mDay == comp.mDay )
 
    def getPosixTime( self ):
        # Look for cached value (or floating time which has to be calculated
        # each time)
        if ( not self.mPosixTimeCached ) or self.floating():
            result = 0L

            # Add hour/mins/secs
            result = ( self.mHours * 60L + self.mMinutes ) * 60L + self.mSeconds

            # Number of days since 1970
            result += self.daysSince1970() * 24L * 60L * 60L

            # Adjust for timezone offset
            result -= self.timeZoneSecondsOffset()

            # Now indcate cache state
            self.mPosixTimeCached = True
            self.mPosixTime = result
 
        return self.mPosixTime

    def isDateOnly( self ):
        return self.mDateOnly

    def setDateOnly( self, date_only ):
        self.mDateOnly = date_only
        self.changed()

    def getYear( self ):
        return self.mYear

    def setYear( self, year ):
        if self.mYear != year:
            self.mYear = year
            self.changed()

    def offsetYear( self, diff_year ):
        self.mYear += diff_year
        self.normalise()

    def getMonth( self ):
        return self.mMonth

    def setMonth( self, month ):
        if self.mMonth != month:
            self.mMonth = month
            self.changed()

    def offsetMonth( self, diff_month ):
        self.mMonth += diff_month
        self.normalise()

    def getDay( self ):
        return self.mDay

    def setDay( self, day ):
        if self.mDay != day:
            self.mDay = day
            self.changed()

    def offsetDay( self, diff_day ):
        self.mDay += diff_day
        self.normalise()

    def setYearDay( self, day ):
        # 1 .. 366 offset from start, or
        # -1 .. -366 offset from end

        if day > 0:
            # Offset current date to 1st January of current year
            self.mMonth = 1
            self.mDay = 1

            # Increment day
            self.mDay += day - 1

            # Normalise to get proper month/day values
            self.normalise()
        elif day < 0:
            # Offset current date to 1st January of next year
            self.mYear += 1
            self.mMonth = 1
            self.mDay = 1

            # Decrement day
            self.mDay += day

            # Normalise to get proper year/month/day values
            self.normalise()

    def getYearDay( self ):
        return self.mDay + utils.daysUptoMonth( self.mMonth, self.mYear )

    def setMonthDay( self, day ):
        # 1 .. 31 offset from start, or
        # -1 .. -31 offset from end

        if day > 0:
            # Offset current date to 1st of current month
            self.mDay = 1

            # Increment day
            self.mDay += day - 1

            # Normalise to get proper month/day values
            self.normalise()
        elif day < 0:
            # Offset current date to 1st of next month
            self.mMonth += 1
            self.mDay = 1

            # Decrement day
            self.mDay += day

            # Normalise to get proper year/month/day values
            self.normalise()

    def isMonthDay( self, day ):
        if day > 0:
            return self.mDay == day
        elif day < 0:
            return self.mDay - 1 - utils.daysInMonth( self.mMonth, self.mYear ) == day
        else:
            return False

    def setWeekNo( self, weekno ):
        # This is the iso 8601 week number definition

        # What day does the current year start on
        temp = PyCalendarDateTime(year=self.mYear, month=1, day=1)
        first_day = temp.getDayOfWeek()

        # Calculate and set yearday for start of week
        if ( first_day == PyCalendarDateTime.SUNDAY ) or ( first_day == PyCalendarDateTime.MONDAY ) or \
            ( first_day == PyCalendarDateTime.TUESDAY ) or ( first_day == PyCalendarDateTime.WEDNESDAY ) or ( first_day == PyCalendarDateTime.THURSDAY ):
            self.setYearDay( ( weekno - 1 ) * 7 - first_day )
        elif ( first_day == PyCalendarDateTime.FRIDAY ) or ( first_day == PyCalendarDateTime.SATURDAY ):
            self.setYearDay( ( weekno - 1 ) * 7 - first_day + 7 )

    def getWeekNo( self ):
        # This is the iso 8601 week number definition

        # What day does the current year start on
        temp = PyCalendarDateTime(year=self.mYear, month=1, day=1)
        first_day = temp.getDayOfWeek()

        # Get days upto the current one
        yearday = self.getYearDay()

        if ( first_day == PyCalendarDateTime.SUNDAY ) or ( first_day == PyCalendarDateTime.MONDAY ) or \
            ( first_day == PyCalendarDateTime.TUESDAY ) or ( first_day == PyCalendarDateTime.WEDNESDAY ) or ( first_day == PyCalendarDateTime.THURSDAY ):
            return ( yearday + first_day ) / 7 + 1
        elif ( first_day == PyCalendarDateTime.FRIDAY ) or ( first_day == PyCalendarDateTime.SATURDAY ):
            return ( yearday + first_day - 7 ) / 7 + 1

    def isWeekNo( self, weekno ):
        # This is the iso 8601 week number definition

        if weekno > 0:
            return self.getWeekNo() == weekno
        else:
            # This needs to calculate the negative offset from the last week in
            # the current year
            return False

    def setDayOfWeekInYear( self, offset, day ):
        # Set to first day in year
        self.mMonth = 1
        self.mDay = 1

        # Determine first weekday in year
        first_day = self.getDayOfWeek()

        if offset > 0:
            cycle = ( offset - 1 ) * 7 + day
            cycle -= first_day
            if first_day > day:
                cycle += 7
            self.mDay = cycle + 1
        elif offset < 0:
            first_day += 365 + [1, 0][not utils.isLeapYear( self.mYear )] - 1
            first_day %= 7

            cycle = ( -offset - 1 ) * 7 - day
            cycle += first_day
            if day > first_day:
                cycle += 7
            self.mDay = 365 + [1, 0][not utils.isLeapYear( self.mYear )] - cycle

        self.normalise()

    def setDayOfWeekInMonth( self, offset, day ):
        # Set to first day in month
        self.mDay = 1

        # Determine first weekday in month
        first_day = self.getDayOfWeek()

        if offset > 0:
            cycle = ( offset - 1 ) * 7 + day
            cycle -= first_day
            if first_day > day:
                cycle += 7
            self.mDay = cycle + 1
        elif offset < 0:
            days_in_month = utils.daysInMonth( self.mMonth, self.mYear )
            first_day += days_in_month - 1
            first_day %= 7

            cycle = ( -offset - 1 ) * 7 - day
            cycle += first_day
            if day > first_day:
                cycle += 7
            self.mDay = days_in_month - cycle

        self.normalise()

    def setNextDayOfWeek( self, start, day ):
        # Set to first day in month
        self.mDay = start

        # Determine first weekday in month
        first_day = self.getDayOfWeek()

        if first_day > day:
            self.mDay += 7

        self.mDay += day - first_day
            
        self.normalise()

    def isDayOfWeekInMonth( self, offset, day ):
        # First of the actual day must match
        if self.getDayOfWeek() != day:
            return False

        # If there is no count the we match any of this day in the month
        if offset == 0:
            return True

        # Create temp date-time with the appropriate parameters and then
        # compare
        temp = PyCalendarDateTime(copyit=self)
        temp.setDayOfWeekInMonth( offset, day )

        # Now compare dates
        return self.compareDate( temp )

    def getDayOfWeek( self ):
        # Count days since 01-Jan-1970 which was a Thursday
        result = PyCalendarDateTime.THURSDAY + self.daysSince1970()
        result %= 7
        if result < 0:
            result += 7

        return result

    def getMonthText( self, short_txt ):
        # Make sure range is valid
        if ( self.mMonth < 1 ) or ( self.mMonth > 12 ):
            return ""
        else:
            return locale.getMonth( self.mMonth, 
                    [locale.SHORT, locale.LONG][not short_txt] )

    def getDayOfWeekText( self, day ):
        return locale.getDay( day, locale.SHORT )

    def setHHMMSS( self, hours, minutes, seconds ):
        if ( self.mHours != hours ) or ( self.mMinutes != minutes ) or ( self.mSeconds != seconds ):
            self.mHours = hours
            self.mMinutes = minutes
            self.mSeconds = seconds
            self.changed()

    def getHours( self ):
        return self.mHours

    def setHours( self, hours ):
        if self.mHours != hours:
            self.mHours = hours
            self.changed()

    def offsetHours( self, diff_hour ):
        self.mHours += diff_hour
        self.normalise()

    def getMinutes( self ):
        return self.mMinutes

    def setMinutes( self, minutes ):
        if self.mMinutes != minutes:
            self.mMinutes = minutes
            self.changed()

    def offsetMinutes( self, diff_minutes ):
        self.mMinutes += diff_minutes
        self.normalise()

    def getSeconds( self ):
        return self.mSeconds

    def setSeconds( self, seconds ):
        if self.mSeconds != seconds:
            self.mSeconds = seconds
            self.changed()

    def offsetSeconds( self, diff_seconds ):
        self.mSeconds += diff_seconds
        self.normalise()

    def getTimezoneUTC( self ):
        return self.mTZUTC

    def setTimezoneUTC( self, utc ):
        self.mTZUTC = utc

    def getTimezoneID( self ):
        return self.mTZID

    def setTimezoneID( self, tzid ):
        self.mTZUTC = False
        self.mTZID = tzid
        self.changed()

    def utc( self ):
        return self.mTZUTC

    def local( self ):
        return ( not self.mTZUTC ) and self.mTZID

    def floating( self ):
        return ( not self.mTZUTC ) and not self.mTZID

    #public ICalendarTimezone getTimezone() {
    #    return mTimezone
    #}

    def setTimezone( self, tzid ):
        self.mTZUTC = tzid.getUTC()
        self.mTZID = tzid.getTimezoneID()
        self.changed()

    def adjustTimezone( self, tzid ):
        # Only if different
        s1 = tzid.getTimezoneID()
        if ( tzid.getUTC() != self.mTZUTC ) or ( s1 != self.mTZID ):
            offset_from = self.timeZoneSecondsOffset()
            self.setTimezone( tzid )
            offset_to = self.timeZoneSecondsOffset()
            self.offsetSeconds( offset_to - offset_from )

    def adjustToUTC( self ):
        if not self.mTZUTC:
            utc = PyCalendarTimezone(utc=True)

            offset_from = self.timeZoneSecondsOffset()
            self.setTimezone( utc )
            offset_to = self.timeZoneSecondsOffset()

            self.offsetSeconds( offset_to - offset_from )

    #def getAdjustedTime( self, tzid = PyCalendarManager.sPyCalendarManager.getDefaultTimezone() ):
    def getAdjustedTime( self, tzid = None ):
        # Copy this and adjust to input timezone
        adjusted = PyCalendarDateTime(copyit=self)
        adjusted.adjustTimezone( tzid )
        return adjusted

    def setToday( self ):
        tz = PyCalendarTimezone(utc=self.mTZUTC, tzid=self.mTZID)
        self.copy_ICalendarDateTime( self.getToday( tz ) )

    @staticmethod
    def getToday( tzid ):
        # Get from posix time
        now = time.time()
        now_tm = time.localtime( now )
    
        temp = PyCalendarDateTime(year=now_tm.tm_year, month=now_tm.tm_mon, day=now_tm.tm_mday, tzid=tzid)
        return temp
    
    def setNow( self ):
        tz = PyCalendarTimezone(utc=self.mTZUTC, tzid=self.mTZID)
        self.copy_ICalendarDateTime( self.getNow( tz ) )

    @staticmethod
    def getNow( tzid ):
        utc = PyCalendarDateTime.getNowUTC()
        utc.adjustTimezone( [tzid, PyCalendarTimezone()][tzid == 0] )
        return utc
    
    def setNowUTC( self ):
        self.copy_PyCalendarDateTime( self.getNowUTC() )

    @staticmethod
    def getNowUTC( ):
        # Get from posix time
        now = time.time()
        now_tm = time.gmtime( now )
        tzid = PyCalendarTimezone(utc=True)
    
        temp = PyCalendarDateTime(year=now_tm.tm_year, month=now_tm.tm_mon, day=now_tm.tm_mday, hours=now_tm.tm_hour, minutes=now_tm.tm_min, seconds=now_tm.tm_sec, tzid=tzid )
        return temp

    def recur( self, freq, interval ):
        # Add appropriate interval
        if freq == definitions.eRecurrence_SECONDLY:
            self.mSeconds += interval
        elif freq == definitions.eRecurrence_MINUTELY:
            self.mMinutes += interval
        elif freq == definitions.eRecurrence_HOURLY:
            self.mHours += interval
        elif freq == definitions.eRecurrence_DAILY:
            self.mDay += interval
        elif freq == definitions.eRecurrence_WEEKLY:
            self.mDay += 7 * interval
        elif freq == definitions.eRecurrence_MONTHLY:
            # Iterate until a valid day in the next month is found.
            # This can happen if adding one month to e.g. 31 January.
            # That is an undefined operation - does it mean 28/29 February
            # or 1/2 May, or 31 March or what? We choose to find the next month with
            # the same day number as the current one.
            self.mMonth += interval
            self.normalise()
            while self.mDay > utils.daysInMonth( self.mMonth, self.mYear ):
                self.mMonth += interval
                self.normalise()
        elif freq == definitions.eRecurrence_YEARLY:
            self.mYear += interval

        # Normalise to standard date-time ranges
        self.normalise()

    def getLocaleDate( self, locale ):

        buf = StringIO.StringIO()

        if locale == PyCalendarDateTime.FULLDATE:
            buf.write( locale.getDay( self.getDayOfWeek(), locale.LONG ) )
            buf.write( ", " )
            buf.write( locale.getMonth( self.mMonth, locale.LONG ) )
            buf.write( " " )
            buf.write( str( self.mDay ) )
            buf.write( ", " )
            buf.write( str( self.mYear ) )
        elif locale == PyCalendarDateTime.ABBREVDATE:
            buf.write( locale.getDay( self.getDayOfWeek(), locale.SHORT ) )
            buf.write( ", " )
            buf.write( locale.getMonth( self.mMonth, locale.SHORT ) )
            buf.write( " " )
            buf.write( str( self.mDay ) )
            buf.write( ", " )
            buf.write( str( self.mYear ) )
        elif locale == PyCalendarDateTime.NUMERICDATE:
            buf.write( str( self.mMonth ) )
            buf.write( "/" )
            buf.write( str( self.mDay ) )
            buf.write( "/" )
            buf.write( str( self.mYear ) )
        elif locale == PyCalendarDateTime.FULLDATENOYEAR:
            buf.write( locale.getDay( self.getDayOfWeek(), locale.LONG ) )
            buf.write( ", " )
            buf.write( locale.getMonth( self.mMonth, locale.LONG ) )
            buf.write( " " )
            buf.write( str( self.mDay ) )
        elif locale == PyCalendarDateTime.ABBREVDATENOYEAR:
            buf.write( locale.getDay( self. getDayOfWeek(), locale.SHORT ) )
            buf.write( ", " )
            buf.write( locale.getMonth( self.mMonth, locale.SHORT ) )
            buf.write( " " )
            buf.write( str( self.mDay ) )
        elif locale == PyCalendarDateTime.NUMERICDATENOYEAR:
            buf.write( str( self.mMonth ) )
            buf.write( "/" )
            buf.write( str( self.mDay ) )

        return buf.getvalue()

    def getTime( self, with_seconds, am_pm, tzid ):

        buf = StringIO.StringIO()
        adjusted_hour = self.mHours

        if am_pm:
            am = True
            if adjusted_hour >= 12:
                adjusted_hour -= 12
                am = False

            if adjusted_hour == 0:
                adjusted_hour = 12

            buf.write( str( adjusted_hour ) )
            buf.write( ":" )
            if self.mMinutes < 10:
                buf.write( "0" )
            buf.write( str( self.mMinutes ) )
            if with_seconds:
                buf.write( ":" )
                if self.mSeconds < 10:
                    buf.write( "0" )
                buf.write( str( self.mSeconds ) )

            buf.write( [" AM", " PM"][not am] )
        else:
            if self.mHours < 10:
                buf.write( "0" )
            buf.write( str( self.mHours ) )
            buf.write( ":" )
            if self.mMinutes < 10:
                buf.write( "0" )
            buf.write( str( self.mMinutes ) )
            if with_seconds:
                buf.write( ":" )
                if self.mSeconds < 10:
                    buf.write( "0" )
                buf.write( str( self.mSeconds ) )

        if tzid:
            desc = self.timeZoneDescriptor()
            if len( desc ) > 0:
                buf.write( " " )
                buf.write( desc )

        return buf.getvalue()

    def getLocaleDateTime( self, locale, with_seconds, am_pm, tzid ):
        return self.getLocaleDate( locale ) + " " + self.getTime( with_seconds, am_pm, tzid )

    def getText( self ):
    
        if self.mDateOnly:
            buf = "%4d%02d%02d" % ( self.mYear, self.mMonth, self.mDay )
        else:
            if self.mTZUTC:
                buf = "%4d%02d%02dT%02d%02d%02dZ" % ( self.mYear, self.mMonth, self.mDay, self.mHours, self.mMinutes, self.mSeconds )
            else:
                buf = "%4d%02d%02dT%02d%02d%02d" % ( self.mYear, self.mMonth, self.mDay, self.mHours, self.mMinutes, self.mSeconds )
        return buf

    def parse( self, data ):

        # parse format YYYYMMDD[THHMMSS[Z]]

        # Size must be at least 8
        if len( data ) < 8:
            return

        # Get year
        buf = data[0:4]
        self.mYear = int( buf )

        # Get month
        buf = data[4:6]
        self.mMonth = int( buf )

        # Get day
        buf = data[6:8]
        self.mDay = int( buf )

        # Now look for more
        if ( len( data ) >= 15 ) and ( data[8] == 'T' ):
            # Get hours
            buf = data[9:11]
            self.mHours = int( buf )

            # Get minutes
            buf = data[11:13]
            self.mMinutes = int( buf )

            # Get seconds
            buf = data[13:15]
            self.mSeconds = int( buf )

            self.mDateOnly = False

            if len(data) > 15:
                self.mTZUTC = ( data[15] == 'Z' )
            else:
                self.mTZUTC = False
        else:
            self.mDateOnly = True

        # Always uncache posix time
        self.changed()

    def generate( self, os ):
        try:
            os.write( self.getText() )
        except:
            pass

    def generateRFC2822( self, os ):
        pass

    def normalise( self ):
        # Normalise seconds
        normalised_secs = self.mSeconds % 60
        adjustment_mins = self.mSeconds / 60
        if normalised_secs < 0:
            normalised_secs += 60
            adjustment_mins -= 1
        self.mSeconds = normalised_secs
        self.mMinutes += adjustment_mins

        # Normalise minutes
        normalised_mins = self.mMinutes % 60
        adjustment_hours = self.mMinutes / 60
        if normalised_mins < 0:
            normalised_mins += 60
            adjustment_hours -= 1
        self.mMinutes = normalised_mins
        self.mHours += adjustment_hours

        # Normalise hours
        normalised_hours = self.mHours % 24
        adjustment_days = self.mHours / 24
        if normalised_hours < 0:
            normalised_hours += 24
            adjustment_days -= 1
        self.mHours = normalised_hours
        self.mDay += adjustment_days

        # Wipe the time if date only
        if self.mDateOnly:
            self.mSeconds = self.mMinutes = self.mHours = 0

        # Adjust the month first, since the day adjustment is month dependent

        # Normalise month
        normalised_month = ( ( self.mMonth - 1 ) % 12 ) + 1
        adjustment_year = ( self.mMonth - 1 ) / 12
        if ( normalised_month - 1 ) < 0:
            normalised_month += 12
            adjustment_year -= 1
        self.mMonth = normalised_month
        self.mYear += adjustment_year

        # Now do days
        if self.mDay > 0:
            while self.mDay > utils.daysInMonth( self.mMonth, self.mYear ):
                self.mDay -= utils.daysInMonth( self.mMonth, self.mYear )
                self.mMonth += 1
                if self.mMonth > 12:
                    self.mMonth = 1
                    self.mYear += 1
        else:
            while self.mDay <= 0:
                self.mMonth -= 1
                if self.mMonth < 1:
                    self.mMonth = 12
                    self.mYear -= 1
                self.mDay += utils.daysInMonth( self.mMonth, self.mYear )

        # Always invalidate posix time cache
        self.changed()

    def timeZoneSecondsOffset( self ):
        if self.mTZUTC:
            return 0
        tz = PyCalendarTimezone(utc=self.mTZUTC, tzid=self.mTZID)
        return tz.timeZoneSecondsOffset( self )

    def timeZoneDescriptor( self ):
        tz = PyCalendarTimezone(utc=self.mTZUTC, tzid=self.mTZID)
        return tz.timeZoneDescriptor( self )

    def changed( self ):
        self.mPosixTimeCached = False

    def daysSince1970( self ):
        # Add days betweenn 1970 and current year (ignoring leap days)
        result = ( self.mYear - 1970 ) * 365

        # Add leap days between years
        result += utils.leapDaysSince1970( self.mYear - 1970 )

        # Add days in current year up to current month (includes leap day for
        # current year as needed)
        result += utils.daysUptoMonth( self.mMonth, self.mYear )

        # Add days in month
        result += self.mDay - 1

        return result
