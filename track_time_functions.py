import time
import datetime


def get_day():
    date = str(datetime.datetime.now().date())
    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    day_chosen = day_name[day]
    return day_chosen


def get_time():
    t_format = "%H:%M:%S"
    my_time = str(time.strftime(t_format, time.localtime()))
    return my_time