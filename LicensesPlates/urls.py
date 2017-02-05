from LicensesPlates import views as myapp_views
from django.conf.urls import url

urlpatterns = [
                    url(r'^check', myapp_views.capturePlate, name='check'),
                    url(r'^$', myapp_views.home, name='home'),
              ]
