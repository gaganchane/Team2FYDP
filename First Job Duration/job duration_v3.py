import pandas as pd
import datetime as dt
from dateutil import relativedelta
import numpy as np
from matplotlib import pyplot as plt

# month = abs(relativedelta.relativedelta(dt.date(2012, 12, 1), dt.date(2018, 1, 1)).months)
# year = abs(relativedelta.relativedelta(dt.date(2012, 12, 1), dt.date(2012, 1, 1)).years)
# print(year*12+month)

filepath = 'C:\\Users\\Joash\\Desktop\\University Stuff\\4B uni stuff\\Network Graph\\Job Duration Histogram\\mgmt_data_v5'

all_df = pd.read_csv(filepath + '.csv')

# dataframe with jobs after graduation
work_df = all_df[all_df['Type'] == 'WORK']
work_df = work_df.drop_duplicates()


# used ID's of people wh have had switched from their first job
start_work = work_df[work_df['WORK_ID'] == 1]
start_work = start_work[start_work['Start Month'] > 0]
# start_work.to_csv(filepath + "_start_work_.csv")

print('Number of Alumni that have switch jobs are:',len(start_work[start_work['End Year'] != 'pres']))

dummy_df = start_work

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
        start_work.loc[index, 'Curr Datetime'] = dt.date(2017, 7, 1)
        start_work.loc[index, 'Curr Job Duration'] = abs(relativedelta.relativedelta(
            dt.date(int(row['Start Year']), int(row['Start Month']),1),
            dt.date(dt.datetime.now().year, dt.datetime.now().month, 1)).months) + abs(relativedelta.relativedelta(
            dt.date(int(row['Start Year']), int(row['Start Month']),1),
            dt.date(2017, 7, 1)).years)*12

# print(start_work)
# start_work.to_csv(filepath + "_start_work_.csv")

start_work_2012 = start_work[start_work['Year'] == 2012]
start_work_2013 = start_work[start_work['Year'] == 2013]
start_work_2014 = start_work[start_work['Year'] == 2014]
start_work_2015 = start_work[start_work['Year'] == 2015]
start_work_2016 = start_work[start_work['Year'] == 2016]
start_work_2017 = start_work[start_work['Year'] == 2017]
# print(start_work_2017)


plt_2012 = plt.figure()
n_bins = 10
x1_2012 = start_work_2012['Job Duration'][start_work_2012['Job Duration'] > 0].tolist()
x2_2012 = start_work_2012['Curr Job Duration'][start_work_2012['Curr Job Duration'] > 0].tolist()
# print(x2_2012)
x = np.array([x1_2012, x2_2012])
plt.hist(x, n_bins, histtype='bar', stacked=True, figure=plt_2012)
plt.ylabel('Count', figure=plt_2012)
plt.xlabel('Job Duration', figure=plt_2012)
plt.title('2012 Job Duration', figure=plt_2012)
plt.legend(['Job Duration', 'Current Job Duration'])
plt.ylim((0,8))
plt.grid(True)
plt.show()

plt_2013 = plt.figure()
n_bins = 10
x1_2013 = start_work_2013['Job Duration'][start_work_2013['Job Duration'] > 0].tolist()
x2_2013 = start_work_2013['Curr Job Duration'][start_work_2013['Curr Job Duration'] > 0].tolist()
# print(x2_2013)
x = np.array([x1_2013, x2_2013])
plt.hist(x, n_bins, histtype='bar', stacked=True, figure=plt_2013)
plt.ylabel('Count', figure=plt_2013)
plt.xlabel('Job Duration', figure=plt_2013)
plt.title('2013 Job Duration', figure=plt_2013)
plt.legend(['Job Duration', 'Current Job Duration'])
plt.ylim((0,9))
plt.grid(True)
plt.show()

plt_2014 = plt.figure()
n_bins = 10
x1_2014 = start_work_2014['Job Duration'][start_work_2014['Job Duration'] > 0].tolist()
x2_2014 = start_work_2014['Curr Job Duration'][start_work_2014['Curr Job Duration'] > 0].tolist()
# print(x2_2014)
x = np.array([x1_2014, x2_2014])
plt.hist(x, n_bins, histtype='bar', stacked=True, figure=plt_2014)
plt.ylabel('Count', figure=plt_2014)
plt.xlabel('Job Duration', figure=plt_2014)
plt.title('2014 Job Duration', figure=plt_2014)
plt.legend(['Job Duration', 'Current Job Duration'])
plt.ylim((0,9))
plt.grid(True)
plt.show()

plt_2015 = plt.figure()
n_bins = 10
x1_2015 = start_work_2015['Job Duration'][start_work_2015['Job Duration'] > 0].tolist()
x2_2015 = start_work_2015['Curr Job Duration'][start_work_2015['Curr Job Duration'] > 0].tolist()
# print(x2_2015)
x = np.array([x1_2015, x2_2015])
plt.hist(x, n_bins, histtype='bar', stacked=True, figure=plt_2015)
plt.ylabel('Count', figure=plt_2015)
plt.xlabel('Job Duration', figure=plt_2015)
plt.title('2015 Job Duration', figure=plt_2015)
plt.legend(['Job Duration', 'Current Job Duration'])
plt.grid(True)
plt.show()

plt_2016 = plt.figure()
n_bins = 10
x1_2016 = start_work_2016['Job Duration'][start_work_2016['Job Duration'] > 0].tolist()
x2_2016 = start_work_2016['Curr Job Duration'][start_work_2016['Curr Job Duration'] > 0].tolist()
# print(x2_2016)
x = np.array([x1_2016, x2_2016])
plt.hist(x, n_bins, histtype='bar', stacked=True, figure=plt_2016)
plt.ylabel('Count', figure=plt_2016)
plt.xlabel('Job Duration', figure=plt_2016)
plt.title('2016 Job Duration', figure=plt_2016)
plt.legend(['Job Duration', 'Current Job Duration'])
plt.grid(True)
# plt.ylim((0,9))
plt.show()

plt_2017 = plt.figure()
n_bins = 10
x1_2017 = start_work_2017['Job Duration'][start_work_2017['Job Duration'] > 0].tolist()
x2_2017 = start_work_2017['Curr Job Duration'][start_work_2017['Curr Job Duration'] > 0].tolist()
# print(x2_2017)
x = np.array([x1_2017, x2_2017])
plt.hist(x, n_bins, histtype='bar', stacked=True, figure=plt_2017)
plt.ylabel('Count', figure=plt_2017)
plt.xlabel('Job Duration', figure=plt_2017)
plt.title('2017 Job Duration', figure=plt_2017)
plt.legend(['Job Duration', 'Current Job Duration'])
plt.grid(True)
# plt.ylim((0,9))
plt.show()