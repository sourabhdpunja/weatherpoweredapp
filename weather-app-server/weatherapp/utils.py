import urllib.request
from datetime import date, timedelta
from math import radians, sin, cos, acos
import logging
import json

# environment variable import
from decouple import config

# custom imports
from weatherapp.apiurlconstants import CURRENT_TEMP_WEATHERBIT_API, HISTORICAL_TEMP_WEATHERBIT_API

logger = logging.getLogger(__name__)


def calc_avg_temp(latitude, longitude):
    """
    Fetches the last 5 days temperature of the given coordinate and calculates the average temperature of them.
    Parameters:
        latitude: latitude of the coordinate
        longitude: longitude of the coordinate.
    Returns:
        average temperature in Celcius of the given coordinate.
    """
    last_five_days_temp = []
    today = date.today()
    for decrement in range(1, 6):
        start_date = today - timedelta(decrement)
        end_date = today - timedelta(decrement - 1)
        history_url = HISTORICAL_TEMP_WEATHERBIT_API.format(start_date, end_date,
                                                            latitude, longitude, config('API_KEY'))
        try:
            api_response = urllib.request.urlopen(history_url)
        except urllib.request.HTTPError as err:
            if err.code == 429:
                error_string = "Limit of historical data request from weatherbit API exceeded." \
                               " Limit of 200 request per day in present plan."
                logger.error(error_string)
                raise ValueError(error_string)
            else:
                error_string = "{} raised. Error during request to weatherbit API for historical data.".format(err.code)
                logger.error(error_string)
                raise ValueError(error_string)

        json_response = json.loads(api_response.read().decode())
        if "data" not in json_response:
            error_string = "No data in historical weatherbit api response."
            logger.error(error_string)
            raise ValueError(error_string)

        weather_data = json_response["data"][0]
        if "temp" not in weather_data:
            error_string = "No temperature data in historical api response"
            logger.error(error_string)
            raise ValueError(error_string)

        decrement_day_temp = weather_data["temp"]
        last_five_days_temp.append(decrement_day_temp)
        logger.info("Request to weatherbit API for {} weather successful.".format(start_date))

    if len(last_five_days_temp) == 0:
        error_string = "No values found for temperatures for last 5 days."
        logger.error(error_string)
        raise ValueError(error_string)
    avg_temp = sum(last_five_days_temp) / len(last_five_days_temp)
    return avg_temp


def get_closest_coordinate(curr_subscriber_coordinate, location_coordinate_list):
    """
    Fetches the coordinate within 50 km of the current coordinate if present from previous set of coordinates.
    If not present returns the current coordinate itself.
    Note: Finding distance between two points using latitude and longitude is given in the following link
    https://support.sisense.com/hc/en-us/articles/230644288-Calculate-Distance-Between-Two-Points-Using-Latitude-and-Longitude
    Parameters:
        curr_subscriber_coordinate: coordinate of the subscriber
        location_coordinate_list: coordinates of subscribers whose current and average temperature
                                 have been calculated previously.
    Returns:
        closest_coordinate if present else the current coordinate itself.
    """
    start_lat = radians(float(curr_subscriber_coordinate[0]))
    start_long = radians(float(curr_subscriber_coordinate[1]))
    for entry in location_coordinate_list:
        end_lat = radians(float(entry[0]))
        end_long = radians(float(entry[1]))
        dist = 6371.01 * acos(sin(start_lat) * sin(end_lat) +
                              cos(start_lat) * cos(end_lat) * cos(start_long - end_long))
        if dist < 50:
            return entry
    return curr_subscriber_coordinate


def fetch_curr_temp(latitude, longitude):
    """
    Fetches the current temperature with description of the given coordinates.
    Parameters:
        latitude: latitude of the coordinate
        longitude: longitude of the coordinate.
    Returns:
        list containing current temperature in Celcius in first entry and weather description in second entry.
    """
    current_url = CURRENT_TEMP_WEATHERBIT_API.format(latitude, longitude, config('API_KEY'))
    try:
        api_response = urllib.request.urlopen(current_url)
    except urllib.request.HTTPError as err:
        if err.code == 429:
            error_string = "Limit of current weather request from weatherbit API exceeded in present plan."
            logger.error(error_string)
            raise ValueError(error_string)
        else:
            error_string = "{} raised. Error during request to weatherbit API for current weather.".format(err.code)
            logger.error(error_string)
            raise ValueError(error_string)

    json_response = json.loads(api_response.read().decode())
    if "data" not in json_response:
        error_string = "No data in current temperature weatherbit api response."
        logger.error(error_string)
        raise ValueError(error_string)

    weather_data = json_response["data"][0]
    if "temp" not in weather_data:
        error_string = "No temperature data in current temperature weatherbit api response."
        logger.error(error_string)
        raise ValueError(error_string)
    current_temp = weather_data["temp"]

    if "weather" not in weather_data or "description" not in weather_data["weather"]:
        error_string = "No weather description in current temperature weatherbit api response."
        logger.error(error_string)
        temp_desc = ''
    else:
        temp_desc = weather_data["weather"]["description"]

    logger.info("Request to weatherbit API for current weather successful.")
    return [current_temp, temp_desc]
