from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage


class Email:
    def __init__(self, to_address, curr_temp, temp_desc):
        self.to_address = to_address
        self.curr_temp = curr_temp
        self.temp_desc = temp_desc
        self.subject = ''
        self.html_body = ''
        self.text_body = ''
        self.image = ''

    def create_email(self, avg_temp):
        if self.curr_temp < avg_temp - 5:
            self.create_personalised_email("COLD")
        elif self.curr_temp > avg_temp + 5:
            self.create_personalised_email("WARM")
        else:
            self.create_personalised_email("NORMAL")

    def create_personalised_email(self, temp_state):
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
            raise ValueError

    def build_cold_email_body(self):
        self.html_body = render_to_string('email/cold_temp_mail.html',
                                          {'curr_temp': self.curr_temp, 'curr_state': self.temp_desc})
        self.text_body = strip_tags(self.html_body)
        filehandle = open('.\weatherappdjango\images\\cold.gif', 'rb')
        self.image = MIMEImage(filehandle.read())
        self.image.add_header('Content-ID', '<image1>')
        filehandle.close()

    def build_warm_email_body(self):
        self.html_body = render_to_string('email/warm_temp_mail.html',
                                          {'curr_temp': self.curr_temp, 'curr_state': self.temp_desc})
        self.text_body = strip_tags(self.html_body)
        filehandle = open('.\weatherappdjango\images\\sun_bath.gif', 'rb')
        self.image = MIMEImage(filehandle.read())
        self.image.add_header('Content-ID', '<image1>')
        filehandle.close()

    def build_normal_email_body(self):
        self.html_body = render_to_string('email/normal_temp_mail.html',
                                          {'curr_temp': self.curr_temp, 'curr_state': self.temp_desc})
        self.text_body = strip_tags(self.html_body)
        filehandle = open('.\weatherappdjango\images\\normal.gif', 'rb')
        self.image = MIMEImage(filehandle.read())
        self.image.add_header('Content-ID', '<image1>')
        filehandle.close()







