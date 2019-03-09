from django.conf.urls import url
# Custom imports
from weatherapp.views import post_subscriber

urlpatterns = [
    url(r'subscriber/', post_subscriber, name='post_subscriber'),
];
