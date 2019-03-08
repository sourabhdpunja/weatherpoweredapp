import logging
from django.core import mail
from django.core.management.base import BaseCommand

# environment variable import
from decouple import config

# Custom imports
from weatherapp.emailclass.email import Email
from weatherapp.utils import calc_avg_temp,get_closest_coordinate,fetch_curr_temp
from weatherapp.models import Subscribers

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        subscribers_list = Subscribers.objects.all()

        if len(subscribers_list) <= 0:
            logger.info("No subscribers present in subscribers table.")
            return

        location_to_mail_map = {}
        email_messages_obj_list = []

        for subscriber in subscribers_list:

            to_email_id = subscriber.emailId
            location = subscriber.location
            latitude = subscriber.latitude
            longitude = subscriber.longitude
            curr_subscriber_coordinate = (latitude, longitude)

            if curr_subscriber_coordinate in location_to_mail_map:
                email_message = location_to_mail_map.get(curr_subscriber_coordinate)
            else:
                # get closest coordinate within 50km distance of the current coordinate if present.
                closest_coordinate = get_closest_coordinate(curr_subscriber_coordinate, location_to_mail_map.keys())
                if closest_coordinate in location_to_mail_map:
                    email_message = location_to_mail_map.get(closest_coordinate)
                    location_to_mail_map[curr_subscriber_coordinate] = email_message
                else:
                    curr_temp_state = fetch_curr_temp(latitude, longitude)
                    avg_temp = calc_avg_temp(latitude, longitude)
                    email_message = Email(curr_temp_state[0], curr_temp_state[1], location, avg_temp)
                    location_to_mail_map[curr_subscriber_coordinate] = email_message

            email_obj = email_message.create_emailmessage_obj(to_email_id)
            email_messages_obj_list.append(email_obj)
            logger.info("Created Email Object with to {} and from {}"
                        .format(to_email_id, config('FROM_EMAIL_ADDRESS')))

        # Send multiple emails using same SMTP connection
        if len(email_messages_obj_list) > 0:
            connection = mail.get_connection(fail_silently=True)
            connection.send_messages(email_messages_obj_list)