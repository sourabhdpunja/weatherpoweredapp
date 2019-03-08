from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
import logging
import os

# environment variable import
from decouple import config

# custom imports
from django.conf import settings

logger = logging.getLogger(__name__)

# Class which defines the email properties such as subject, body, image.
class Email:
    def __init__(self, curr_temp, temp_desc, location, avg_temp):
        self.curr_temp = curr_temp
        self.temp_desc = temp_desc
        self.location = location
        self.avg_temp = avg_temp
        self.subject = ''
        self.html_body = ''
        self.text_body = ''
        self.image = None

    def create_emailmessage_obj(self, to_address):
        """
        Builds EmailMessage Instance using to_address.
        Parameters:
            to_address: subscriber email id
        Returns:
            EmailMessage Instance
        """
        self.create_email()
        email_message = EmailMultiAlternatives(self.subject, self.html_body,
                                               config('FROM_EMAIL_ADDRESS'), [to_address])
        email_message.attach_alternative(self.html_body, "text/html")
        email_message.content_subtype = 'html'
        email_message.mixed_subtype = 'related'
        if self.image is not None:
            email_message.attach(self.image)
        return email_message

    def create_email(self):
        """
        Creates email object with subject and body defined based on the average temperature.
        If current temperature less than 5 degrees from the average then cold email is built.
        If current temperature more than 5 degrees from the average then warm email is built.
        If current temperature within 5 degrees from the average then normal email is built.
        Returns:
            Nothing is returned
        """
        if self.curr_temp < self.avg_temp - 5:
            self.create_personalised_email("COLD")
        elif self.curr_temp > self.avg_temp + 5:
            self.create_personalised_email("WARM")
        else:
            self.create_personalised_email("NORMAL")

    def create_personalised_email(self, temp_state):
        """ Helper function to build the subject and body of email object based on temperature state"""
        if temp_state == "COLD":
            self.subject = "Not so nice out? That's okay, enjoy a discount on us."
            self.build_cold_email_body()
        elif temp_state == "NORMAL":
            self.subject = "Enjoy a discount on us."
            self.build_normal_email_body()
        elif temp_state == "WARM":
            self.subject = "It's nice out! Enjoy a discount on us."
            self.build_warm_email_body()
        else:
            logger.error("Invalid temp_state given. Should be one of (COLD, NORMAL, WARM)")
            raise ValueError

    def build_cold_email_body(self):
        """ Helper function to build the body of cold email"""
        self.html_body = render_to_string('email/cold_temp_mail.html',
                                          {'curr_temp': self.curr_temp,
                                           'curr_state': self.temp_desc,
                                           'location': self.location})
        self.text_body = strip_tags(self.html_body)
        try:
            filehandle = open(os.path.join(settings.BASE_DIR, 'weather-app-server', 'weatherapp', 'images', 'cold.gif'), 'rb')
        except IOError:
            logger.error("cold.gif file does not exist in images folder")
            return
        self.image = MIMEImage(filehandle.read())
        self.image.add_header('Content-ID', '<image1>')
        filehandle.close()

    def build_warm_email_body(self):
        """ Helper function to build the body of warm email"""
        self.html_body = render_to_string('email/warm_temp_mail.html',
                                          {'curr_temp': self.curr_temp,
                                           'curr_state': self.temp_desc,
                                           'location': self.location})
        self.text_body = strip_tags(self.html_body)
        try:
            filehandle = open(os.path.join(settings.BASE_DIR, 'weather-app-server', 'weatherapp', 'images', 'good_weather.jpg'), 'rb')
        except IOError:
            logger.error("sun_bath.gif file does not exist in images folder")
            return
        self.image = MIMEImage(filehandle.read())
        self.image.add_header('Content-ID', '<image1>')
        filehandle.close()

    def build_normal_email_body(self):
        """ Helper function to build the body of normal email"""
        self.html_body = render_to_string('email/normal_temp_mail.html',
                                          {'curr_temp': self.curr_temp,
                                           'curr_state': self.temp_desc,
                                           'location': self.location})
        self.text_body = strip_tags(self.html_body)
        try:
            filehandle = open(os.path.join(settings.BASE_DIR, 'weather-app-server', 'weatherapp', 'images', 'normal.gif'), 'rb')
        except IOError:
            logger.error("normal.gif file does not exist in images folder")
            return
        self.image = MIMEImage(filehandle.read())
        self.image.add_header('Content-ID', '<image1>')
        filehandle.close()







