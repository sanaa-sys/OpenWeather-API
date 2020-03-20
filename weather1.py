import requests
import time
import argparse
import datetime
import os
from pprint import pprint


# api_id = &appid=9faea4c243f8e74d846cc455fbbd810f >>> Jason's
"""

# city = input("Enter your city: ")
city = "Clayton,AU"
# api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=9faea4c243f8e74d846cc455fbbd810f&units=metric".format(city)
api_url = "http://api.openweathermap.org/data/2.5/weather?zip=3800,AU&appid=9faea4c243f8e74d846cc455fbbd810f&units=metric"

response = requests.get(api_url)

data = response.json()

# pprint(data)

city_id = data['sys']['id']
gc_lat = data['coord']['lat']
gc_lon = data['coord']['lon']
zip = data['cod']
last_time = data['timezone']
temp = data['main']['temp']
pressure = data['main']['pressure']
cloud = data['clouds']
humidity = data['main']['humidity']
wind = data['wind']
sunset = data['sys']['sunset']
sunrise = data['sys']['sunrise']
pprint(data)
# print("City ID: {}".format(city_id))
# print("Coordinates: {} lat, {} lon".format(gc_lat, gc_lon))
# print("Zip code: {}".format(zip))
# print("Time: {}".format(time.strftime('%H:%M:%S', time.gmtime(last_time))))
# print("Temp: {}".format(temp))
# print("Pressure: {}".format(pressure))
# print("Clouds: {}".format(cloud))
# print("Humidity: {}".format(humidity))
# print("Wind: {}".format(wind))
# print("Sunset: {}".format(time.strftime('%H:%M:%S', time.gmtime(sunset))))
# print("Sunrise: {}".format(time.strftime('%H:%M:%S', time.gmtime(sunrise))))
"""



