from django.conf.urls import url
from weatherappdjango.views import postCredentials

urlpatterns = [
    url(r'postcredentials/', postCredentials, name='postCredentials'),
    # url(r'getCredentials/', views.index, name='index')
];
