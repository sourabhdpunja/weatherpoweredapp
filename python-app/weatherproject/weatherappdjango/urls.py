from django.conf.urls import url
from weatherappdjango.views import post_credentials
from weatherappdjango.views import get_all_credentials

urlpatterns = [
    url(r'postcredentials/', post_credentials, name='post_credentials'),
    url(r'getallcredentials/', get_all_credentials, name='get_all_credentials')
];
