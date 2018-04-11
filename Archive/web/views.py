from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import math
import numpy as nm
from numpy import array
from geopy.geocoders import Nominatim
from geotext import GeoText
from django.contrib import messages


def form(request):
    return render(request, "form.html")

def home(request):
    return render(request, "home.html")

def loading(request):
    return render(request, "loading.html")

def upload(request):
    if request.POST and request.FILES:
        messages.success(request, 'Files are now being transformed...')
        print(request)
        print(request.POST)
        print(request.FILES)
        print(request.FILES.getlist("files"))
        print(request.FILES.getlist("master"))
        return beginTransform(request.FILES.getlist("files"), request.FILES.getlist("master"))
    else:
        messages.success(request, 'Files are now being transformed...')
        return render(request,"error.html")          

        # print(request.FILES.getlist("files")[0])
        # file = request.FILES.getlist("files")[0]
        # data = pd.DataFrame()
        # data = pd.read_csv(file)
        # print(data)
        # data.to_csv(path_or_buf=file,sep=';',float_format='%.2f',index=False,decimal=",")
        # print(results)

def beginTransform(alma_data, oldFile):
        def date_format(duration):
            month_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07",
                         "Aug": "08", "Sep": "09",
                         "Oct": "10", "Nov": "11", "Dec": "12"}
            emp_duration_split = duration.split(" - ")
            start_duration_split = emp_duration_split[0].split(" ")
            if len(start_duration_split) == 2:
                start_month = start_duration_split[0]
                start_year = start_duration_split[1]

                if emp_duration_split[1] == "Present":
                    end_duration_split = "pres"
                    end_month = "pres"
                    end_year = "pres"
                else:
                    end_duration_split = emp_duration_split[1].split(" ")
                    if len(end_duration_split) == 2:
                        end_month = end_duration_split[0]
                        end_year = end_duration_split[1]
                    else:
                        end_month = None
                        end_year = end_duration_split[0]

                start_month_num = month_dic[start_month]
                start_date = start_month_num + "/" + start_year

                if end_month is not None:
                    if end_month == "pres":
                        end_month_num = "pres"
                    else:
                        end_month_num = month_dic[end_month]
                else:
                    end_month_num = None

                if end_month_num == "pres":
                    end_date = end_month_num
                elif end_month_num is not None:
                    end_date = end_month_num + "/" + end_year
                else:
                    end_date = end_year

                final_duration = start_date + "-" + end_date
            else:
                start_date = emp_duration_split[0]
                start_month_num = None
                start_year = emp_duration_split[0]

                if emp_duration_split[1] == "Present":
                    end_date = "pres"
                else:
                    end_date = emp_duration_split[1]

                end_month_num = None

                if emp_duration_split[1] == "Present":
                    end_year = "pres"
                else:
                    end_year = emp_duration_split[1]

                final_duration = start_date + "-" + end_date

            return [final_duration, start_date, start_month_num, start_year, end_date, end_month_num, end_year]

        def input_ids(masterFile):
            masterFile.loc[:, ["WORK_ID", "COOP_ID"]] = None
            masterFile = masterFile.sort_values(by=['ID', 'Start.Year', 'Start.Month'], ascending=True)
            masterFile = masterFile.reset_index(drop=True)

            coopcount = 1
            workcount = 1

            if masterFile.loc[0, "Year"] is not None:
                if str(masterFile.loc[0, "Start.Year"]) < str(masterFile.loc[0, "Year"]) and \
                                str(masterFile.loc[0, "End.Date.pres"]) != "pres":
                    masterFile.loc[0, "COOP_ID"] = coopcount
                    masterFile.loc[0, "WORK_ID"] = None
                    coopcount = coopcount + 1
                else:
                    masterFile.loc[0, "WORK_ID"] = workcount
                    masterFile.loc[0, "COOP_ID"] = None
                    workcount = workcount + 1
            else:
                masterFile.loc[0, "WORK_ID"] = None
                masterFile.loc[0, "COOP_ID"] = None
                workcount = workcount + 1


            for index, row in masterFile.iterrows():

                if index == 0:
                    continue

                if row["ID"] != masterFile.loc[index-1, 'ID']:
                    coopcount = 1
                    workcount = 1

                # if row["Year"] is not None:
                if len(str(row["Year"]).strip()) >= 4:
                    if str(row["Start.Year"]) < str(row["Year"]) and str(row["End.Date.pres"]) != "pres":
                        # print(index, "coop")
                        masterFile.loc[index, "COOP_ID"] = coopcount
                        masterFile.loc[index, "WORK_ID"] = None
                        coopcount = coopcount + 1
                    else:
                        # print(index, "work")
                        masterFile.loc[index, "WORK_ID"] = workcount
                        masterFile.loc[index, "COOP_ID"] = None
                        workcount = workcount + 1
                else:
                    masterFile.loc[index, "WORK_ID"] = None
                    masterFile.loc[index, "COOP_ID"] = None

            # # if row["Year"] is not None:
            #     if len(str(row["Year"]).strip()) >= 4:
            #         if str(row["Start.Year"]) < str(row["Year"]) and str(row["End.Date.pres"]) != "pres":
            #             print(index, "coop")
            #             row["COOP_ID"] = coopcount
            #             row["WORK_ID"] = None
            #             coopcount = coopcount + 1
            #         else:
            #             print(index, "work")
            #             row["WORK_ID"] = workcount
            #             row["COOP_ID"] = None
            #             workcount = workcount + 1
            #     else:
            #         row["WORK_ID"] = None
            #         row["COOP_ID"] = None

            return masterFile

        def append_replace(newFile, masterFile):

            # if ['ID', 'WORK_ID', 'COOP_ID', 'Name', 'URL', 'Year', 'Company', 'Position', 'Duration', 'Start.Date', 'Start.Month'
            #     'Start.Year', 'End.Date.pres', 'End.Month', 'End.Year', 'Full.Location', 'City', 'Country'] in masterFile.columns:

            masterDict = {}
            newDict = {}
            idDict = {}
            for index, row in masterFile.iterrows():
                if not pd.isnull(row['Year']):

                    if (len(str(row['Name']).strip()) > 0 and not pd.isnull(row['Name'])) and (len(str(int(row['Year'])).strip()) == 4) \
                            and (len(str(row['Company']).strip()) > 0 and not pd.isnull(row['Company'])) and \
                            (len(str(row['Position']).strip()) > 0 and not pd.isnull(row['Position'])):

                        masterDict[str(row['Name']), str(int(row['Year'])), str(row['Company']), str(row['Position'])] = index
                        idDict[str(row['Name']), str(int(row['Year']))] = row['ID']

            for index, row in newFile.iterrows():
                if not pd.isnull(row['Year']):
                    if (len(str(row['Name']).strip()) > 0 and not pd.isnull(row['Name'])) and (len(str(int(row['Year'])).strip()) >= 4) \
                            and (len(str(row['Company']).strip()) > 0 and not pd.isnull(row['Company'])) and \
                            (len(str(row['Position']).strip()) > 0 and not pd.isnull(row['Position'])):

                        newDict[str(row['Name']), str(int(row['Year'])), str(row['Company']), str(row['Position'])] = 1

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
            # else:
            #     print('Master file is incorrect. Does not have the appropriate columns.')
            #     masterFile = newFile
            masterFile = input_ids(masterFile)
            return masterFile

        # Main Function/Transform_Script.py starts here
        multiFile = pd.DataFrame([])
        
        if oldFile:
            masterFile = pd.read_csv(oldFile[0])

        for eachFile in alma_data:
            print(eachFile)
            # masterFile = pd.read_csv("masterfile_replace_append.csv")

            alma_data = pd.read_csv(eachFile)

            if not alma_data.empty:
            # alma_data = pd.read_csv("update_mgmt_1.csv")
            # alma_data = pd.read_csv("C:\\Users\\Joash\\Desktop\\University Stuff\\4B uni stuff\\Team2FYDP\\data_cleaning\\"
            #                         "transform\\update_mgmt_1.csv")


                alma_data = alma_data.rename(columns={"Name":"Name",
                                           "Linkedin URL":"Linkedin.URL",
                                           " Education: School 1":"Education..School.1",
                                           "Education: Duration 1":"Education..Duration.1",
                                           " Education: School 2":"Education..School.2",
                                           "Education: Duration 2":"Education..Duration.2",
                                           " Employment: Employer 1":"Employment..Employer.1",
                                           "Employment: Title 1":"Employment..Title.1",
                                           "Employment: Duration 1":"Employment..Duration.1",
                                           "Employment: Location 1":"Employment..Location.1",
                                           " Employment: Employer 2":"Employment..Employer.2",
                                           "Employment: Title 2":"Employment..Title.2",
                                           "Employment: Duration 2":"Employment..Duration.2",
                                           "Employment: Location 2":"Employment..Location.2",
                                           " Employment: Employer 3":"Employment..Employer.3",
                                           "Employment: Title 3":"Employment..Title.3",
                                           "Employment: Duration 3":"Employment..Duration.3",
                                           "Employment: Location 3":"Employment..Location.3",
                                           " Employment: Employer 4":"Employment..Employer.4",
                                           "Employment: Title 4":"Employment..Title.4",
                                           "Employment: Duration 4":"Employment..Duration.4",
                                           "Employment: Location 4":"Employment..Location.4",
                                           " Employment: Employer 5":"Employment..Employer.5",
                                           "Employment: Title 5":"Employment..Title.5",
                                           "Employment: Duration 5":"Employment..Duration.5",
                                           "Employment: Location 5":"Employment..Location.5"})


                relevant_data = alma_data[["Name",
                                           "Linkedin.URL",
                                           "Education..School.1",
                                           "Education..Duration.1",
                                           "Education..School.2",
                                           "Education..Duration.2",
                                           "Employment..Employer.1",
                                           "Employment..Title.1",
                                           "Employment..Duration.1",
                                           "Employment..Location.1",
                                           "Employment..Employer.2",
                                           "Employment..Title.2",
                                           "Employment..Duration.2",
                                           "Employment..Location.2",
                                           "Employment..Employer.3",
                                           "Employment..Title.3",
                                           "Employment..Duration.3",
                                           "Employment..Location.3",
                                           "Employment..Employer.4",
                                           "Employment..Title.4",
                                           "Employment..Duration.4",
                                           "Employment..Location.4",
                                           "Employment..Employer.5",
                                           "Employment..Title.5",
                                           "Employment..Duration.5",
                                           "Employment..Location.5"]]

                clean_df = pd.DataFrame(columns=["ID", "WORK_ID", "COOP_ID", "Name", "URL", "Year", "Company", "Position", "Duration",
                                                 "Start.Date", "Start.Month", "Start.Year", "End.Date.pres", "End.Month", "End.Year",
                                                 "Full.Location", "City", "Country"])
                # print(len(clean_df))
                count = 0

                for index, row in relevant_data.iterrows():

                    employ_title_lst = [['Employment..Title.1', 'Employment..Employer.1', 'Employment..Duration.1',
                                         "Employment..Location.1"],
                                        ['Employment..Title.2', 'Employment..Employer.2', 'Employment..Duration.2',
                                         "Employment..Location.2"],
                                        ['Employment..Title.3', 'Employment..Employer.3', 'Employment..Duration.3',
                                         "Employment..Location.3"],
                                        ['Employment..Title.4', 'Employment..Employer.4', 'Employment..Duration.4',
                                         "Employment..Location.4"],
                                        ['Employment..Title.5', 'Employment..Employer.5', 'Employment..Duration.5',
                                         "Employment..Location.5"]]

                    for i in employ_title_lst:
                        if len(row[i[0]].strip()) != 0:
                            clean_df.loc[count,"ID"] = index
                            clean_df.loc[count, "WORK_ID"] = index
                            clean_df.loc[count, "COOP_ID"] = index
                            clean_df.loc[count, "Name"] = row["Name"]
                            clean_df.loc[count, "URL"] = row["Linkedin.URL"]

                            # future improvement to make this better
                            if "waterloo" in row['Education..School.2'].lower():
                                if (len(str(row["Education..Duration.2"])) >= 4):
                                    clean_df.loc[count, "Year"] = row["Education..Duration.2"][-4:]
                            elif "waterloo" in row['Education..School.1'].lower():
                                if (len(str(row["Education..Duration.1"])) >= 4):
                                    clean_df.loc[count, "Year"] = row["Education..Duration.1"][-4:]

                            # clean_df.loc[count, "Company"] = row["Employment..Employer.1"]
                            clean_df.loc[count, "Company"] = row[i[1]].replace('&amp;', '&')
                            clean_df.loc[count, "Position"] = row[i[0]].replace('&amp;', '&')
                            a = date_format(row[i[2]])
                            clean_df.loc[count,["Duration",
                                                "Start.Date","Start.Month","Start.Year","End.Date.pres","End.Month","End.Year"]] = a
                            clean_df.loc[count, "Full.Location"] = row[i[3]]
                            clean_df.loc[count, "City"] = None
                            clean_df.loc[count, "Country"] = None
                            count = count + 1

                clean_df = input_ids(clean_df)

                world_cities_df = pd.read_csv("cities_countries.csv")

                geolocator = Nominatim(scheme='http')
                city1 = ""
                country1 = ""
                for index, row in clean_df.iterrows():
                    #geolocator = Nominatim(scheme='http')
                    city1 = ""
                    country1 = ""
                    try:
                        if not pd.isnull(row['Full.Location']):
                            geo = geolocator.geocode(str(row['Full.Location'].replace("Area", "").strip()))
                        else:
                            geo = ""
                        #print(geo)
                        city = GeoText(str(geo).strip()).cities
                        country = GeoText(str(geo).strip()).countries
                        #print(city, country)
                        if len(city) > 0 and len(country) > 0:
                            city1 = city[0]
                            country1 = country[0]
                        elif len(city) > 0:
                            city1 = city[0]
                        elif len(country) > 0:
                            country1 = country[0]
                        else:
                            city1 = ""
                            country1 = ""

                    except:
                        if not pd.isnull(row['Full.Location']):
                            geo = row['Full.Location']
                        else:
                            geo = ""

                        city = GeoText(str(geo)).cities
                        country = GeoText(str(geo)).countries

                        if len(city) > 0 and len(country) > 0:

                            city1 = city[0]
                            country1 = country[0]

                        elif len(country) > 0:
                            df = world_cities_df[(world_cities_df['country'] == country[0])]
                            for city_df in df['name']:
                                #Add spaces between text
                                if city_df.lower() in geo.lower():
                                    city1 = city_df
                                    country1 = country[0]
                                    break
                                else:
                                    city1 = ""
                                    country1 = ""

                        elif len(city) > 0:
                            df = world_cities_df[(world_cities_df['country'] == 'Canada') | (world_cities_df['country'] == 'USA')]
                            for index_x, x in df.iterrows():

                                curr_location = " " + str(geo).lower() + " "
                                spaced_x = " " + x['name'].lower() + " "

                                if spaced_x in curr_location:
                                    country1 = x['country']
                                    city1 = city[0]
                                    break

                        else:
                            for index_y, y in world_cities_df.iterrows():

                                curr_location = " " + str(geo).lower() + " "
                                spaced_y = " " + y['name'].lower() + " "

                                if spaced_y in curr_location:
                                    city1 = y['name']
                                    country1 = y['country']
                                    break

                    row["City"] = city1
                    row["Country"] = country1
                    # print(row["Full.Location"], "|", city1, "|", country1)
                    print("getting location...")

                # print(clean_df)
                clean_df.to_csv("test.csv", index = False)

                if oldFile:
                    masterFile = append_replace(clean_df, masterFile)
                    # masterFile.to_csv('masterfile_replace_append.csv', index=False)
                else:
                    masterFile = clean_df

                # multiFile = multiFile.append(masterFile)
            else:
                print("Input file is empty!")

        # print(multiFile)
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(masterFile.to_csv(index = False), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        return response

        # downloadcsv(multiFile)
        # multiFile.to_csv("multiFile.csv", index = False)
        # clean_df.to_csv("alma-output.csv", index = False)

# def downloadcsv(mergedFile):
#   your_dataframe = pd.Dataframe()

#   response = HttpResponse(content_type='text/csv')
#   response['Content-Disposition'] = 'attachment; filename=filename.csv'

#   results.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")
#   return response

# def Upload(request):
#     for count, x in enumerate(request.FILES.getlist("files")):
#         def process(f):
#             with open('/Users/sunnygaur/Docs/ManagementEngineering/4B/FYDP/alumnize/alumnize' + str(count), 'wb+') as destination:
#                 for chunk in f.chunks():
#                     destination.write(chunk)
#         process(x)
#     return HttpResponse("File(s) uploaded!")

# def index(request):
#     if request.POST and request.FILES:
#         csvfile = request.FILES['csv_file']
#         dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
#         csvfile.open()
#         reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=',', dialect=dialect)

#     return render(request, "index.html", locals())