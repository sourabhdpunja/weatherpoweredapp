from django.conf.urls import url
from weatherappdjango.views import postCredentials
from weatherappdjango.views import getAllCredentials

urlpatterns = [
    url(r'postcredentials/', postCredentials, name='postCredentials'),
    url(r'getallcredentials/', getAllCredentials, name='getAllCredentials')
];
