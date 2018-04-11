# Current input file is mgmt_data_clean

import pandas as pd
import numpy as np
import csv

# filepath = 'C:\\Users\\Joash\\Desktop\\University Stuff\\4B uni stuff\\Network Graph\\Hackathon' \
#            '\\combined_update_mgmt_output_3'
filepath = 'C:\\Users\\Joash\\Desktop\\University Stuff\\4B uni stuff\\Network Graph\\Hackathon' \
           '\\mgmt_data_clean'

read_file = open(filepath + '.csv', 'r', encoding='latin1')
csv_read = csv.reader(read_file)
firstline = True
data = []
for row in csv_read:
    if firstline == True:
        firstline = False
        continue
    data.append(row)


# print(data)
# Uncomment this if for mgmt_data_clean
all_df = pd.DataFrame(data, columns=['ID', 'WORK_ID', 'COOP_ID', 'Name', 'URL', 'Year', 'Type', 'Company', 'Industry',
                                     'Position', 'Clean Position Name', 'Duration', 'Start Date', 'Start Month',
                                     'Start Year', 'End.Date.pres', 'End Month', 'End Year', 'Full Location', 'City'
                                     , 'Province', 'Country'])
# print(all_df)

#Uncoment this for combined_update_mgmt_output_3
# all_df = pd.read_csv(filepath + '.csv')
# print(all_df)

all_df["Current Position"] = np.where(all_df['End.Date.pres']=='pres', True, False)

count_curr_ft = all_df[all_df["Current Position"] == True]["ID"].drop_duplicates().count()

# all_df[all_df["Current Position"] == True]["ID"].drop_duplicates().to_csv(filepath + '_result.csv')

print("Total number of Management Engineers in the dataset are", all_df["ID"].drop_duplicates().count())
print("Total number of Management Engineers that currently have full time employment are", count_curr_ft)
print()


c1 = 0
c2 = 0
# print(all_df[(all_df['Year'] == "2012")])
for i in range(2012,2018,1):

    df1 = all_df[(all_df['Year'] == str(i))]
    df2 = all_df[(all_df['Year'] == str(i)) & (all_df['Current Position'] == True)]
    count_all = df1['ID'].drop_duplicates().count()
    count_curr = df2['ID'].drop_duplicates().count()
    print("Number of Alumni from", i, "grad class that currently have jobs are", count_curr, "out of", count_all, ",",
          count_curr/count_all)
    c1 += count_curr
    c2 += count_all

print()
print("Total number of alumni that currently have full-time are", c1, "out of", c2)
print()


# all_df_loc = all_df[(all_df.Country.notnull()) & (all_df["Current Position"] == True)]

for i in range(2012,2018,1):

    count_canada = all_df[(all_df['Year'] == str(i)) & (all_df['Country'] == "Canada") &
                          (all_df['Current Position'] == True)]['ID'].drop_duplicates().count()
    count_usa = all_df[(all_df['Year'] == str(i)) & (all_df['Country'] == "United States") &
                          (all_df['Current Position'] == True)]['ID'].drop_duplicates().count()
    count_not_null = all_df[(all_df['Year'] == str(i)) & (all_df.Country != "") &
                          (all_df['Current Position'] == True)]['ID'].drop_duplicates().count()
    print("The number of Alumnus who have provide location of their workplace are", count_not_null,".",
          count_canada, "of the alumnus from class", i, "work in Canada,", round(count_canada/count_not_null,2),
          count_usa, "of the alumnus work in USA,", round(count_usa/count_not_null,2))


