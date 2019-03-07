import urllib.request
import json
import logging
from datetime import date, timedelta
from math import radians, sin, cos, acos
from django.core.mail import EmailMultiAlternatives
from django.core import mail
from django.core.management.base import BaseCommand

# environment variable import
from decouple import config

# Custom imports
from weatherapp.emailclass.email import Email

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        response = urllib.request.urlopen('http://localhost:8000/api/weather/getallsubscribers')
        subscribers_list = json.loads(response.read().decode())["results"]

        if len(subscribers_list) <= 0:
            logger.info("No subscribers present in subscribers table.")
            return

        location_to_mail_map = {}
        email_messages_obj_list = []
        location_coordinate_set = set([])

        for subscriber in subscribers_list:

            to_email_id = subscriber["emailId"]
            latitude = subscriber["latitude"]
            longitude = subscriber["longitude"]
            curr_subscriber_coordinate = (latitude, longitude)

            closest_coordinate = Command.get_closest_coordinate(
                self, curr_subscriber_coordinate, location_coordinate_set)
            location_coordinate_set.add(closest_coordinate)
            if closest_coordinate in location_to_mail_map:
                email_template = location_to_mail_map.get(closest_coordinate)
            else:
                curr_temp_state = Command.fetch_curr_temp(self, latitude, longitude)
                avg_temp = Command.calc_avg_temp(self, latitude, longitude)
                email_template = Email(curr_temp_state[0], curr_temp_state[1])
                email_template.create_email(avg_temp)
                location_to_mail_map[curr_subscriber_coordinate] = email_template

            email_message = self.build_emailmessage_obj(to_email_id, email_template)
            email_messages_obj_list.append(email_message)
            logger.info("Created Email Object with to {} and from {}"
                        .format(to_email_id, config('FROM_EMAIL_ADDRESS')))

        # Send multiple emails using same SMTP connection
        if len(email_messages_obj_list) > 0:
            connection = mail.get_connection(fail_silently=True)
            connection.send_messages(email_messages_obj_list)


    def build_emailmessage_obj(self, to_address, email_template):
        """
        Builds EmailMessage Instance using the email_template and to_address.
        Parameters:
            to_address: subscriber email id
            email_template: contains the subject, body and image to build the EmailMessage Instance
        Returns:
            EmailMessage Instance
        """
        email_message = EmailMultiAlternatives(email_template.subject, email_template.html_body,
                                               config('FROM_EMAIL_ADDRESS'), [to_address])
        email_message.attach_alternative(email_template.html_body, "text/html")
        email_message.content_subtype = 'html'
        email_message.mixed_subtype = 'related'
        email_message.attach(email_template.image)
        return email_message


    def get_closest_coordinate(self, curr_subscriber_coordinate, location_coordinate_set):
        """
        Fetches the coordinate within 50 km of the current coordinate if present from set of coordinates.
        If not present returns the current coordinate itself.
        Parameters:
            curr_subscriber_coordinate: coordinate of the subscriber
            location_coordinate_set: coordinates of subscribers whose current and average temperature
                                     have been calculated.
        Returns:
            closest_coordinate if present else the current coordinate itself.
        """
        start_lat = radians(float(curr_subscriber_coordinate[0]))
        start_long = radians(float(curr_subscriber_coordinate[1]))
        for entry in location_coordinate_set:
            end_lat = radians(float(entry[0]))
            end_long = radians(float(entry[1]))
            dist = 6371.01 * acos(sin(start_lat) * sin(end_lat) +
                                  cos(start_lat) * cos(end_lat) * cos(start_long - end_long))
            if dist < 50:
                return entry
        return curr_subscriber_coordinate

    def fetch_curr_temp(self, latitude, longitude):
        """
        Fetches the current temperature with description of the given coordinates.
        Parameters:
            latitude: latitude of the coordinate
            longitude: longitude of the coordinate.
        Returns:
            list containing current temperature in Celcius in first entry and weather description in second entry.
        """
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

    def calc_avg_temp(self, latitude, longitude):
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
            logger.info("Request to weatherbit API for {} weather successful.".format(start_date))
        avg_temp = sum(last_five_days_temp) / len(last_five_days_temp)
        return avg_temp
