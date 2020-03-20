import requests
import argparse
import datetime
import os
from pprint import pprint

#test to see if CI works........................pip
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data


    if (args[0] == "http://api.openweathermap.org/data/2.5/weather?q=London&units=metric&appid=9faea4c243f8e74d846cc455fbbd810f"):

        # London
        return MockResponse({"coord":{"lon":-0.13,"lat":51.51},
                             "weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],
                             "base":"stations",
                             "main":{"temp":10.1,"pressure":1005,"humidity":81,"temp_min":7.78,"temp_max":12.22},
                             "visibility":10000,"wind":{"speed":1.5},"rain":{"1h":0.25},"clouds":{"all":17},"dt":1571187011,
                             "sys":{"type":1,"id":1414,"country":"GB","sunrise":1571207117,"sunset":1571245602},
                             "timezone":0,"id":2643743,"name":"London","cod":200})

    elif (args[0] == "http://api.openweathermap.org/data/2.5/weather?id=4379545&units=imperial&appid=9faea4c243f8e74d846cc455fbbd810f"):
        # California
        return MockResponse({"coord":{"lon":-92.57,"lat":38.63},
                             "weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02n"}],
                             "base":"stations",
                             "main":{"temp":56.55,"pressure":1015,"humidity":47,"temp_min":53.01,"temp_max":61},
                             "visibility":16093,"wind":{"speed":17.22,"deg":320,"gust":26.4},"clouds":{"all":20},"dt":1571189504,
                             "sys":{"type":1,"id":3686,"country":"US","sunrise":1571141942,"sunset":1571182368},
                             "timezone":0,"id":4379545,"name":"California","cod":200})

    elif (args[0] == "http://api.openweathermap.org/data/2.5/weather?lat=35.68&lon=139.76&units=metric&appid=9faea4c243f8e74d846cc455fbbd810f"):
        # Tokyo
        return MockResponse({"coord": {"lon": 139.76, "lat": 35.68},
                             "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}],
                             "base": "stations",
                             "main": {"temp": 15.48, "pressure": 1026, "humidity": 72, "temp_min": 13.89, "temp_max": 17.22},
                             "visibility": 10000, "wind": {"speed": 3.1, "deg": 10}, "rain": {}, "clouds": {"all": 75}, "dt": 1571186255,
                             "sys": {"type": 1, "id": 8077, "country": "JP", "sunrise": 1571172444, "sunset": 1571213138},
                             "timezone": 0, "id": 1850147, "name": "Tokyo", "cod": 200})

    elif (args[0] == "http://api.openweathermap.org/data/2.5/weather?zip=3000,AU&units=metric&appid=9faea4c243f8e74d846cc455fbbd810f"):
        # Melbourne
        return MockResponse({"coord":{"lon":144.96,"lat":-37.81},
                             "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],
                             "base":"stations",
                             "main":{"temp":14.97,"pressure":1010,"humidity":77,"temp_min":13.89,"temp_max":16.11},
                             "visibility":10000,"wind":{"speed":4.6,"deg":360},"clouds":{"all":75},"dt":1571187042,
                             "sys":{"type":1,"id":9554,"country":"AU","sunrise":1571168063,"sunset":1571215023},
                             "timezone":0,"id":0,"name":"Melbourne","cod":200})

    print(args[0])
    return MockResponse(None)



