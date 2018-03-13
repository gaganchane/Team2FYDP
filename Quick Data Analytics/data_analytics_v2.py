import pandas as pd
import numpy as np

filepath = 'mgmt_data_v5'

all_df = pd.read_csv(filepath + '.csv')
# print(all_df)



coop_df = all_df[all_df['Type'] == 'COOP']
# print(coop_df)

num_of_id = len(all_df.ID.unique())
print('Number of ids are', num_of_id)

work_df = all_df[all_df['Type'] == 'WORK']
work_df = work_df.drop_duplicates()
# print(work_df)
# print('len of work is', len(work_df))
print('total number of ID who have jobs after graduation', len(work_df.ID.unique()))
alumni_job_coop = []

for index, row in work_df.iterrows():
    temp_df = coop_df[(coop_df['ID'] == row['ID']) & (coop_df['Company'] == row['Company'])]
    # print(temp_df)
    for index_2, row_2 in temp_df.iterrows():
        if (row['Company'] == row_2['Company']) and (row['ID'] not in alumni_job_coop):
            alumni_job_coop.append(row['ID'])

print('\n')
print(alumni_job_coop)
print('Number of alumni that worked in the same companies as their coops after graduation are:', len(alumni_job_coop))
print('Percentage of alumni that worked in the same companies as their coops after graduation are:', len(alumni_job_coop)/num_of_id)
# print(all_df)

# print(work_df)
first_work_df = work_df[work_df['WORK_ID'] == 1]
# print(first_work_df)
list_ID = coop_df.ID.unique()
last_coop_df = coop_df
last_coop_df['Last Coop'] = 0
# print(list_ID)

for i in list_ID:
    temp_df = coop_df[(coop_df['ID'] == i)]
    last_coop_ID = temp_df.COOP_ID.max()
    # print(last_coop_ID)
    # print(last_coop_df[(last_coop_df.ID == i) & (last_coop_df.COOP_ID == last_coop_ID)])
    # last_coop_df['Last Coop'] = np.where(last_coop_df[(last_coop_df.ID == i)
    #                                                   & (last_coop_df.COOP_ID == last_coop_ID)], 1, 0)

    index = temp_df[temp_df['COOP_ID'] == last_coop_ID].index.values[0]
    # print(index)
    last_coop_df.loc[index, "Last Coop"] = 1

last_coop_df = last_coop_df[last_coop_df['Last Coop'] == 1]
# print(last_coop_df)

alumni_first_job_last_coop = []
for index, row in first_work_df.iterrows():
    temp_df = last_coop_df[(last_coop_df['ID'] == row['ID']) & (last_coop_df['Company'] == row['Company'])]

    for index_2, row_2 in temp_df.iterrows():
        # print(row['Company'], row_2['Company'])
        if (row['Company'] == row_2['Company']) and (row['ID'] not in alumni_first_job_last_coop):
            alumni_first_job_last_coop.append(row['ID'])


print('\n')
print(alumni_first_job_last_coop)
print('Number of alumni who worked at their last coop after graduation is:', len(alumni_first_job_last_coop))
print('Percentage of alumni who worked at their last coop after graduation is:', len(alumni_first_job_last_coop)/num_of_id)
print('\n')
print('Percentage of Management Engineers with jobs after graduation:', len(work_df.ID.unique())/num_of_id)

