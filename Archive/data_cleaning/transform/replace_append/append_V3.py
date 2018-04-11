# get correct coop and work id
# Deal with duplicates
# handle multiple rows to append
# handle empty fields
# handle people with same names and year (if they are the same, check the previous position to see if they are the same)
import pandas as pd
import numpy as np


# from math import isnan
if __name__ == '__main__':

    # masterFile = pd.read_csv("masterfile_replace_append.csv")
    masterFile = pd.read_csv("ece.csv")
    newFile = pd.read_csv("combined_update_mgmt_output_2 - Copy.csv")
    #newFile = pd.read_csv("ece-new.csv")
    # newFile = pd.read_csv("test.csv")
    # newFile = pd.read_csv("combined_update_mgmt_output_3.csv")

    masterDict = {}
    newDict = {}
    idDict = {}
    for index, row in masterFile.iterrows():
        if (len(str(row['Name']).strip()) > 0 and not pd.isnull(row['Name'])) and (len(str(int(row['Year'])).strip()) == 4) \
                and (len(str(row['Company']).strip()) > 0 and not pd.isnull(row['Company'])) and \
                (len(str(row['Position']).strip()) > 0 and not pd.isnull(row['Position'])):

            masterDict[row['Name'], row['Year'], row['Company'], row['Position']] = index
            idDict[row['Name'], row['Year']] = row['ID']

    for index, row in newFile.iterrows():
        if (len(str(row['Name']).strip()) > 0 and not pd.isnull(row['Name'])) and (len(str(int(row['Year'])).strip()) >= 4) \
                and (len(str(row['Company']).strip()) > 0 and not pd.isnull(row['Company'])) and \
                (len(str(row['Position']).strip()) > 0 and not pd.isnull(row['Position'])):

            newDict[row['Name'], row['Year'], row['Company'], row['Position']] = 1


    # Finds all the newrows that need to be appended to the master file
    newRows = []
    count = 1
    max_id = masterFile['ID'].max()
    dup_id_dict = {}
    for k, v in newDict.items():
        if k not in masterDict:
            id_key = (k[0], k[1])
            if (k[0], k[1]) in idDict:
                newRows.append([idDict[id_key], k])
            else:
                newRows.append([max_id + count, k])
                idDict[(k[0], k[1])] = max_id+count
                count += 1
    print(newRows)

    # appends the rows to the master file
    count = 1
    for row in newRows:
        temp_df = newFile[(newFile['Name'] == row[1][0]) & (newFile['Year'] == row[1][1]) &
                          (newFile['Company'] == row[1][2]) & (newFile['Position'] == row[1][3])]
        temp_df = temp_df.drop_duplicates(subset=['Name', 'Year', 'Company', 'Position'])
        for index, temp_row in temp_df.iterrows():
            print("appending...", temp_row['Name'], temp_row['Year'], temp_row['Company'], temp_row['Position'])
            temp_row['ID'] = row[0]
            masterFile = masterFile.append(temp_row[['ID', 'Name', 'Year', 'Company', 'Position', 'URL', 'Duration',
                                                     'Start.Month', 'Start.Year', 'End.Date.pres', 'End.Month',
                                                     'End.Year', 'Full.Location', 'City','Country','Start.Date']])

    # Replaces rows in the master file for people who are appended
    done = {}
    for row in newRows:
        if row[0] not in done:
            temp_df = newFile[(newFile['Name'] == row[1][0]) & (newFile['Year'] == row[1][1])]
            temp_df = temp_df.drop_duplicates(subset=['Name', 'Year', 'Company', 'Position'])
            for index, temp_row in temp_df.iterrows():
                if (temp_row['Name'], temp_row['Year'], temp_row['Company'], temp_row['Position']) in masterDict:
                    print("replacing...", temp_row['Name'], temp_row['Year'], temp_row['Company'], temp_row['Position'])
                    temp_new_df = newFile[(newFile['Name'] == temp_row['Name']) &
                                          (newFile['Year'] == temp_row['Year']) &
                                          (newFile['Company'] == temp_row['Company']) &
                                          (newFile['Position'] == temp_row['Position'])]
                    index_to_replace = \
                        masterDict[(temp_row['Name'], temp_row['Year'], temp_row['Company'], temp_row['Position'])]

                    if len(temp_new_df) > 0:
                        masterFile.loc[index_to_replace, :] = temp_row
                        masterFile.loc[index_to_replace, 'ID'] = row[0]
            done[row[0]] = 1


    masterFile.to_csv('masterfile_replace_append.csv', index=False)