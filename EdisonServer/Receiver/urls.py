
from django.conf.urls import include, url
from Receiver import views

# http://127.0.0.1:8000/receiver/
urlpatterns = [
    url(r'^receive_message_data', views.receive_message_data, name='receive_message_data'),
    url(r'^receive_command', views.control, name='control'),
    url(r'^index', views.index, name='index'),
    url(r'^get_next_message', views.get_next_message, name='get_next_message'),
]

