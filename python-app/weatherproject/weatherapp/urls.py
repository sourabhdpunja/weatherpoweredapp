from django.conf.urls import url
# Custom imports
from weatherapp.views import post_subscriber
from weatherapp.views import get_all_subscribers

urlpatterns = [
    url(r'postsubscriber/', post_subscriber, name='post_subscriber'),
    url(r'getallsubscribers/', get_all_subscribers, name='get_all_subscribers')
];
