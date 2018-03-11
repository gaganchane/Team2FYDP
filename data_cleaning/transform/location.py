from geopy.geocoders import Nominatim
import pandas as pd
from geotext import GeoText

#filepath = "/Users/mbr/Desktop/transform/location_test"
if __name__ == '__main__':

    all_df = pd.read_csv("/Users/mbr/Desktop/transform/location_test.csv")
    world_cities_df = pd.read_csv("/Users/mbr/Desktop/transform/cities_countries.csv")
    # print(world_cities_df)

    geolocator = Nominatim(scheme='http')
    city1 = ""
    country1 = ""
    data = []

    for index, row in all_df.iterrows():
        city1 = ""
        country1 = ""
        try:
            geo = geolocator.geocode(row[0])
            city = GeoText(str(geo).strip()).cities
            country = GeoText(str(geo).strip()).countries

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
            # print("Geopy not working")
            city = GeoText(row[0]).cities
            country = GeoText(row[0]).countries
            if len(city) > 0 and len(country) > 0:

                city1 = city[0]
                country1 = country[0]

            elif len(country) > 0:
                df = world_cities_df[(world_cities_df['country'] == country[0])]
                for city_df in df['name']:
                    #Add spaces between text
                    if city_df.lower() in row[0].lower():
                        city1 = city_df
                        country1 = country[0]
                        break
                    else:
                        city1 = ""
                        country1 = ""

            elif len(city) > 0:
                df = world_cities_df[(world_cities_df['country'] == 'Canada') | (world_cities_df['country'] == 'USA')]
                for index_x, x in df.iterrows():

                    curr_location = " " + row[0].lower() + " "
                    spaced_x = " " + x['name'].lower() + " "

                    if spaced_x in curr_location:
                        country1 = x['country']
                        city1 = city[0]
                        break

            else:
                for index_y, y in world_cities_df.iterrows():

                    curr_location = " " + row[0].lower() + " "
                    spaced_y = " " + y['name'].lower() + " "

                    if spaced_y in curr_location:
                        city1 = y['name']
                        country1 = y['country']
                        break

        print(row[0], "|", city1, country1)
        data.append([city1, country1])

    data_df = pd.DataFrame(data)
    data_df.to_csv("LOCATION ALL.csv")
