from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [ url('add_participant', views.add_participant, name='add_participant'), ]