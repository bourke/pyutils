import pytz
import re
from rfc3339 import rfc3339
from calendar import monthrange, timegm
from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import *
from dateutil import zoneinfo


eastern = pytz.timezone("US/Eastern")
utc = pytz.utc


def is_naive(dt):
    return dt.tzinfo is None and dt.tzinfo.utcoffset(dt) is None


def delta_seconds(td):
    return td.days * 86400 + td.seconds


def et_to_utc(dt):
    """convert a datetime with no tzinfo as est->utc."""
    return eastern.localize(dt).astimezone(utc)


def utc_to_et(dt):
    """convert a datetime with optional tzinfo as utc->est"""

    if not dt.tzinfo:
        dt = utc.localize(dt)
    return dt.astimezone(eastern)


def utc_fmt(dt):
    return rfc3339(dt)


_date_reg = re.compile(r'\b0(\d)')


def _dateformat(date, format="%A, %B %d, %Y"):
    return _date_reg.sub(r'\1', date.strftime(format))


def date_only(date):
    return _dateformat(date, "%d %B %Y")


def fulldate(date):
    return _dateformat(date)


def weekday_date(date):
    return _dateformat(date, format="%A, %B %d")


def weekday_only(date):
    return _dateformat(date, format="%A")


def month_date(date):
    return _dateformat(date, format="%m/%d")


def twelve_hour(date):
    h, m = tuple(date.strftime("%I:%M").split(":"))
    return '%s:%s' % (int(h), m)


def years_in_months(years):
    return int(round(years * 12))


def add_time_to_date(d, localized=True):
    dt = datetime(d.year, d.month, d.day, tzinfo=utc)
    if dt.date() == datetime.now(utc).date():
        dt = datetime.combine(dt.date(), datetime.now(utc).time())
    if localized:
        return utc_to_et(dt)
    return dt


def date_from_datestr(datestr, return_dt=False):
    dt = None
    for fmt in ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d'):
        try:
            dt = datetime.strptime(datestr, fmt)
        except:
            continue
        else:
            break
    if dt is None:
        raise ValueError(
            "from_datestr received datestr %s in wrong format" %
                datestr
        )
    return dt if return_dt else dt.date()


def dt_from_datestr(datestr, localized=True):
    dt = None
    for fmt in ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d'):
        try:
            dt = datetime.strptime(datestr, fmt).astimezone(utc)
        except:
            continue
        else:
            break
    if dt is None:
        raise ValueError(
            "from_datestr received datestr %s in wrong format" %
                datestr
        )
    return add_time_to_date(dt.date(), localized=localized)


def time_from_timestr(timestr):
    t = None
    for fmt in ('%H%M%S', '%H:%M:%S'):
        try:
            t = datetime.strptime(timestr, fmt).time()
        except:
            continue
        else:
            break
    if t is None:
        raise ValueError(
            "from_timestr received timestr %s in wrong format" %
                timestr
        )
    return t


def factor_datetime(dt):
    return dict(as_of_date=dt.date(), as_of_time=dt.timetz())


def iter_weekdays(dt, expanded=False, bounds_only=False):
    """
    Iterates Sunday to Saturday of the week surrounding a given datetime;
    in expanded mode also iterates over the week prior and week after
    """
    period_start = dt if (dt.weekday() == 6) else dt - timedelta(days=dt.weekday() + 1)
    if expanded:
        period_start = period_start - timedelta(days=7)
        for i in xrange(21):
            yield period_start + timedelta(days=i)
    elif bounds_only:
        for day in (period_start, period_start + timedelta(days=6)):
            yield day
    else:
        for i in xrange(7):
            yield period_start + timedelta(days=i)


def iter_dates(startdate, enddate, skip_days=[], include_end=False):
    for i in xrange((enddate - startdate).days):
        res = startdate + timedelta(i)
        if res.weekday() not in skip_days:
            yield res
    if include_end:
        yield enddate



def month_ends(num_months, as_of_date):

    one_twelfth = float(1) / float(12)

    end_year, end_month = as_of_date.year, as_of_date.month - 1

    if end_month == 0:
        end_year = end_year - 1
        end_month = 12

    decimal_end_year = end_year + end_month * one_twelfth
    decimal_start_year = decimal_end_year - num_months * one_twelfth

    def conv(decimal_year):
        return int(decimal_year), int(round((decimal_year % 1) * 12))

    res = []

    def iter_months(num_months):
        for i in range(num_months):
            decimal_year = decimal_start_year + i * one_twelfth
            year, month = conv(decimal_year)
            if month == 0:
                month = 12
                year = year - 1
            yield year, month

    for year, month in iter_months(num_months):
        d = monthrange(year, month)[1]
        res.append((year, month, d))

    return res


def seconds_from_epoch(dt=datetime.utcnow()):
    struct = dt.timetuple()
    return timegm(struct)


def milliseconds_from_epoch(dt):
    return seconds_from_epoch(dt) * 1000

def months_ago(date):
    delta = relativedelta(datetime.utcnow().date(), date.date())
    return delta.months + (delta.years * 12)

def days_ago(date):
    return seconds_ago(date) / 86400

def seconds_ago(date):
    delta = datetime.utcnow() - date.replace(tzinfo=None)
    return delta_seconds(delta)

def time_recency(date):
    if days_ago(date) > 1:
        return "%d days ago" % days_ago(date)
    elif days_ago(date) == 1:
        return " ".join([time_only(date), "yesterday"])
    else:
        return time_only(date)

def ordinal_suffix(date):
    n = int(date.strftime("%d"))
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
        return str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

_text_reg = re.compile(r'(A|P)M')

def lower_match(match):
    return match.group(1).lower()

def et_now():
    tz = zoneinfo.gettz("EST5EDT")
    return datetime.now(tz=tz)

def recency(date, minutes=3):
    months = months_ago(date)

    et_date = utc_to_et(date)
    default_timestamp = _text_reg.sub(lower_match, et_date.strftime("%I.%M%p ET on %d %b"))
    time_only_timestamp = _text_reg.sub(lower_match, et_date.strftime("%I.%M%p"))

    if et_date.year != et_now().year:
        default_timestamp = default_timestamp + et_date.strftime(" %y")

    t = months / 12
    if t > 0:
        return default_timestamp
    t = months
    if t > 0:
        return default_timestamp

    seconds = seconds_ago(date)
    t = seconds / 86400 / 7
    if t > 0:
        return default_timestamp

    def date_difference():
        diff = et_date.date() - et_now().date()
        print
        if diff == timedelta(0):
            return time_only_timestamp + " earlier today"
        elif diff < timedelta(1):
            return time_only_timestamp + " yesterday"
        else:
            return None

    t = seconds / 86400
    if t > 1:
        custom = date_difference()
        if custom:
            return custom
        return default_timestamp

    t = seconds / 3600
    if t > 0:
        custom = date_difference()
        return custom


    t = seconds / 60
    if t > minutes:
        return "%d " % t + ("minutes" if t > 1 else "minute") + " ago"

    return "Just now"
