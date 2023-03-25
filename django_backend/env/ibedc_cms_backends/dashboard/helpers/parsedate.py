import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

class Datetimeutils(object):
    
    def __init__(self,duration):
        self.duration = duration

    def months_previous_days_from_now(self,months,hrs=''):
        delta = relativedelta(months=months)
        time_month_previous = datetime.date.today() - delta
        return abs((datetime.date.today()-time_month_previous).days) * 24

    def months_previous_days_from_now_days(self,months,hrs=''):
        delta = relativedelta(months=months)
        time_month_previous = datetime.date.today() - delta
        return abs((datetime.date.today()-time_month_previous).days)

    def get_previous_date(self,days):
        print("Comparison ",datetime.date.today() , datetime.timedelta(days=days),days)
        return str(datetime.date.today() - datetime.timedelta(days=days)).split(" ")[0]

    def get_pages_created_on_date(self,filter):

        if filter == 'day': hours = 24 * self.duration
        if filter == 'week': hours = 168 * self.duration
        if filter == 'month': hours = self.months_previous_days_from_now(self.duration) 
        if filter == 'year': hours = self.months_previous_days_from_now(12) 
        now = datetime.datetime.now()
        end_date = now.replace(minute=0, second=0, microsecond=0)
        start_date = end_date - datetime.timedelta(hours=hours)
        return (start_date , end_date)
    