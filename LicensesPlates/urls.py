from LicensesPlates import views as myapp_views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
                    url(r'^check', myapp_views.capturePlate, name='check'),
                    url(r'^$', myapp_views.home, name='home'),
                ]