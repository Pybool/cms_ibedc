import calendar
from django.shortcuts import get_object_or_404
import pendulum
from .parsedate import Datetimeutils
from datetime import date,  datetime, timedelta
import datetime as dt
from dateutil.relativedelta import relativedelta
from dateutil import rrule
from authentication.models import User


class Dashboardutils(object):
    
    def __init__(self,period):
        
        self.period = period
        self.dt_obj = Datetimeutils(int(period))
    
    def compare_uid(self,request):   
        user = get_object_or_404(User,id=request.user.id)
        print(user.id,user.id)
        return user.id == int(request.GET.get("cuid"))

    
    def getTodayPreviousmonth(self,months):
        
        y = self.dt_obj.months_previous_days_from_now_days(months)
        return self.dt_obj.get_previous_date(y)
        
    def get_previous_current_dates(self):
        
        y_days = 1 if self.period == '0' else 0
        w_days = 7 if self.period == '-1' or self.period == '-2' else 0
        days = int(self.dt_obj.months_previous_days_from_now(int(self.period))/24) if int(self.period) >= 1 and w_days is 0 else 0
        days = w_days + y_days + days

        prev_start_date, prev_end_date = self.void(days,self.period,self.dt_obj.get_previous_date(days))
        curr_start_date, curr_end_date = self.void(days,self.period,str(date.today()))
        dashboard_utils_dates = {}
        dashboard_utils_dates['prev_start_date'] = prev_start_date
        dashboard_utils_dates['prev_end_date'] = prev_end_date
        dashboard_utils_dates['curr_start_date'] = curr_start_date
        dashboard_utils_dates['curr_end_date'] = curr_end_date
        
        return dashboard_utils_dates
    

    # def start_end_period(self,days,period,q_date):
    def void(self,days,period,q_date):
            
        date = q_date.split("-")
        year = int(date[0])
        month = int(date[1][1]) if date[0]=='0' else int(date[1])
        day = int(date[2][1]) if date[0]=='0' else int(date[2])
        dt = pendulum.datetime(year, month, day)
        
        if int(period) >= 1: scale = "month"
        if period == '-2': scale = "week"
        if period == 0: scale = "day"
        if period == -1: scale = "week"

        start = dt.start_of(scale)

        end = dt.end_of(scale)
        return start.to_datetime_string().split(" ")[0], end.to_datetime_string().split(" ")[0]
    
def start_end_period(period,q_date):
            
        date = q_date.split("-")
        year = int(date[0])
        month = int(date[1][1]) if date[0]=='0' else int(date[1])
        day = int(date[2][1]) if date[0]=='0' else int(date[2])
        dt = pendulum.datetime(year, month, day)
        
        if int(period) >= 1: scale = "month"
        if period == '-2': scale = "week"
        if period == '0': scale = "day"
        if period == '-1': scale = "week"

        start = dt.start_of(scale)
    
        end = dt.end_of(scale)
        return start.to_datetime_string().split(" ")[0], end.to_datetime_string().split(" ")[0]
    
        
def get_date_day(x_date):
    day = datetime.strptime(x_date, '%d-%m-%y').strftime('%A')
    return day


def get_previous_n_days(n,**kwargs):

    today = date.today()
    if kwargs.get('get_day_date'):
        Dateslist = tuple({get_date_day(str((today - timedelta(days = day)).strftime('%Y-%m-%d'))):str((today - timedelta(days = day)).strftime('%Y-%m-%d'))} for day in range(n)
                    ) if kwargs.get('shorten') else tuple({get_date_day(str((today - timedelta(days = day)).strftime('%Y-%m-%d'))):str((today - timedelta(days = day)))} for day in range(n))

    else:
        Dateslist = tuple(str((today - timedelta(days = day)).strftime('%Y-%m-%d')) for day in range(1)) if kwargs.get('shorten') else tuple(str((today - timedelta(days = day)).strftime('%Y-%m-%d')) for day in range(1))
    Dateslist= reversed(Dateslist)
    return tuple(Dateslist)

def weeks_in_month(year,month):

    firstweekday = 6 # sunday is the first day of the week , set 0 for monday
    c = calendar.Calendar(firstweekday)
    for weekstart in filter(lambda d: d.weekday() == firstweekday, c.itermonthdates(year, month)):
        weekend = weekstart + timedelta(6)
        yield (weekstart, weekend)

def convert_date_format(date=''):
    
        now = datetime.now() if date == '' else date
        try:
            dt_string = now.strftime("%d/%m/%y")
            dt_string = dt_string.replace("/","-")
        except:
            dt_string = datetime.strptime(now, '%Y-%m-%d').strftime("%d/%m/%y")
            dt_string = dt_string.replace("/","-")
            
        return dt_string

def previous_week_range(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    start_date = date + dt.timedelta(-date.weekday(), weeks=-1)
    end_date = date + dt.timedelta(-date.weekday() - 1)
    return start_date.isoformat().split('T')[0], end_date.isoformat().split('T')[0]

def current_week_range(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    start_date = date - timedelta(days = date.weekday())
    end_date = end_of_week = start_date + timedelta(days = 6)
    return start_date.isoformat().split('T')[0], end_date.isoformat().split('T')[0]

def get_days_between_days(start_date,end_date):
        
        f_date = datetime.strptime(start_date, '%Y-%m-%d')
        l_date = datetime.strptime(end_date, '%Y-%m-%d')
        delta = l_date - f_date
        return delta.days
    
def date_range_dates(start_date,end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end - start  # as timedelta
    days = [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
    return days

def get_month_name(period,date_time):
    
    if period == 'month':
        currentDate = date_time
        currentMonthName = currentDate.strftime("%B")

        return currentMonthName

def split_bracket(string):
    return string.split('(')[1].split(')')[0]

def get_months_between_days(start_date,end_date):

    date_range = (list(rrule.rrule(rrule.MONTHLY, dtstart=datetime.strptime(start_date, '%Y-%m-%d'), until=datetime.strptime(end_date, '%Y-%m-%d'))))
    return [date_obj.strftime('%Y-%m-%d') for date_obj in date_range]

