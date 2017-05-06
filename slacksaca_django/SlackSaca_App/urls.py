from django.conf.urls import url
from . import views

app_name = 'SlackSaca_App'

urlpatterns = [
    url(r'^$', views.index),
    url(r'^oauth/$', views.slack_oauth),
]
