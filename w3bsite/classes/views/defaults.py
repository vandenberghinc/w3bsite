#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils

# django imports.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# include apps from website/urls.py.
def include_apps(apps=[], auto_include=False):
	if auto_include:
		apps = []
		for _name_ in os.listdir(f"apps/"):
			if _name_ not in [".DS_Store"] and os.path.isdir(f"apps/{_name_}"): apps.append(_name_)
	urlpatterns = []
	for name in apps:
		_path_ = f"apps/{name}/"
		#try:
		if os.path.exists(f"{_path_}/views.py"):
			l_path = f"{_path_}/views.py"
			urlpatterns.append(
				path('', include(f"apps.{name}.views"))
			)
		if os.path.exists(f"{_path_}/requests.py"):
			l_path = f"{_path_}/requests.py"
			urlpatterns.append(
				path('', include(f"apps.{name}.requests"))
			)
		"""
		except Exception as e:
			sys.tracebacklimit = -1
			raise ImportError(f"Failed to import application [{name}], file [{l_path}], error: {e}.")
		"""
	return urlpatterns

# build url patterns.
def build_urls(views=[]):
	urls, landing_page = [], False
	for view in views:
		if view.type.lower() in ["view", "documentationview"] and not landing_page and view.landing_page:
			landing_page = True
			urls.append(path("", view.view))
			urls.append(path("/", view.view))
		urls.append(
			path(utils.__clean_url__(view.url, strip_first_slash=True), view.view),
		)
	return urls

# the django request object class.
class Request(syst3m.objects.Object):
	def __init__(self,
		# the base path (required; if url path is null) [#1 argument].
		base=None,
		# the requests id (required) [#2 argument].
		id=None, 
		# the url path (optional).
		url=None,
		# template data (optional).
		template_data={},
	):

		# defaultss.
		syst3m.objects.Object.__init__(self)

		# variables.
		self.id = id
		if url == None:
			self.url = f"{base}/{id}/".replace("//",'/').replace("//",'/')
		else:
			self.url = url
		self.base = Formats.FilePath(self.url).base(back=1)
		self.url = utils.__clean_url__(self.url, strip_first_slash=True).replace(".html", "")
		self.base = utils.__clean_url__(self.base, strip_first_slash=True)
		self.type = "request"
		self.template_data = template_data
	def view(self, request):
		return self.error_response("Define the self.view function.")
	def success_response(self, message, arguments={}):
		return r3sponse.success_response(message, arguments, django=True)
	def error_response(self, error):
		return r3sponse.error_response(error, django=True)
	def response(self, response):
		try:
			return JsonResponse(response.dict(), safe=False)
		except AttributeError:
			return JsonResponse(response)
	def get_parameter(self, request, identifier):
		return r3sponse.get_request_parameter(request, identifiers)
	def get_parameters(self, request, identifiers=[], optional=False):
		return r3sponse.get_request_parameters(request, identifiers, optional=optional)
	def maintenance(self, request=None):
		return r3sponse.error_response("Domain is under maintenance.")
	def permission_denied(self, request=None):
		return self.error_response("Permission denied.")

# the django view object class.
class View(syst3m.objects.Object):
	def __init__(self, 
		# the base path (required; if url path is null) [#1 argument].
		base=None,
		# the views id (required) [#2 argument].
		id=None, 
		# the url path (optional).
		url=None,
		# the html path (optional).
		html=None,
		# enable if this view is the [/] landing page.
		landing_page=False,
		# the template data (required).
		template_data={},
		# the object type (do not edit).
		type="View",
	):

		# defaultss.
		syst3m.objects.Object.__init__(self)

		# variables.
		self.id = id
		self.template_data = template_data
		self.landing_page = landing_page
		self.type = type
		if url == None:
			self.url = f"{base}/{id}/".replace("//",'/').replace("//",'/')
		else:
			self.url = url
		self.base = Formats.FilePath(self.url).base(back=1)
		if html != None:
			self.html = html
		else:
			self.html = f"{self.base}/{self.id}.html"
		self.base = utils.__clean_url__(self.base, strip_first_slash=True)
		self.url = utils.__clean_url__(self.url, strip_first_slash=True).replace(".html", "")
		self.html = utils.__clean_url__(self.html, strip_first_slash=True)
		self.type = type

		# check html.
		if self.type.lower() in ["view"]:
			fp = Formats.FilePath(f"{SOURCE_PATH}/example/")
			if not os.path.exists(f"templates/{self.html}"):
				base = utils.__clean_url__(Formats.FilePath(self.html).base(back=1), strip_first_slash=True)
				if not os.path.exists(base): os.system(f"mkdir -p templates/{base}")
				os.system(f"cp {SOURCE_PATH}/example/view.html templates/{self.html}")

		#
	#@w3bsite.views.method_decorator(w3bsite.views.login_required)
	def view(self, request):
		return self.render(request)
	def render(self, request, 
		# overwrite default template data. #2
		template_data=None,
		# overwrite default html #3.
		html=None,
	):
		if template_data == None: template_data = self.template_data
		if html == None: html = self.html
		try:
			return render(request, html, template_data.dict())
		except AttributeError:
			return render(request, html, template_data)
	def get_parameter(self, request, identifier):
		return r3sponse.get_request_parameter(request, identifiers)
	def get_parameters(self, request, identifiers=[], optional=False):
		return r3sponse.get_request_parameters(request, identifiers, optional=optional)
	def error(self, 
		# the django request parameter.
		request, 
		# the error title.
		title="Warning!",
		# the error title.
		message="Some error occured.",
		# the error icon (the static directory is root).
		icon="media/icons/warning.png", 
		# the redirect button text (right button).
		redirect_button="Ok",
		# the redirect url.
		redirect="/dashboard/home/",
		# overwrite default template data.
		template_data=None):
		if template_data == None: template_data = self.template_data
		template_data["ERROR"] = {
			"title":title,
			"message":message,
			"icon":icon,
			"redirect":redirect,
			"redirect_button":redirect_button,
		}
		try:
			return render(request, f"w3bsite/classes/apps/defaults/html/error.html", template_data.dict())
		except AttributeError:
			return render(request, f"w3bsite/classes/apps/defaults/html/error.html", template_data)
	def maintenance(self, request, template_data=None):
		if template_data == None: template_data = self.template_data
		try:
			return render(request, f"w3bsite/classes/apps/defaults/html/maintenance.html", template_data.dict())
		except AttributeError:
			return render(request, f"w3bsite/classes/apps/defaults/html/maintenance.html", template_data)
	def permission_denied(self, request, template_data=None):
		if template_data == None: template_data = self.template_data
		try:
			return render(request, f"w3bsite/classes/apps/defaults/html/permission_denied.html", template_data.dict())
		except AttributeError:
			return render(request, f"w3bsite/classes/apps/defaults/html/permission_denied.html", template_data)

# template data object.
class TemplateData(syst3m.objects.Object):
	def __init__(self, data={}):
		# defaults.
		syst3m.objects.Object.__init__(self)
		self.assign(data)
		

#