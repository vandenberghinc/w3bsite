from django.contrib import admin
from django.urls import path, include
from classes.config import *
urlpatterns = [
	#path('admin/', admin.site.urls),
]
urlpatterns += website.apps.authentication.requests.urls 
urlpatterns += website.apps.authentication.views.urls
urlpatterns += website.apps.payments.requests.urls
urlpatterns += website.apps.payments.views.urls
urlpatterns += w3bsite.views.include_apps(auto_include=True)