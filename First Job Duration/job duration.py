import pandas as pd
import datetime as dt
from dateutil import relativedelta
import numpy as np
import matplotlib.pyplot as plt

# month = abs(relativedelta.relativedelta(dt.date(2012, 12, 1), dt.date(2018, 1, 1)).months)
# year = abs(relativedelta.relativedelta(dt.date(2012, 12, 1), dt.date(2012, 1, 1)).years)
# print(year*12+month)

filepath = 'C:\\Users\\Joash\\Desktop\\University Stuff\\4B uni stuff\\Network Graph\\Job Duration Histogram\\mgmt_data_v5'

all_df = pd.read_csv(filepath + '.csv')

# dataframe with jobs after graduation
work_df = all_df[all_df['Type'] == 'WORK']
work_df = work_df.drop_duplicates()
# print(work_df)

# dataframe with only the first jobs after graduation
first_work_df = work_df[work_df['WORK_ID'] == 1]
# print(first_work_df)

#checking if any of the ID have duplicates
print(first_work_df.ID.drop_duplicates().shape[0])

# Taking out all work experiences that does not have a start month
start_work = first_work_df[first_work_df['Start Month'] > 0]
print('Took out',first_work_df.shape[0]-start_work.shape[0], 'jobs.')

# date = dt.date(2009, 12,1)
# print(date)

# dummy_df used for the for loop below
dummy_df = start_work

# print(dt.datetime.now().month)

# The for loop makes datetime objects using the data and then gets the job duration
for index, row in dummy_df.iterrows():
    start_work.loc[index, 'Start Datetime'] = dt.date(int(row['Start Year']), int(row['Start Month']),1)
    if row['End Year'] != 'pres':
        start_work.loc[index, 'End Datetime'] = dt.date(int(row['End Year']), int(row['End Month']), 1)
        start_work.loc[index, 'Job Duration'] = relativedelta.relativedelta(
            dt.date(int(row['End Year']), int(row['End Month']), 1),
            dt.date(int(row['Start Year']), int(row['Start Month']),1)).months + (relativedelta.relativedelta(
            dt.date(int(row['End Year']), int(row['End Month']), 1),
            dt.date(int(row['Start Year']), int(row['Start Month']),1)).years)*12
    else:
        start_work.loc[index, 'End Datetime'] = dt.date(dt.datetime.now().year, dt.datetime.now().month, 1)
        start_work.loc[index, 'Job Duration'] = abs(relativedelta.relativedelta(
            dt.date(int(row['Start Year']), int(row['Start Month']),1),
            dt.date(dt.datetime.now().year, dt.datetime.now().month, 1)).months) + abs(relativedelta.relativedelta(
            dt.date(int(row['Start Year']), int(row['Start Month']),1),
            dt.date(dt.datetime.now().year, dt.datetime.now().month, 1)).years)*12

# print(start_work)

start_work_2012 = start_work[start_work['Year'] == 2012]
start_work_2013 = start_work[start_work['Year'] == 2013]
start_work_2014 = start_work[start_work['Year'] == 2014]
start_work_2015 = start_work[start_work['Year'] == 2015]
start_work_2016 = start_work[start_work['Year'] == 2016]
start_work_2017 = start_work[start_work['Year'] == 2017]
# print(start_work_2012)
# start_work_2012.to_csv(filepath + '_test_.csv')

# start_work['datetime'] = dt.date(int(start_work['Start Year']), int(start_work['Start Month']), 1)

plt_2012 = start_work_2012['Job Duration'].hist(bins=10)
plt_2012.set_xlabel("Duration (Months)")
plt_2012.set_ylabel("Count")
plt_2012.set_title('2012 First Job Duration')
plt.show()

plt_2013 = start_work_2013['Job Duration'].hist(bins=8)
plt_2013.set_xlabel("Duration (Months)")
plt_2013.set_ylabel("Count")
plt_2013.set_title('2013 First Job Duration')
plt.show()

plt_2014 = start_work_2014['Job Duration'].hist(bins=10)
plt_2014.set_xlabel("Duration (Months)")
plt_2014.set_ylabel("Count")
plt_2014.set_title('2014 First Job Duration')
plt.show()

plt_2015 = start_work_2015['Job Duration'].hist(bins=8)
plt_2015.set_xlabel("Duration (Months)")
plt_2015.set_ylabel("Count")
plt_2015.set_title('2015 First Job Duration')
plt.show()

plt_2016 = start_work_2016['Job Duration'].hist(bins=8)
plt_2016.set_xlabel("Duration (Months)")
plt_2016.set_ylabel("Count")
plt_2016.set_title('2016 First Job Duration')
plt.show()

plt_2017 = start_work_2017['Job Duration'].hist(bins=5)
plt_2017.set_xlabel("Duration (Months)")
plt_2017.set_ylabel("Count")
plt_2017.set_title('2017 First Job Duration')
plt.show()