def initialiseParser():
    # initialise parser for arguments parsing
    parser = argparse.ArgumentParser()

    # add compulsory arguments "-api"
    parser.add_argument("-api", required=True,help="enter in following syntax, python openweather.py  -api=xxx rest of arguments which will be further explainded")

    # any location flag is mutually exclusive
    location = parser.add_mutually_exclusive_group()
    location.add_argument("-city", "--city",help="Input location with city name add -city=city,countrycode(location can be inputted with one method only)")
    location.add_argument("-cid", "--cid",help="Input location with city name add -cid=(location can be inputted with one method only)")
    location.add_argument("-gc", "--gc", type=str, help="Input location with coordinates add -gc=\"lat,lon\"")
    location.add_argument("-z", "--z",help="Input location with zip code add -z=zipcode,countrycode(location can be inputted with one method only)")

    # add optional arguments
    parser.add_argument("-time", "--time", action='store_true',help="displays date and time at which values are being shown")
    parser.add_argument("-temp", "--temp", help="displays temperature range for current day")
    parser.add_argument("-pressure", "--pressure", action='store_true', help="displays pressure for current day")
    parser.add_argument("-cloud", "--cloud", action='store_true', help="displays cloud data for current day")
    parser.add_argument("-humidity", "--humidity", action='store_true', help="displays humidity for current day")
    parser.add_argument("-wind", "--wind", action='store_true', help="displays wind data for current day")
    parser.add_argument("-sunset", "--sunset", action='store_true', help="displays sunrise time for current day")
    parser.add_argument("-sunrise", "--sunrise", action='store_true', help="displays sunset time for current day")
    parser.add_argument("-help", action='store_true', help="displays help menu")

    return parser.parse_args()  # return arguments parsing


def get_city_url(city, api):
    # Monash University: Monash,AU
    arg_city = str(city)

    url = api + "q=" + arg_city
    return url


def get_cid_url(cid, api):
    # Monash University: 2157247
    arg_cid = str(cid)

    url = api + "id=" + arg_cid
    return url


def get_gc_url(gc, api):
    # Monash University -34.23, 140.57
    arg_gc = str(gc)
    arg_gc = arg_gc.replace(' ', '')
    lat, lon = arg_gc.split(',')

    url = api + "lat=" + lat + "&lon=" + lon
    return url

    # valid: python .py -gc -34.23 140.57


def get_z_url(z, api):
    # Monash University: 3800,AU
    arg_z = str(z)
    arg_z = arg_z.replace(' ', '')
    zip_code, country_code = arg_z.split(',')

    url = api + "zip=" + zip_code + "," + country_code
    return url

