#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes.utils import utils

# django imports.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

# include apps from website/urls.py.
def include_apps(apps=[], auto_include=False):
	if dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
		return []
	if auto_include:
		apps = []
		for _name_ in os.listdir(f"apps/"):
			if _name_ not in [".DS_Store"] and os.path.isdir(f"apps/{_name_}"): apps.append(_name_)
	urlpatterns = []
	for name in apps:
		_path_ = f"apps/{name}/"
		#try:
		if Files.exists(f"{_path_}/views.py"):
			l_path = f"{_path_}/views.py"
			urlpatterns.append(
				path('', include(f"apps.{name}.views"))
			)
		if Files.exists(f"{_path_}/requests.py"):
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
	if dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
		return []
	urls, landing_page = [], False
	for view in views:
		if view.type.lower() in ["view", "documentationview"] and not landing_page and view.landing_page:
			landing_page = True
			if view.auth_required:
				if view.except_xframe:
					urls.append(path("", view.__auth_xframe_except_view__))
					urls.append(path("/", view.__auth_xframe_except_view__))
				else:
					urls.append(path("", view.__auth_view__))
					urls.append(path("/", view.__auth_view__))
			else:
				if view.except_xframe:
					urls.append(path("", view.__xframe_except_view__))
					urls.append(path("/", view.__xframe_except_view__))
				else:
					urls.append(path("", view.__view__))
					urls.append(path("/", view.__view__))
		if view.auth_required:
			urls.append(
				path(gfp.clean(view.url, remove_first_slash=True, remove_last_slash=True)+"/", view.__auth_view__),
			)
		else:
			urls.append(
				path(gfp.clean(view.url, remove_first_slash=True, remove_last_slash=True)+"/", view.__view__),
			)
	return urls
	
# the django request object class.
class Request(Object):
	# do not forget the self.parameters's functions.
	def __init__(self,
		# the base path (required; if url path is null) [#1 argument].
		base=None,
		# the requests id (required) [#2 argument].
		id=None, 
		# the url path (optional).
		url=None,
		# the w3bsite.Website object (required).
		website=None,
		# authentication required.
		auth_required=False,
		# root permission required.
		root_required=False,
		# overwrite default maintenance (bool) (leave None to use website.maintenance).
		maintenance=None,
	):


		# docs.
		DOCS = {
			"module":"website.views.Request", 
			"initialized":False,
			"description":[], 
			"chapter": "Views", }

		# defaultss.
		Object.__init__(self)
		self.parameters = dev0s.response.parameters

		# variables.
		self.base = base
		self.id = id
		if url == None:
			self.url = gfp.clean(f"{base}/{id}/", remove_first_slash=True)
		else:
			self.url = gfp.clean(url.replace("/$id",f"/{self.id}"), remove_last_slash=True, remove_first_slash=True)+"/"
		if self.base == None: 
			self.base = gfp.clean(FilePath(self.url).base(back=1), remove_last_slash=True)+"/"
		self.url = gfp.clean(self.url, remove_first_slash=True).replace(".html", "")
		self.base = gfp.clean(self.base, remove_first_slash=True)
		self.type = "Request"
		self.website = website
		self.auth_required = auth_required
		self.root_required = root_required
		self.maintenance_ = maintenance
		if self.maintenance_ == None: self.maintenance_ = self.website.maintenance

		# checks.
		if self.website.__class__.__name__ not in ["Website"]:
			raise dev0s.exceptions.InvalidUsage(f"You forgot to pass the initialized w3bsite.Website object as the [website] parameter ({self.url}).")

	# response functions.
	def success(self, message, arguments={}):
		return dev0s.response.success(message, arguments, django=True)
	def error(self, error):
		return dev0s.response.error(error, django=True)
	def response(self, response):
		if isinstance(response, (JsonResponse, HttpResponse)):
			return response
		else:
			try:
				return JsonResponse(response.dict(safe=True), safe=False)
			except AttributeError:
				return JsonResponse(response, safe=False)

	# default responses.
	def _403(self, request=None):
		return self.error(f"Permission denied [403] ({self.url}).")
	def _404(self, request=None, error=None):
		return self.error(f"Page not found [404] ({self.url}).")
	def _500(self, request=None, error=None):
		info = utils.catch_error(error)
		return self.error(f"Server error [500] ({self.url}).")
	def _503(self, request=None):
		return self.error(f"Domain is under maintenance [503] ({self.url}).")
	def permission_denied(self, request=None):
		return self._403(request=request)
	def maintenance(self, request=None):
		return self._503(request=request)

	"""
	the view functions.
	 - the request() function must be overwritten.
	 - the __auth_view__ & __view__ are called before and should not be overwritten. """
	def request(self, request):
		return self.error(f"You did not define a default request() function for request [{self.url}].")
	def __view__(self, request, count=True):

		# count request.
		if count:
			self.website.metrics.count_api_request(request, data={
				"url":self.url,
			})

		# maintenance.
		if self.maintenance_:
			return self.maintenance(request=request)

		# make request.
		try: 
			response = self.request(request)
		except Exception as e: return self._500(request, error=e)
		return self.response(response)

		#
	def __auth_view__(self, request, count=True):
		
		# count request.
		if count:
			self.website.metrics.count_api_request(request, data={
				"url":self.url,
			})

		# check authenticated.
		if self.auth_required:
			response = self.website.users.authenticated(request)
			if not response.success: return self.response(response)

		# check root permissions.
		if self.root_required:
			response = self.website.users.root_permission(request)
			if not response.success: return self.response(response)

		# default __view__.
		return self.__view__(request, count=False)

	#

