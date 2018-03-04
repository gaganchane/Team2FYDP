# Current input file is combined_update_mgmt_output_3
# I manually removed all NA and NA-NA from the input file; combined_update_mgmt_output_3
# I changed all Present to pres; combined_update_mgmt_output_3
# The WORK_ID and COOP_ID columns are incorrect in this file; combined_update_mgmt_output_3
import pandas as pd
import numpy as np

filepath = 'C:\\Users\\Joash\\Desktop\\University Stuff\\4B uni stuff\\Network Graph\\Hackathon' \
           '\\combined_update_mgmt_output_3'

all_df = pd.read_csv(filepath + '.csv')
# print(all_df)

all_df["Current Position"] = np.where(all_df['End.Date.pres']=='pres', True, False)

count_curr_ft = all_df[all_df["Current Position"] == True]["ID"].drop_duplicates().count()

# all_df[all_df["Current Position"] == True]["ID"].drop_duplicates().to_csv(filepath + '_result.csv')

print("Total number of Management Engineers in the dataset are", all_df["ID"].drop_duplicates().count())
print("Total number of Management Engineers that currently have full time employment are", count_curr_ft)
print()


c1 = 0
c2 = 0
for i in range(2012,2018,1):

    df1 = all_df[(all_df['Year'] == i)]
    df2 = all_df[(all_df['Year'] == i) & (all_df['Current Position'] == True)]

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

    count_canada = all_df[(all_df['Year'] == i) & (all_df['Country'] == "Canada") &
                          (all_df['Current Position'] == True)]['ID'].drop_duplicates().count()
    count_usa = all_df[(all_df['Year'] == i) & (all_df['Country'] == "United States") &
                          (all_df['Current Position'] == True)]['ID'].drop_duplicates().count()
    count_not_null = all_df[(all_df['Year'] == i) & (all_df.Country.notnull()) &
                          (all_df['Current Position'] == True)]['ID'].drop_duplicates().count()
    print("The number of Alumnus who have provide location of their workplace are", count_not_null,".",
          count_canada, "of the alumnus from class", i, "work in Canada,", round(count_canada/count_not_null,2),
          count_usa, "of the alumnus work in USA,", round(count_usa/count_not_null,2))