class Weather():
    def __init__(self, url, api, metric=True):
        self.url = url
        self.api = api
        self.metric = metric
        self.data = self.api_fetch()

    def get_time(self):

        # offset to location's current time
        timezone_offset = self.data['timezone']
        utc_time = datetime.datetime.utcnow()  # initialise utc time

        offset = datetime.timedelta(seconds=timezone_offset)
        data_time = utc_time + offset

        time_string = data_time.strftime('%Y-%m-%d %H:%M:%S')  # format time to year-month-day hour:min:second

        # concatenate readable syntax and return string
        time_string = "On {}. ".format(time_string)

        return time_string


    def get_temp(self):

        # api return temperature string in fahrenheit or celsius(default)
        temp_min = self.data['main']['temp_min']
        temp_max = self.data['main']['temp_max']

        # concatenate readable syntax
        temp_string = "The temperature ranges from {}-{}".format(temp_min, temp_max)

        # concatenate units
        if self.metric is False:
            temp_string += " fahrenheit. "
        else:
            temp_string += " celsius. "

        return temp_string


    def get_humidity(self):

        # api return humidity string in % and description string
        humidity = self.data['main']['humidity']
        description = self.data['weather'][0]['description']

        # concatenate readable syntax, units and return string
        humidity_string = "Weather conditions are likely {} with humidity of {}%. ".format(description, humidity)
        return humidity_string


    def get_cloud(self):

        # api return clouds string in %
        cloud = self.data['clouds']['all']

        # concatenate readable syntax, units and return string
        cloud_string = "The percentage of clouds is {}%. ".format((cloud))
        return cloud_string


    def get_wind(self):

        data = self.api_fetch(self.url)

        # api return windspeed string in miles/sec or meters/sec(default) and wind degrees string in degrees
        wind_speed = data['wind']['speed']
        wind_degrees = data['wind']['deg']

        wind_string = "The wind speed is {} meters/sec from {} degrees. ".format(str(wind_speed), str(wind_degrees))

        # concatenate readable syntax, units and return string
        return wind_string


    def get_pressure(self):

        # api return pressure string in hPa
        pressure = self.data['main']['pressure']

        # concatenate readable syntax, units and return string
        pressure_string = "The pressure is {} hPa. ".format(pressure)
        return pressure_string


    def get_sunrise(self):
        unix_utc = self.data['sys']['sunrise']  # api response in unix utc
        utc_sunrise_time = datetime.datetime.utcfromtimestamp(unix_utc)  # convert from unix utc to current utc time

        # offset to location's current time
        timezone_offset = self.data['timezone']
        offset = datetime.timedelta(seconds=timezone_offset)
        local_sunrise_time = utc_sunrise_time + offset

        sunrise_string = local_sunrise_time.strftime('%H:%M:%S')  # format time to hour:min:second

        # concatenate readable syntax and return string
        sunrise_string = "Sunrise time is at {}. ".format(sunrise_string)
        return sunrise_string


    def get_sunset(self):
        unix_utc = self.data['sys']['sunset']  # api response in unix utc
        utc_sunset_time = datetime.datetime.utcfromtimestamp(unix_utc)  # convert from unix utc to current utc time

        # offset to location's current time
        timezone_offset = self.data['timezone']
        offset = datetime.timedelta(seconds=timezone_offset)
        local_sunset_time = utc_sunset_time + offset

        sunset_string = local_sunset_time.strftime('%H:%M:%S')  # format time to hour:min:second

        # concatenate readable syntax and return string
        sunset_string = "Sunset time is at {}. ".format(sunset_string)
        return sunset_string


    def api_fetch(self):
        # add units
        if self.metric is False:
            url = self.url + "&units=imperial"
        else:
            url = self.url + "&units=metric"

        api = "&appid=" + self.api  # concatnate provided api key to comply with api call format
        url += api  # append api key to url for api call
        response = requests.get(url)  # api call
        data = response.json()  # api response
        # pprint(data)

        return data




if __name__ == "__main__":

    # initialise arguments parsing
    args = initialiseParser()
    api = "http://api.openweathermap.org/data/2.5/weather?"  # initialise api url for api call

    # invoke help menu and exit program without any error code
    if args.help:
        os.system("python3 " + __file__ + " --help")
        exit()

    if args.city:
        url = get_city_url(args.city, api)

    elif args.cid:
        url = get_cid_url(args.cid, api)

    elif args.gc:
        url = get_gc_url(args.gc, api)

    elif args.z:
        url = get_z_url(args.z, api)

    else:
        # Case whereby user does not provide any location argument, exit with error code 1
        print("User must enter a location using either -city, -cid, -gc or -z")
        exit(1)

    if args.temp == "fahrenheit":
        weather_object = Weather(url, args.api, False)
    else:
        weather_object = Weather(url, args.api)
    status_code = weather_object.data['cod']


    if (status_code == 200):
        r_string = ""  # intialise return string

        if (args.humidity == False and args.pressure == False and args.temp == None and args.wind == False and
                args.cloud == False and args.sunrise == False and args.sunset == False and args.time == False):

            print("Enter a weather parameter")
            exit(2)

        if args.time:
            r_string += weather_object.get_time()

        if args.temp:
            r_string += weather_object.get_temp()

        if args.humidity:
            r_string += weather_object.get_humidity()

        if args.cloud:
            r_string += weather_object.get_cloud()

        if args.wind:
            r_string += weather_object.get_wind()

        if args.pressure:
            r_string += weather_object.get_pressure()

        if args.sunrise:
            r_string += weather_object.get_sunrise()

        if args.sunset:
            r_string += weather_object.get_sunset()

        # print result string
        print(r_string)

    else:
        # print error message with error code
        print("Error: {}".format(status_code))
        exit(int(status_code))







