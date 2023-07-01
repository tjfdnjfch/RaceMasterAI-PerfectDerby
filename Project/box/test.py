# importing the required module
import datetime
import calendar
import time

t=datetime.datetime(2022, 12, 25, 0, 0, 0)
print(calendar.timegm(t.timetuple()))


t=datetime.datetime(2023, 1, 3, 15, 58, 0)
print(calendar.timegm(t.timetuple()))
print(time.time())