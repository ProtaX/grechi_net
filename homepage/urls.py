from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url('add_participant', views.add_participant, name='add_participant'),
    path('email_invite/<str:email>', views.email_invite, name='email_invite'),
    path('validate_invite/<str:invite_id>', views.validate_invite, name='validate_invite'),
    path('logout', views.logout, name='logout'),
    path('load_prices', views.load_prices, name='load_prices'),
    path('load_comments', views.load_comments, name='load_comments'),
    path('add_comment', views.add_comment, name='add_comment'),
    path('update_comment', views.update_comment, name='update_comment'),
]
