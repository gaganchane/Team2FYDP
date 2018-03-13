from datetime import datetime
import pandas as pd


# date_format = "%m/%d/%Y"
# a = datetime.strptime('08/18/2008', date_format)
# b = datetime.strptime('09/26/2008', date_format)
# delta = b - a
# print(delta.days)
#
#
# now = datetime.now().year
# print(now)

a = datetime(year=2012, month=2, day=9)
b = datetime(year=2013, month=3, day=10)
delta = b-a
print(round((delta.days/365),1))

a = datetime(year=datetime.now().year, month=datetime.now().month, day=1)
print(a)

