import pandas as pd

filepath = 'C:\\Users\\Joash\\Desktop\\University Stuff\\4B uni stuff\\Network Graph\\Quick Data Analytics\\mgmt_data_v4'

all_df = pd.read_csv(filepath + '.csv')
# print(all_df)

coop_df = all_df[all_df['Type'] == 'COOP']

num_of_id = len(all_df.ID.unique())
print('Number of ids are', num_of_id)

work_df = all_df[all_df['Type'] == 'WORK']
work_df = work_df.drop_duplicates()
# print(work_df)
print('len of work is', len(work_df))
print('total number of ID who have jobs after graduation', len(work_df.ID.unique()))
alumni_job_coop = []

for index, row in work_df.iterrows():
    temp_df = coop_df[(coop_df['ID'] == row['ID']) & (coop_df['Company'] == row['Company'])]
    for index_2, row_2 in temp_df.iterrows():
        if (row['Company'] == row_2['Company']) and (row['ID'] not in alumni_job_coop):
            alumni_job_coop.append(row['ID'])

print('\n')
print(alumni_job_coop)
print('Number of alumni that worked in the same companies as their coops after graduation are:', len(alumni_job_coop))
print('Percentage of alumni that worked in the same companies as their coops after graduation are:', len(alumni_job_coop)/num_of_id)
# print(all_df)

work_df['Work_Order'] = 1
lst_of_IDs = all_df.ID.unique()

# For loop is used to store the first workplace for each ID
for ID in lst_of_IDs:
    temp_df = work_df[(work_df['ID'] == ID)]
    count = 1
    for index, row in temp_df.iterrows():
        work_df.loc[index, 'Work_Order'] = count
        # print(row['ID'],count)
        count = count + 1

first_work_df = work_df[work_df['Work_Order'] == 1]

alumni_first_job_last_coop = []
for index, row in first_work_df.iterrows():
    temp_df = coop_df[(coop_df['ID'] == row['ID']) & (coop_df['Company'] == row['Company'])]
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


# first_work_df.to_csv(filepath + 'first_work_df.csv')
# first_work_df['Year - Start Year'] = first_work_df['Start Year'] - first_work_df['Year']
# print(first_work_df)
# work_df.to_csv(filepath + '_work_df.csv')
# coop_df.to_csv(filepath + '_coop_df.csv')