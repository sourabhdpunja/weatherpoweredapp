from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import logging

logger = logging.getLogger(__name__)

# Class which defines the email properties such as subject, body, image.
class Email:
    def __init__(self, curr_temp, temp_desc, location):
        self.curr_temp = curr_temp
        self.temp_desc = temp_desc
        self.location = location
        self.subject = ''
        self.html_body = ''
        self.text_body = ''
        self.image = ''

    def create_email(self, avg_temp):
        """
        Creates email object with subject and body defined based on the average temperature.
        If current temperature less than 5 degrees from the average then cold email is built.
        If current temperature more than 5 degrees from the average then warm email is built.
        If current temperature within 5 degrees from the average then normal email is built.
        Parameters:
            avg_temp: average temperature of the location
        Returns:
            Nothing is returned
        """
        if self.curr_temp < avg_temp - 5:
            self.create_personalised_email("COLD")
        elif self.curr_temp > avg_temp + 5:
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
            filehandle = open('.\weatherapp\images\\cold.gif', 'rb')
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
            filehandle = open('.\weatherapp\images\\good_weather.jpg', 'rb')
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
            filehandle = open('.\weatherapp\images\\normal.gif', 'rb')
        except IOError:
            logger.error("normal.gif file does not exist in images folder")
            return
        self.image = MIMEImage(filehandle.read())
        self.image.add_header('Content-ID', '<image1>')
        filehandle.close()







