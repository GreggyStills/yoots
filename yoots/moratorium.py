"""Functions for determining when a regularly-scheduled moratorium is in effect."""
import time

this_year = int(time.strftime("%Y"))


def make_day_julian(isodate):
    """Generate a Julian date integer from a YYYY-MM-DD string.

    Args:
        isodate (str): ISO 8601 date string, e.g. "2018-03-17" (Mar 17, 2018)
    Returns:
        (int): Julian date
    """
    dt = time.strptime(isodate, "%Y-%m-%d")
    return int(time.strftime("%j", dt))


def make_month_julian(year, month):
    """Generate a list of Julian date integers within a given month.

    Args:
        year (int): 4-digit year
        month (int): integer month (1 = Jan, 2 = Feb, etc.)
    Returns:
        jdays (list): list of Julian dates
    """
    jdays = []
    for d in range(1, 32):
        try:
            dtuple = time.strptime("{} {} {}".format(year, month, d), "%Y %m %d")
            jday = int(time.strftime("%j", dtuple))
            jdays.append(jday)
        except ValueError:
            pass
    return jdays


def get_nth_day(day_name, n, year, month):
    """Get Nth occurence of day named <blah> in some month.  If n = -1, return the last one.

    Args:
        day_name (str): name of day, full and capitalized, e.g. "Thursday"
        n (int): Nth occurrence of day_name (1 = first, -1 = last)
        year (int): 4-digit year
        month (int): integer month (1 = Jan, 2 = Feb, etc.)
    Returns:
        jday (int): Julian date
    """
    days_matched = []
    for d in range(1, 32):
        try:
            dt = time.strptime("{} {} {}".format(year, month, d), "%Y %m %d")
            dname = time.strftime("%A", dt)
            if dname == day_name:
                j = int(time.strftime("%j", dt))
                days_matched.append(j)
        except ValueError:
            pass
    if n == -1:
        return days_matched[-1]
    else:
        return days_matched[n-1]


holidays = {
    "New Year's Day": make_day_julian("{}-01-01".format(this_year)),
    "Martin Luther King Jr Day": get_nth_day("Monday", 3, this_year, 1),
    "Presidents Day": get_nth_day("Monday", 3, this_year, 2),
    "Memorial Day": get_nth_day("Monday", -1, this_year, 5),
    "Independence Day": make_day_julian("{}-07-04".format(this_year)),
    "Labor Day": get_nth_day("Monday", 1, this_year, 9),
    "Thanksgiving": get_nth_day("Thursday", 4, this_year, 11),
    "Thanksgiving Friday": get_nth_day("Thursday", 4, this_year, 11)+1,
    "Christmas": make_day_julian("{}-12-25".format(this_year))
}


def is_holiday(dtuple=None):
    """Check if company holiday.

    Args:
        dtuple (time.struct_time): a time tuple for some date
    Returns:
        (bool): True if holiday
    """
    if dtuple is None:
        dtuple = time.gmtime()
    today = int(time.strftime("%j", dtuple))
    if today in holidays.values():
        return True
    else:
        return False


def is_eom(dtuple=None, end_days=3):
    """Check if end-of-month.

    Args:
        dtuple (time.struct_time): a time tuple for some date
        end_days (int): number of days at end of month
    Returns:
        (bool): True if end-of-month
    """
    if dtuple is None:
        dtuple = time.gmtime()
    today_julian = int(time.strftime("%j", dtuple))
    year = dtuple.tm_year
    month = dtuple.tm_mon
    jcal = make_month_julian(year, month)
    if today_julian in jcal[-end_days:]:
        return True
    else:
        return False


def is_eoy(dtuple=None):
    """Check if end-of-year (Thanksgiving -> Dec 31).

    Args:
        dtuple (time.struct_time): a time tuple for some date
    Returns:
        (bool): True if end-of-month
    """
    if dtuple is None:
        dtuple = time.gmtime()
    thx = holidays["Thanksgiving"]
    today = int(time.strftime("%j", dtuple))
    if today >= thx:
        return True
    else:
        return False
