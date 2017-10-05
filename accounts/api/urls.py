from django.conf.urls import url
from django.contrib import admin

from .views import ( 
	UsersCreateAPIView,
	UserLoginAPIView,
	)

urlpatterns = [
	url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
	url(r'^register/$', UsersCreateAPIView.as_view(), name='register'),
]