if __name__ == "__main__":

    # initialise parser for arguments parsing
    parser = argparse.ArgumentParser()

    # add compulsory arguments "-api"
    parser.add_argument("-api", required=True, help = "enter in following syntax, python openweather.py  -api=xxx rest of arguments which will be further explainded")

    # any location flag is mutually exclusive
    location = parser.add_mutually_exclusive_group()
    location.add_argument("-city", "--city", help="Input location with city name add -city=city,countrycode(location can be inputted with one method only)")
    location.add_argument("-cid", "--cid", help="Input location with city name add -cid=(location can be inputted with one method only)")
    location.add_argument("-gc", "--gc", type=str, help="Input location with coordinates add -gc=\"lat,lon\"")

    location.add_argument("-z", "--z", help="Input location with zip code add -z=zipcode,countrycode(location can be inputted with one method only)")

    # add optional arguments
    parser.add_argument("-time", "--time", action = 'store_true', help = "displays date and time at which values are being shown")
    parser.add_argument("-temp", "--temp", help = "displays temperature range for current day")
    parser.add_argument("-pressure", "--pressure", action = 'store_true', help = "displays pressure for current day")
    parser.add_argument("-cloud", "--cloud", action = 'store_true', help = "displays cloud data for current day")
    parser.add_argument("-humidity", "--humidity", action = 'store_true', help = "displays humidity for current day")
    parser.add_argument("-wind", "--wind", action = 'store_true', help = "displays wind data for current day")
    parser.add_argument("-sunset", "--sunset", action = 'store_true', help = "displays sunrise time for current day")
    parser.add_argument("-sunrise", "--sunrise", action = 'store_true', help = "displays sunset time for current day")
    parser.add_argument("-help", action = 'store_true', help = "displays help menu")

    args = parser.parse_args()  # initialise arguments parsing

    # invoke help menu and exit program without any error code
    if (args.help):
        os.system("python3 " + __file__ + " --help")
        exit()

    url = "http://api.openweathermap.org/data/2.5/weather?"     # initialise url for api call
    api_id = "&appid=" + str(args.api)   # concatnate provided api key to comply with api call format
    r_string = ""   # intialise return string
    utc_time = datetime.datetime.utcnow()   # initialise utc time

    if args.city:
        # Monash University: Monash,AU
        arg_city = str(args.city)
        url = url + "q=" + arg_city

    elif args.cid:
        # Monash University: 2157247
        arg_cid = str(args.cid)
        url = url + "id=" + arg_cid

    elif args.gc:
        # Monash University -34.23, 140.57
        arg_gc = str(args.gc)
        lat, lon = arg_gc.split(',')

        url = url + "lat=" + lat + "&lon=" + lon

        # valid: python .py -gc -34.23 140.57

    elif args.z:
        # Monash University: 3800,AU
        arg_z = str(args.z)

        zip_code, country_code = arg_z.split(',')

        url = url + "zip=" + zip_code + "," + country_code

    else:
        # Case whereby user does not provide any location argument, exit with error code 1
        print("User must enter a location using either -city, -cid, -gc or -z")
        exit(1)


    # -temp argument specified as fahrenheit
    if str(args.temp) == "fahrenheit":
        url = url + "&units=imperial"
    # default to celsius
    else:
        url = url + "&units=metric"


    url += api_id   # append api key to url for api call
    response = requests.get(url)    # api call
    data = response.json()  # api response
    # pprint(data)


    if (data['cod'] != "404"):
        if args.time:
            # offset to location's current time
            timezone_offset = data['timezone']
            offset = datetime.timedelta(seconds=timezone_offset)
            data_time = utc_time + offset

            time_string = data_time.strftime('%Y-%m-%d %H:%M:%S')   # format time to year-month-day hour:min:second

            # concatenate readable syntax and return string
            time_string = "On {}, ".format(time_string)
            r_string += time_string

        if args.temp:
            # api return temperature string in fahrenheit or celsius(default)
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']

            # concatenate readable syntax
            temp_string = "The temperature ranges from {}-{}".format(temp_min, temp_max)

            # concatenate units
            if str(args.temp) == "fahrenheit":
                temp_string += " fahrenheit. "
            else:
                temp_string += " celsius. "

            # return string
            r_string += temp_string

        if args.humidity:
            # api return humidity string in % and description string
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']

            # concatenate readable syntax, units and return string
            humidity_string = "Weather conditions are likely {} with humidity of {}%. ".format(description, humidity)
            r_string += humidity_string

        if args.cloud:
            # api return clouds string in %
            cloud = data['clouds']['all']

            # concatenate readable syntax, units and return string
            cloud_string = "The percentage of clouds is {}%. ".format((cloud))
            r_string += cloud_string

        if args.wind:
            # api return windspeed string in miles/sec or meters/sec(default) and wind degrees string in degrees
            wind_speed = data['wind']['speed']
            wind_degrees = data['wind']['deg']

            if str(args.temp) == "fahrenheit":
                wind_string = "The wind speed is {} miles/sec from {} degrees. ".format(str(wind_speed), str(wind_degrees))
            else:
                wind_string = "The wind speed is {} meters/sec from {} degrees. ".format(str(wind_speed), str(wind_degrees))

            # concatenate readable syntax, units and return string
            r_string += wind_string

        if args.pressure:
            # api return pressure string in hPa
            pressure = data['main']['pressure']

            # concatenate readable syntax, units and return string
            pressure_string = "The pressure is {} hPa. ".format(pressure)
            r_string += pressure_string

        if args.sunrise:
            unix_utc = data['sys']['sunrise']   # api response in unix utc
            utc_sunrise_time = datetime.datetime.utcfromtimestamp(unix_utc) # convert from unix utc to current utc time

            # offset to location's current time
            timezone_offset = data['timezone']
            offset = datetime.timedelta(seconds=timezone_offset)
            local_sunrise_time = utc_sunrise_time + offset

            sunrise_string = local_sunrise_time.strftime('%H:%M:%S')    # format time to hour:min:second

            # concatenate readable syntax and return string
            sunrise_string = "Sunrise time is at {}. ".format(sunrise_string)
            r_string += sunrise_string

        if args.sunset:
            unix_utc = data['sys']['sunset']    # api response in unix utc
            utc_sunset_time = datetime.datetime.utcfromtimestamp(unix_utc)  # convert from unix utc to current utc time

            # offset to location's current time
            timezone_offset = data['timezone']
            offset = datetime.timedelta(seconds=timezone_offset)
            local_sunset_time = utc_sunset_time + offset

            sunset_string = local_sunset_time.strftime('%H:%M:%S')  # format time to hour:min:second

            # concatenate readable syntax and return string
            sunset_string = "Sunset time is at {}. ".format(sunset_string)
            r_string += sunset_string

        # print result string
        print(r_string)

    else:
        # print error message with error code
        print("Error: {}".format(data['cod']))
        exit(int(data['cod']))



    






# python openweather.py -api = XXX -city="London" -temp = "celsius"
# >> The temperature ranges from 10.08-11.98 celsius.

# python openweather.py -api = XXX -city="London" -temp = "celsius"
# >> On 2019-09-17 00:00:00+00, the temperature ranges from 10.08-11.98 celsius.
#   It is likely Cloudy with a humidity of 58% and a wind speed of 4.67 from 134.853 degrees.












