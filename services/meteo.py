import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


class OpenMeteoService :
	""" Class to use OpenMeteo Forecast API """
    
	def __init__(self):
		# Setup requests caching 
		self.cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
		self.retry_session = retry(self.cache_session, retries = 5, backoff_factor = 0.2)
		self.openmeteo = openmeteo_requests.Client(session = self.retry_session)

		# Set API url
		self.url = "https://api.open-meteo.com/v1/forecast"

	def get_forecast(self, lat, lon, horizon=1):
		params = {
			"latitude": lat,
			"longitude": lon,
			"timezone": "Europe/Berlin",
			"hourly": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "cloud_cover", "precipitation", "wind_speed_10m", "wind_direction_10m"],
			"temperature_unit": "celsius",
			"wind_speed_unit": "kmh",
			"precipitation_unit": "mm",
			"forecast_days": horizon
		}
		response = self.openmeteo.weather_api(self.url, params=params)
		# Process a single location
		return self.extract_data(response=response[0])
	
	def extract_data(self, response):

		# Process hourly data. The order of variables needs to be the same as requested.
		hourly = response.Hourly()
		hourly_temperature_2m       = hourly.Variables(0).ValuesAsNumpy().tolist()
		hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy().tolist()
		hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy().tolist()
		hourly_cloud_cover          = hourly.Variables(3).ValuesAsNumpy().tolist()
		hourly_precipitation        = hourly.Variables(4).ValuesAsNumpy().tolist()
		hourly_wind_speed_10m       = hourly.Variables(5).ValuesAsNumpy().tolist()
		hourly_wind_direction_10m   = hourly.Variables(6).ValuesAsNumpy().tolist()

		hourly_data = {"date": pd.date_range(
			start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
			end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = hourly.Interval()),
			inclusive = "left"
		).strftime("%Y-%m-%dT%H:%M:%SZ").to_list()}

		hourly_data["temperature_2m"]       = hourly_temperature_2m
		hourly_data["apparent_temperature"] = hourly_apparent_temperature
		hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
		hourly_data["cloud_cover"]          = hourly_cloud_cover
		hourly_data["precipitation"]        = hourly_precipitation
		hourly_data["wind_speed_10m"]       = hourly_wind_speed_10m
		hourly_data["wind_direction_10m"]   = hourly_wind_direction_10m

		return hourly_data

if __name__ == '__main__':
	om = OpenMeteoService()
	print(om.get_forecast(47.383331, 0.68333))