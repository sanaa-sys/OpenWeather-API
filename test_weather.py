import os
import unittest
import openweather
from requests.exceptions import Timeout
from unittest.mock import MagicMock
from unittest import mock
import datetime
import argparse


from unittest.mock import patch

# london = "http://api.openweathermap.org/data/2.5/weather?q=London&units=metric&appid=9faea4c243f8e74d846cc455fbbd810f"
# california = "http://api.openweathermap.org/data/2.5/weather?q=California,US&units=metric&appid=9faea4c243f8e74d846cc455fbbd810f"
# melbourne = "http://api.openweathermap.org/data/2.5/weather?q=Melbourne,AU&units=metric&appid=9faea4c243f8e74d846cc455fbbd810f"


class TestWeather(unittest.TestCase):

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def setUp(self, mock_get):
        self.api_key = "9faea4c243f8e74d846cc455fbbd810f"
        self.url = "http://api.openweathermap.org/data/2.5/weather?"

        london = "http://api.openweathermap.org/data/2.5/weather?q=London"
        self.w_london = openweather.Weather(london, self.api_key)

        california = "http://api.openweathermap.org/data/2.5/weather?id=4379545"
        self.w_california = openweather.Weather(california, self.api_key, False)

        tokyo = "http://api.openweathermap.org/data/2.5/weather?lat=35.68&lon=139.76"
        self.w_tokyo = openweather.Weather(tokyo, self.api_key)

        melbourne = "http://api.openweathermap.org/data/2.5/weather?zip=3000,AU"
        self.w_melbourne = openweather.Weather(melbourne, self.api_key)


    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_api_fetch(self, mock_get):
        mock_london_fetch = self.w_london.api_fetch()
        self.assertEqual(mock_london_fetch['cod'], 200) # assert that response code is 200
        self.assertEqual(mock_london_fetch['sys']['country'], "GB")  # assert that country is Great Britian
        self.assertEqual(mock_london_fetch['name'], "London")  # assert that city name is indeed London


        mock_california_fetch = self.w_california.api_fetch()
        self.assertEqual(mock_california_fetch['cod'], 200)  # assert that response code is 200
        self.assertEqual(mock_california_fetch['sys']['country'], "US")  # assert that the country is US
        self.assertEqual(mock_california_fetch['name'], "California")  # assert that city name is indeed California


        mock_tokyo_fetch = self.w_tokyo.api_fetch()
        self.assertEqual(mock_tokyo_fetch['cod'], 200)  # assert that response code is 200
        self.assertEqual(mock_tokyo_fetch['sys']['country'], "JP")  # assert that the country is Japan
        self.assertEqual(mock_tokyo_fetch['name'], "Tokyo")  # assert that city name is indeed Tokyo


        mock_melbourne_fetch = self.w_melbourne.api_fetch()
        self.assertEqual(mock_melbourne_fetch['cod'], 200)  # assert that response code is 200
        self.assertEqual(mock_melbourne_fetch['sys']['country'], "AU")  # assert that the country is Australia
        self.assertEqual(mock_melbourne_fetch['name'], "Melbourne")  # assert that the country is Australia

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_time(self, mock_get):

        utc_time = datetime.datetime.utcnow()
        utc_time_string = "On " + utc_time.strftime('%Y-%m-%d %H:%M:%S') + ". " # format time to year-month-day hour:min:second

        london_time_string = self.w_london.get_time()
        self.assertEqual(utc_time_string, london_time_string)

        california_time_string = self.w_california.get_time()
        self.assertEqual(utc_time_string, california_time_string)

        tokyo_time_string = self.w_tokyo.get_time()
        self.assertEqual(utc_time_string, tokyo_time_string)

        melbourne_time_string = self.w_melbourne.get_time()
        self.assertEqual(utc_time_string, melbourne_time_string)

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_temp(self, mock_get):
        mock_metric_string = "Weather conditions are likely {} with temperature range from {}-{} celsius. "
        mock_imperial_string = "Weather conditions are likely {} with temperature range from {}-{} fahrenheit. "

        london_temp_string = self.w_london.get_temp()
        london_mock_temp_string = mock_metric_string.format("light rain", 7.78, 12.22)
        self.assertEqual(london_temp_string, london_mock_temp_string)

        california_temp_string = self.w_california.get_temp()
        california_mock_temp_string = mock_imperial_string.format("few clouds", 53.01, 61)
        self.assertEqual(california_temp_string, california_mock_temp_string)

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_humidity(self, mock_get):
        mock_humidity_string = "The humidity is {}%. "

        tokyo_humidity_string = self.w_tokyo.get_humidity()
        tokyo_mock_humidity_string = mock_humidity_string.format(72)
        self.assertEqual(tokyo_humidity_string, tokyo_mock_humidity_string)

        melbourne_humidity_string = self.w_melbourne.get_humidity()
        melbourne_mock_humidity_string = mock_humidity_string.format(77)
        self.assertEqual(melbourne_humidity_string, melbourne_mock_humidity_string)

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_cloud(self, mock_get):
        mock_cloud_string = "The percentage of clouds is {}%. "

        london_cloud_string = self.w_london.get_cloud()
        london_mock_cloud_string = mock_cloud_string.format(17)
        self.assertEqual(london_cloud_string, london_mock_cloud_string)

        california_cloud_string = self.w_california.get_cloud()
        california_mock_cloud_string = mock_cloud_string.format(20)
        self.assertEqual(california_cloud_string, california_mock_cloud_string)

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_wind(self, mock_get):
        mock_metric_wind_string = "The wind speed is {} meters/sec from {} degrees. "
        mock_imperial_wind_string = "The wind speed is {} miles/hour from {} degrees. "

        london_wind_string = self.w_london.get_wind()
        london_mock_wind_string = mock_metric_wind_string.format(1.5, 140)
        self.assertEqual(london_wind_string, london_mock_wind_string)

        california_wind_string = self.w_california.get_wind()
        california_mock_wind_string = mock_imperial_wind_string.format(3.48, 320)
        self.assertEqual(california_wind_string, california_mock_wind_string)

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_pressure(self, get_mock):
        mock_pressure_string = "The pressure is {} hPa. "

        tokyo_pressure_string = self.w_tokyo.get_pressure()
        tokyo_mock_pressure_string = mock_pressure_string.format(1026)
        self.assertEqual(tokyo_pressure_string, tokyo_mock_pressure_string)

        melbourne_pressure_string = self.w_melbourne.get_pressure()
        melbourne_mock_pressure_string = mock_pressure_string.format(1010)
        self.assertEqual(melbourne_pressure_string, melbourne_mock_pressure_string)

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_sunrise(self, get_mock):
        mock_sunrise_string = "Sunrise time is at {}. "


        ### california sunrise
        mock_california_unix_utc = 1571141942
        mock_california_utc_sunrise_time = datetime.datetime.utcfromtimestamp(mock_california_unix_utc)  # convert from unix utc to current utc time


        mock_california_sunrise_string = mock_california_utc_sunrise_time.strftime('%H:%M:%S')  # format time to hour:min:second
        mock_california_sunrise_string = mock_sunrise_string.format(mock_california_sunrise_string)
        california_sunrise_string = self.w_california.get_sunrise()
        self.assertEqual(mock_california_sunrise_string, california_sunrise_string)


        ### melbourne sunrise
        mock_melbourne_unix_utc = 1571141942
        mock_melbourne_utc_sunrise_time = datetime.datetime.utcfromtimestamp(mock_melbourne_unix_utc)  # convert from unix utc to current utc time

        mock_melbourne_sunrise_string = mock_melbourne_utc_sunrise_time.strftime('%H:%M:%S')  # format time to hour:min:second
        mock_melbourne_sunrise_string = mock_sunrise_string.format(mock_melbourne_sunrise_string)
        california_sunrise_string = self.w_california.get_sunrise()
        self.assertEqual(mock_melbourne_sunrise_string, california_sunrise_string)

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_sunset(self, get_mock):
        mock_sunset_string = "Sunset time is at {}. "


        ### california sunset
        mock_california_unix_utc = 1571182368
        mock_california_utc_sunset_time = datetime.datetime.utcfromtimestamp(mock_california_unix_utc)  # convert from unix utc to current utc time


        mock_california_sunset_string = mock_california_utc_sunset_time.strftime('%H:%M:%S')  # format time to hour:min:second
        mock_california_sunset_string = mock_sunset_string.format(mock_california_sunset_string)

        california_sunset_string = self.w_california.get_sunset()
        self.assertEqual(mock_california_sunset_string, california_sunset_string)


        ### melbourne sunset
        mock_melbourne_unix_utc = 1571215023
        mock_melbourne_utc_sunset_time = datetime.datetime.utcfromtimestamp(mock_melbourne_unix_utc)  # convert from unix utc to current utc time

        mock_melbourne_sunset_string = mock_melbourne_utc_sunset_time.strftime('%H:%M:%S')  # format time to hour:min:second
        mock_melbourne_sunset_string = mock_sunset_string.format(mock_melbourne_sunset_string)

        melbourne_sunset_string = self.w_melbourne.get_sunset()
        self.assertEqual(mock_melbourne_sunset_string, melbourne_sunset_string)


    def test_get_url(self):
        test_london_city_url = openweather.get_url("London,GB", None, None, None, self.url)
        london_url = "http://api.openweathermap.org/data/2.5/weather?q=London,GB"
        self.assertEqual(test_london_city_url, london_url)

        test_tokyo_cid_url = openweather.get_url(None, "1850147", None, None, self.url)
        tokyo_url = "http://api.openweathermap.org/data/2.5/weather?id=1850147"
        self.assertEqual(test_tokyo_cid_url, tokyo_url)

        test_california_gc_url = openweather.get_url(None, None, "38.63,-92.57", None, self.url)
        california_url = "http://api.openweathermap.org/data/2.5/weather?lat=38.63&lon=-92.57"
        self.assertEqual(test_california_gc_url, california_url)

        test_melbourne_z_url = openweather.get_url(None, None, None, "3000,AU", self.url)
        melbourne_url = "http://api.openweathermap.org/data/2.5/weather?zip=3000,AU"
        self.assertEqual(test_melbourne_z_url, melbourne_url)


    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_get_weather_object(self, get_mock):

        # california
        mock_california_object = openweather.get_weather_object("fahrenheit", self.url+"id=4379545", self.api_key)
        mock_data = mock_california_object.data

        california_object = self.w_california
        data = california_object.data

        self.assertEqual(mock_data['name'], data['name'])
        self.assertEqual(mock_data['sys']['country'], data['sys']['country'])
        self.assertEqual(mock_data['id'], data['id'])

        # tokyo
        mock_tokyo_object = openweather.get_weather_object("fahrenheit", self.url + "id=4379545", self.api_key)
        mock_data = mock_tokyo_object.data

        tokyo_object = self.w_california
        data = tokyo_object.data

        self.assertEqual(mock_data['name'], data['name'])
        self.assertEqual(mock_data['sys']['country'], data['sys']['country'])
        self.assertEqual(mock_data['id'], data['id'])

    @mock.patch('openweather.requests.get', side_effect=openweather.mocked_requests_get)
    def test_r_print(self, get_mocked):
        mock_california_string = openweather.r_print(self.w_california, False, "fahrenheit", True, True, True, True, True, True)
        california_string = "Weather conditions are likely few clouds with temperature range from 53.01-61 fahrenheit. The humidity is 47%. The percentage of clouds is 20%. The wind speed is 3.48 miles/hour from 320 degrees. The pressure is 1015 hPa. Sunrise time is at 12:19:02. Sunset time is at 23:32:48. "

        self.assertEqual(mock_california_string, california_string)

        mock_melbourne_string = openweather.r_print(self.w_melbourne, False, "fahrenheit", True, True, True, True, True, True)
        melbourne_string = "Weather conditions are likely broken clouds with temperature range from 13.89-16.11 celsius. The humidity is 77%. The percentage of clouds is 75%. The wind speed is 4.6 meters/sec from 360 degrees. The pressure is 1010 hPa. Sunrise time is at 19:34:23. Sunset time is at 08:37:03. "
        self.assertEqual(mock_melbourne_string, melbourne_string)




if __name__ == '__main__':
    unittest.main()
