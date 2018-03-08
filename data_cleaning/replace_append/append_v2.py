# get correct coop and work id
# Deal with duplicates
# handle multiple rows to append
# handle empty fields
# handle people with same names and year (if they are the same, check the previous position to see if they are the same)
import pandas as pd
import numpy as np

# from math import isnan

if __name__ == '__main__':

    masterFile = pd.read_csv("ece.csv")
    newFile = pd.read_csv("ece-new.csv")

    # masterFile = masterFile.fillna()
    # newFile = newFile.fillna()

    masterDict = {}
    newDict = {}
    idDict = {}
    for index, row in masterFile.iterrows():
        if (len(str(row['Name']).strip()) > 0 and not pd.isnull(row['Name'])) and (len(str(row['Year']).strip()) == 4) \
                and (len(str(row['Company']).strip()) > 0 and not pd.isnull(row['Company'])) and \
                (len(str(row['Position']).strip()) > 0 and not pd.isnull(row['Position'])):

            masterDict[row['Name'], row['Year'], row['Company'], row['Position']] = index
            idDict[row['Name'], row['Year']] = row['ID']

    for index, row in newFile.iterrows():
        # print(pd.isnull(row['Position']))
        if (len(str(row['Name']).strip()) > 0 and not pd.isnull(row['Name'])) and (len(str(row['Year']).strip()) == 4) \
                and (len(str(row['Company']).strip()) > 0 and not pd.isnull(row['Company'])) and \
                (len(str(row['Position']).strip()) > 0 and not pd.isnull(row['Position'])):

            newDict[row['Name'], row['Year'], row['Company'], row['Position']] = 1

    newRows = []
    count = 1
    max_id = masterFile['ID'].max()
    for k, v in newDict.items():
        if k not in masterDict:
            id_key = (k[0], k[1])
            if (k[0], k[1]) in idDict:
                newRows.append([idDict[id_key], k])
            else:
                newRows.append([max_id + count, k])
                count += 1
    print(newRows)

    for row in newRows:
        temp_df = newFile[(newFile['Name'] == row[1][0]) & (newFile['Year'] == row[1][1])]
        temp_df = temp_df.drop_duplicates(subset=['Name', 'Year', 'Company', 'Position'])
        for index, temp_row in temp_df.iterrows():
            if (temp_row['Name'], temp_row['Year'], temp_row['Company'], temp_row['Position']) in masterDict:
                # print("replace")
                temp_new_df = newFile[(newFile['Name'] == temp_row['Name']) &
                                            (newFile['Year'] == temp_row['Year']) &
                                            (newFile['Company'] == temp_row['Company']) &
                                            (newFile['Position'] == temp_row['Position'])]
                index_to_replace = \
                    masterDict[(temp_row['Name'], temp_row['Year'], temp_row['Company'], temp_row['Position'])]
                # print(index_to_replace)
                # print(temp_new_df)
                # print(temp_master_df.index.values)
                if len(temp_new_df) > 0:
                    masterFile.loc[index_to_replace, :] = temp_row
                    masterFile.loc[index_to_replace, 'ID'] = row[0]
            else:
                # print("append")
                index_to_append = len(masterFile)
                masterFile.loc[index, ['Name', 'Year', 'Company', 'Position', 'URL', 'Duration', 'Start.Month',
                                       'Start.Year', 'End.Date.pres', 'End.Month', 'End.Year', 'Full.Location',
                                       'City', 'Country', 'Start.Date']] = \
                    temp_row[['Name', 'Year', 'Company', 'Position', 'URL', 'Duration', 'Start.Month', 'Start.Year',
                              'End.Date.pres', 'End.Month', 'End.Year', 'Full.Location', 'City','Country','Start.Date']]

                masterFile.loc[index, 'ID'] = row[0]
                # masterFile = pd.concat([masterFile, temp_row], axis=0)

    masterFile.to_csv('masterfile_replace_append.csv', index=False)