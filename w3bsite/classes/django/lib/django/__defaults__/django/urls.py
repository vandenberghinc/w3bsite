#!/usr/bin/env python3

# imports.
from django.contrib import admin
from django.urls import path, include
from classes.config import *
urlpatterns = []
if not dev0s.system.env.get("MIGRATIONS", format=bool, default=False):

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
	# Logging.
	#

	# import the default logging requests.
	imports += website.apps.logging.requests.urls 

	# ______________________________________________________________________________________
	#
	# Metrics.
	#

	# import the default metrics requests.
	imports += website.apps.metrics.requests.urls 

	# ______________________________________________________________________________________
	#
	# Defaults.
	#

	# urlpatterns.
	urlpatterns = [] + imports

	# default handlers.
	if not dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
		handler500 = website.apps.exceptions._500
		handler404 = website.apps.exceptions._404

	#
	#