# the django view object class.
class View(Object):
	# do not forget the self.parameters's functions.
	def __init__(self, 
		# the base path (required; if url path is null) [#1 argument].
		base=None,
		# the views id (required) [#2 argument].
		id=None, 
		# the url path (optional).
		url=None,
		# the html path (optional).
		html=None,
		# the w3bsite.Website object (required).
		website=None,
		# enable if this view is the [/] landing page.
		landing_page=False,
		# authentication required.
		auth_required=False,
		# root permission required.
		root_required=False,
		# overwrite default maintenance (bool) (leave None to use website.maintenance).
		maintenance=None,
		# except xframe for the view.
		except_xframe=False,
		# the object type (do not edit).
		type="View",
	):

		# docs.
		DOCS = {
			"module":"website.views.View", 
			"initialized":False,
			"description":[], 
			"chapter": "Views", }

		# defaults.
		Object.__init__(self)
		self.parameters = dev0s.response.parameters

		# vars.
		self.base = base
		self.id = id
		self.website = website
		self.landing_page = landing_page
		self.type = type
		if url == None:
			self.url = gfp.clean(f"{base}/{id}/", remove_first_slash=True)
		else:
			self.url = gfp.clean(url.replace("/$id",f"/{self.id}"), remove_last_slash=True, remove_first_slash=True)+"/"
		if self.base == None: 
			self.base = gfp.clean(FilePath(self.url).base(back=1), remove_last_slash=True)+"/"
		if html != None:
			if len(html) >= len(f"/apps/") and html[:len(f"/apps/")] == f"/apps/": html = html[len(f"/apps"):]
			elif len(html) >= len(f"apps/") and html[:len(f"apps/")] == f"apps/": html = html[len(f"apps/"):]
			self.html = gfp.clean(html.replace("/$id",f"/{self.id}"))
			self.app = gfp.clean(self.html, remove_first_slash=True, remove_last_slash=True, remove_double_slash=True).split("/")[0]
		else:
			self.app = gfp.clean(self.base, remove_first_slash=True, remove_last_slash=True, remove_double_slash=True).split("/")[0]
			l_base = gfp.clean(str(self.base), remove_last_slash=True)+"/"
			if len(l_base) >= len(f"{self.app}/{self.app}") and l_base[:len(f"{self.app}/{self.app}")] == f"{self.app}/{self.app}": l_base = l_base[len(f"{self.app}/"):]
			elif len(l_base) >= len(f"{self.app}/") and l_base[:len(f"{self.app}/")] == f"{self.app}/": l_base = l_base[len(f"{self.app}/"):]
			self.html = gfp.clean(f"{self.app}/html/{l_base}/{self.id}.html")
		self.base = gfp.clean(self.base, remove_last_slash=True)+"/"
		self.url = gfp.clean(self.url.replace(".html", ""), remove_first_slash=True, remove_last_slash=True)+"/"
		self.html = gfp.clean(self.html)
		self.type = type
		self.auth_required = auth_required
		self.root_required = root_required
		self.maintenance_ = maintenance
		if self.maintenance_ == None: self.maintenance_ = self.website.maintenance
		self.except_xframe = except_xframe

		# check html.
		if self.type.lower() in ["view"] and "w3bsite/" not in self.html:
			path = FilePath(f"apps/{self.app}/")
			if Files.exists(path):
				path = Files.join(path, "html")
				if not Files.exists(path): 
					dev0s.response.log(f"&ORANGE&Creating&END& html base [{path}].")
					Files.create(path, directory=True)
				path = Files.join("apps", self.html)
				if not Files.exists(path):
					dev0s.response.log(f"&ORANGE&Creating&END& default html view [{path}].")
					base = FilePath(path).base(back=1)
					if not Files.exists(base): Files.create(base, directory=True)
					Files.copy(f"{SOURCE_PATH}/classes/django/lib/html/view.html", path)

		# checks.
		if self.website.__class__.__name__ not in ["Website"]:
			raise dev0s.exceptions.InvalidUsage(f"You forgot to pass the initialized w3bsite.Website object as the [website] parameter ({self.url}).")

		#

	# render functions.
	def render(self, 
		# the request (obj) (#1)
		request, 
		# overwrite default template data. #2
		template_data=None,
		# overwrite default html #3.
		html=None,
		# the response's status code.
		status=200,
	):
		if html == None: html = self.html
		return render(request, str(html), self.template(template_data), status=status)
	def error(self, 
		# the django request parameter.
		request, 
		# the error title.
		title="Warning!",
		# the error title.
		message="Some error occured (#000000).",
		# the error icon (the static directory is root).
		icon="media/icons/warning.png", 
		# the redirect button text (right button).
		redirect_button="Ok",
		# the redirect url.
		redirect="/dashboard/home/",
		# overwrite default template data.
		template_data=None,
		# pass arguments by dict.
		serialized={},
	):
		if serialized != {}:
			title, message, icon, redirect_button, redirect = Dictionary(serialized).unpack({
				"title":"Warning!",
				"message":"Some error occured (#000000).",
				"icon":"media/icons/warning.png",
				"redirect_button":"Ok",
				"redirect":"/dashboard/home/",
			})
		if template_data == None: template_data = self.website.template_data
		if template_data == None: template_data = {}
		title = title.replace("\n","")
		message = message.replace("\n","")
		template_data["ERROR"] = {
			"title":title,
			"message":message,
			"icon":icon,
			"redirect":redirect,
			"redirect_button":redirect_button,
		}
		return self.render(request=request, template_data=template_data, html=f"w3bsite/classes/apps/defaults/html/error.html")

	# default renders.
	def _403(self, request, template_data=None):
		return self.render(request=request, template_data=template_data, status=403, html=f"w3bsite/classes/apps/defaults/html/permission_denied.html")
	def _404(self, request, template_data=None):
		return self.render(request=request, template_data=template_data, status=404, html=f"w3bsite/classes/apps/defaults/html/404.html")
	def _500(self, request, template_data=None, error=None):
		if template_data == None: template_data = self.website.template_data
		if template_data == None: template_data = {}
		info = utils.catch_error(error)
		traceback, debug = None, False
		if not dev0s.env.get("PRODUCTION", format=bool, default=True) or dev0s.env.get("DEBUG", format=bool, default=False):
			debug = True
			traceback = info["traceback"]
		return self.render(request=request, html=f"w3bsite/classes/apps/defaults/html/500.html", status=500, template_data=self.template(old=template_data, new={
			"ERROR_ID":str(info["id"]),
			"DEBUG":str(debug),
			"TRACEBACK":str(traceback),
			"URL":self.url,
		}))
	def _503(self, request, template_data=None):
		return self.render(request=request, template_data=template_data, status=503, html=f"w3bsite/classes/apps/defaults/html/maintenance.html")
	def permission_denied(self, request, template_data=None):
		return self._403(request, template_data=template_data)
	def maintenance(self, request, template_data=None):
		return self._503(request, template_data=template_data)

	# append template data.
	def template(self, new={}, old=None, safe=False):
		if old == None: old = self.website.template_data
		return utils.template(old=old, new=new, safe=safe)

	# the view functions.
	# the view() function can be overwritten.
	# the __auth_view__ & __view__ are called before and should not be overwritten.
	def view(self, request):
		return self.render(request)
	def __view__(self, request, count=True):

		# count request.
		if count:
			self.website.metrics.count_web_request(request, data={
				"url":self.url,
			})

		# maintenance.
		if self.maintenance_:
			return self.maintenance(request=request)

		# default view.
		try: 
			return self.view(request)
		except Exception as e: return self._500(request, error=e)
		return self.render(request=request)

		#
	@method_decorator(login_required)
	def __auth_view__(self, request, count=True):

		# count request.
		if count:
			self.website.metrics.count_web_request(request, data={
				"url":self.url,
			})

		# check root permission.
		if self.root_required:
			response = self.website.users.root_permission(request)
			if not response.success: return self._404(request)

		# return __view__.
		return self.__view__(request, count=False)

		#
	@method_decorator(xframe_options_exempt)
	def __xframe_except_view__(self, request):

		# count request.
		if count:
			self.website.metrics.count_web_request(request, data={
				"url":self.url,
			})

		# return __view__.
		return self.__view__(request, count=False)
	@method_decorator(login_required)
	@method_decorator(xframe_options_exempt)
	def __auth_xframe_except_view__(self, request):

		# count request.
		if count:
			self.website.metrics.count_web_request(request, data={
				"url":self.url,
			})

		# check root permission.
		if self.root_required:
			response = self.website.users.root_permission(request)
			if not response.success: return self._404(request)

		# return __view__.
		return self.__view__(request, count=False)
	#

#

















# template data object !!! DEPRICATED !!!.
class TemplateData(Object):
	def __init__(self, data={}):
		# defaults.
		Object.__init__(self)
		self.assign(data)
	# return raw data.
	def raw(self):
		return self.attributes()
		

#