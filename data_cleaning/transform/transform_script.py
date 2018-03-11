import pandas as pd
import math
import numpy as nm
from numpy import array
from geopy.geocoders import Nominatim
from geotext import GeoText

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

if __name__ == '__main__':

    alma_data = pd.read_csv("update_mgmt_5.csv")

    # print(alma_data)

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
    # print(relevant_data)
    # print(relevant_data.iloc[3]['Employment..Location.1'])
    clean_df = pd.DataFrame(columns=["ID", "WORK_ID", "COOP_ID", "Name", "URL", "Year", "Company", "Position", "Duration",
                                     "Start.Date", "Start.Month", "Start.Year", "End.Date.pres", "End.Month", "End.Year",
                                     "Full.Location", "City", "Country"])
    # print(len(clean_df))
    count = 0

    for index, row in relevant_data.iterrows():


        # if row['Employment..Title.1'] is not None:
        if len(row['Employment..Title.1'].strip()) != 0:
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
            clean_df.loc[count, "Company"] = row["Employment..Employer.1"].replace('&amp;', '&')
            clean_df.loc[count, "Position"] = row["Employment..Title.1"].replace('&amp;', '&')
            a = date_format(row["Employment..Duration.1"])
            clean_df.loc[count,["Duration",
                                "Start.Date","Start.Month","Start.Year","End.Date.pres","End.Month","End.Year"]] = a
            clean_df.loc[count, "Full.Location"] = row["Employment..Location.1"]
            clean_df.loc[count, "City"] = None
            clean_df.loc[count, "Country"] = None
            count = count + 1



        # if row['Employment..Title.2'] is not None:
        if len(row['Employment..Title.2'].strip()) != 0:
            clean_df.loc[count,"ID"] = index
            clean_df.loc[count, "WORK_ID"] = index
            clean_df.loc[count, "COOP_ID"] = index
            clean_df.loc[count, "Name"] = row["Name"]
            clean_df.loc[count, "URL"] = row["Linkedin.URL"]

            if "waterloo" in row['Education..School.2'].lower():
                if (len(str(row["Education..Duration.2"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.2"][-4:]
            elif "waterloo" in row['Education..School.1'].lower():
                if (len(str(row["Education..Duration.1"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.1"][-4:]

            clean_df.loc[count, "Company"] = row["Employment..Employer.2"].replace('&amp;', '&')
            clean_df.loc[count, "Position"] = row["Employment..Title.2"].replace('&amp;', '&')
            a = date_format(row["Employment..Duration.2"])
            clean_df.loc[count,["Duration",
                                "Start.Date","Start.Month","Start.Year","End.Date.pres","End.Month","End.Year"]] = a
            clean_df.loc[count, "Full.Location"] = row["Employment..Location.2"]
            clean_df.loc[count, "City"] = None
            clean_df.loc[count, "Country"] = None
            count = count + 1

        # if row['Employment..Title.3'] is not None:
        if len(row['Employment..Title.3'].strip()) != 0:
            clean_df.loc[count,"ID"] = index
            clean_df.loc[count, "WORK_ID"] = index
            clean_df.loc[count, "COOP_ID"] = index
            clean_df.loc[count, "Name"] = row["Name"]
            clean_df.loc[count, "URL"] = row["Linkedin.URL"]

            if "waterloo" in row['Education..School.2'].lower():
                if (len(str(row["Education..Duration.2"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.2"][-4:]
            elif "waterloo" in row['Education..School.1'].lower():
                if (len(str(row["Education..Duration.1"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.1"][-4:]

            clean_df.loc[count, "Company"] = row["Employment..Employer.3"].replace('&amp;', '&')
            clean_df.loc[count, "Position"] = row["Employment..Title.3"].replace('&amp;', '&')
            a = date_format(row["Employment..Duration.3"])
            clean_df.loc[count,["Duration",
                                "Start.Date","Start.Month","Start.Year","End.Date.pres","End.Month","End.Year"]] = a
            clean_df.loc[count, "Full.Location"] = row["Employment..Location.3"]
            clean_df.loc[count, "City"] = None
            clean_df.loc[count, "Country"] = None
            count = count + 1

        # if row['Employment..Title.4'] is not None:
        if len(row['Employment..Title.4'].strip()) != 0:
            clean_df.loc[count,"ID"] = index
            clean_df.loc[count, "WORK_ID"] = index
            clean_df.loc[count, "COOP_ID"] = index
            clean_df.loc[count, "Name"] = row["Name"]
            clean_df.loc[count, "URL"] = row["Linkedin.URL"]

            if "waterloo" in row['Education..School.2'].lower():
                if (len(str(row["Education..Duration.2"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.2"][-4:]
            elif "waterloo" in row['Education..School.1'].lower():
                if (len(str(row["Education..Duration.1"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.1"][-4:]

            clean_df.loc[count, "Company"] = row["Employment..Employer.4"].replace('&amp;', '&')
            clean_df.loc[count, "Position"] = row["Employment..Title.4"].replace('&amp;', '&')
            a = date_format(row["Employment..Duration.4"])
            clean_df.loc[count,["Duration",
                                "Start.Date","Start.Month","Start.Year","End.Date.pres","End.Month","End.Year"]] = a
            clean_df.loc[count, "Full.Location"] = row["Employment..Location.4"]
            clean_df.loc[count, "City"] = None
            clean_df.loc[count, "Country"] = None
            count = count + 1

        # if row['Employment..Title.5'].strip() is not None:
        if len(row['Employment..Title.5'].strip()) != 0:
            clean_df.loc[count,"ID"] = index
            clean_df.loc[count, "WORK_ID"] = index
            clean_df.loc[count, "COOP_ID"] = index
            clean_df.loc[count, "Name"] = row["Name"]
            clean_df.loc[count, "URL"] = row["Linkedin.URL"]

            if "waterloo" in row['Education..School.2'].lower():
                if (len(str(row["Education..Duration.2"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.2"][-4:]
            elif "waterloo" in row['Education..School.1'].lower():
                if (len(str(row["Education..Duration.1"])) >= 4):
                    clean_df.loc[count, "Year"] = row["Education..Duration.1"][-4:]

            clean_df.loc[count, "Company"] = row["Employment..Employer.5"].replace('&amp;', '&')
            clean_df.loc[count, "Position"] = row["Employment..Title.5"].replace('&amp;', '&')
            a = date_format(row["Employment..Duration.5"])
            clean_df.loc[count,["Duration",
                                "Start.Date","Start.Month","Start.Year","End.Date.pres","End.Month","End.Year"]] = a
            clean_df.loc[count, "Full.Location"] = row["Employment..Location.5"]
            clean_df.loc[count, "City"] = None
            clean_df.loc[count, "Country"] = None
            count = count + 1

clean_df = clean_df.sort_values(by=['ID', 'Start.Year', 'Start.Month'], ascending=True)
clean_df = clean_df.reset_index(drop=True)

coopcount = 1
workcount = 1

if clean_df.loc[0, "Year"] is not None:
    if clean_df.loc[0, "Start.Year"] < clean_df.loc[1, "Year"] and clean_df.loc[1, "End.Date.pres"] != "pres":
        clean_df.loc[0, "COOP_ID"] = coopcount
        clean_df.loc[0, "WORK_ID"] = None
        coopcount = coopcount + 1
    else:
        clean_df.loc[0, "WORK_ID"] = workcount
        clean_df.loc[0, "COOP_ID"] = None
        workcount = workcount + 1
else:
    clean_df.loc[0, "WORK_ID"] = workcount
    clean_df.loc[0, "COOP_ID"] = None
    workcount = workcount + 1


for index, row in clean_df.iterrows():

    if index == 0:
        continue

    #print(clean_df.loc[index-1, 'ID'], clean_df.loc[index-1, 'Name'], clean_df.loc[index-1, 'Position'])
    # if len(str(row['Year'])) < 4:
    #     coopcount = 0
    #     workcount = 0
    if row["ID"] != clean_df.loc[index-1, 'ID']:
        coopcount = 1
        workcount = 1

    # if row["Year"] is not None:
    if len(str(row["Year"]).strip()) >= 4:
        if row["Start.Year"] < row["Year"] and row["End.Date.pres"] != "pres":
            row["COOP_ID"] = coopcount
            row["WORK_ID"] = None
            coopcount = coopcount + 1
        else:
            row["WORK_ID"] = workcount
            row["COOP_ID"] = None
            workcount = workcount + 1
    else:
        row["WORK_ID"] = None
        row["COOP_ID"] = None


world_cities_df = pd.read_csv("/Users/mbr/Desktop/transform/cities_countries.csv")

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
    print(row["Full.Location"], "|", city1, "|", country1)

print(clean_df)
clean_df.to_csv("test.csv", index = False)












print("FAISAL IS A PUSSY?")