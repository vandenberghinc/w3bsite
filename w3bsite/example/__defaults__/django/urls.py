#!/usr/bin/env python3

# imports.
from django.contrib import admin
from django.urls import path, include
from classes.config import *

# limit migrations
if  dev0s.env.get("MIGRATIONS", format=bool, default=False): urlpatterns = []
else:
	

	# ______________________________________________________________________________________
	#
	# Inlude Apps.
	#

	# autmatically include all apps that contain a ./views.py or ./requests.py file.
	imports = w3bsite.views.include_apps(auto_include=True)

	# manually include apps.
	#imports = w3bsite.views.include_apps([
	#	"dashboard",
	#)

	# ______________________________________________________________________________________
	#
	# Authentication.
	#

	# import the default authentication requests.
	imports += website.apps.authentication.requests.urls 

	# import the default authentication views.
	#imports += website.apps.authentication.views.urls 

	# ______________________________________________________________________________________
	#
	# Payments.
	#

	# import the default payments requests.
	#imports += website.apps.payments.requests.urls 

	# import the default payments views.
	#imports += website.apps.payments.views.urls 

	# ______________________________________________________________________________________
	#
	# dev0s.defaults.
	#
	urlpatterns = [
		# uncomment the following line to se the default django admin interface.
		#path('admin/', admin.site.urls)
	] + imports

#