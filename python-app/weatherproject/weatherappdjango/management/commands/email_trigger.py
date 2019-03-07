import urllib.request
import json
import logging
from datetime import date, timedelta
from math import radians, sin, cos, acos
# environment variable import
from decouple import config

# Custom imports
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.core import mail
from django.core.management.base import BaseCommand
from weatherappdjango.emailclass.email import Email

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        response = urllib.request.urlopen('http://localhost:8000/api/weather/getallcredentials')
        subscribers_list = json.loads(response.read().decode())["results"]
        if len(subscribers_list) <= 0:
            logger.info("No subscribers in present in subscribers table.")
            return
        location_to_mail_map = {}
        email_messages_obj_list = []
        lat_long_key_set = set([])
        for subscriber in subscribers_list:
            emailid = subscriber["emailId"]
            latitude = subscriber["latitude"]
            longitude = subscriber["longitude"]
            lat_long_key = (latitude, longitude)
            closest_lat_long = Command.distance_lat_long(self, lat_long_key, lat_long_key_set)
            lat_long_key_set.add(closest_lat_long)
            if closest_lat_long in location_to_mail_map:
                emailobj = location_to_mail_map.get(closest_lat_long)
            else:
                curr_temp_state = Command.fetch_curr_temp(self, latitude, longitude)
                avg_temp = Command.fetch_avg_temp(self, latitude, longitude)
                emailobj = Email(emailid, curr_temp_state[0], curr_temp_state[1])
                emailobj.create_email(avg_temp)
                location_to_mail_map[lat_long_key] = emailobj
            msg = EmailMultiAlternatives(emailobj.subject, emailobj.html_body,
                                         config('FROM_EMAIL_ADDRESS'), [emailobj.to_address])
            msg.attach_alternative(emailobj.html_body, "text/html")
            msg.content_subtype = 'html'
            msg.mixed_subtype = 'related'
            msg.attach(emailobj.image)
            try:
                # msg.send(fail_silently=True)
                email_messages_obj_list.append(msg)
            except BadHeaderError:
                logger.info("Invalid header found when sending mail to {} from {}"
                            .format(emailobj.to_address, config('FROM_EMAIL_ADDRESS')))
                return
            logger.info("Created Email Object with to {} and from {}"
                        .format(emailobj.to_address, config('FROM_EMAIL_ADDRESS')))

        if len(email_messages_obj_list) > 0:
            connection = mail.get_connection()  # Use default email connection
            connection.send_messages(email_messages_obj_list)

    def distance_lat_long(self, lat_long_key, lat_long_key_set):
        start_lat = radians(float(lat_long_key[0]))
        start_long = radians(float(lat_long_key[1]))
        for entry in lat_long_key_set:
            end_lat = radians(float(entry[0]))
            end_long = radians(float(entry[1]))
            dist = 6371.01 * acos(sin(start_lat) * sin(end_lat) +
                                  cos(start_lat) * cos(end_lat) * cos(start_long - end_long))
            if dist < 50:
                return entry
        return lat_long_key

    def fetch_curr_temp(self, latitude, longitude):
        current_url = "https://api.weatherbit.io/v2.0/current?lat={}&lon={}&key={}"\
            .format(latitude, longitude, config('API_KEY'))
        try:
            api_response = urllib.request.urlopen(current_url)
        except urllib.request.HTTPError as err:
            if err.code == 429:
                logger.error("Limit of current weather request from weatherbit API exceeded in present plan.")
                raise
            else:
                logger.error("{} raised. Error during request to weatherbit API for current weather.".format(err.code))
                raise
        weather_data = json.loads(api_response.read().decode())["data"][0]
        current_temp = weather_data["temp"]
        temp_desc = weather_data["weather"]["description"]
        logger.info("Request to weatherbit API for current weather successful.")
        return [current_temp, temp_desc]

    def fetch_avg_temp(self, latitude, longitude):
        last_five_days_temp = []
        today = date.today()
        for decrement in range(1, 2):
            start_date = today - timedelta(decrement)
            end_date = today - timedelta(decrement-1)
            history_url = "https://api.weatherbit.io/v2.0/history/daily" \
                "?&start_date={}&end_date={}&lat={}&lon={}&key={}"\
                .format(start_date, end_date, latitude, longitude, config('API_KEY'))
            try:
                api_response = urllib.request.urlopen(history_url)
            except urllib.request.HTTPError as err:
                if err.code == 429:
                    logger.error(
                        "Limit of historical data request from weatherbit API exceeded."
                        " Limit of 200 request per day in present plan.")
                    raise
                else:
                    logger.error(
                        "{} raised. Error during request to weatherbit API for historical data.".format(err.code))
                    raise
            weather_data = json.loads(api_response.read().decode())["data"][0]
            decrement_day_temp = weather_data["temp"]
            last_five_days_temp.append(decrement_day_temp)
            logger.info("Request to weatherbit API for {} weather successfull.".format(start_date))
        avg_temp = sum(last_five_days_temp) / len(last_five_days_temp)
        #TODO Remove below comment
        logger.info("{}, {}, {}".format(last_five_days_temp, len(last_five_days_temp), avg_temp))
        return avg_temp
