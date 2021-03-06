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
	urls, landing_page = [], False
	for view in views:
		if view.type.lower() in ["view", "documentationview"] and not landing_page and view.landing_page:
			landing_page = True
			urls.append(path("", view.view))
			urls.append(path("/", view.view))
		urls.append(
			path(gfp.clean(view.url, remove_first_slash=True), view.view),
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
		self.parameters = r3sponse.parameters

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
		self.type = "request"
		self.template_data = template_data
	def view(self, request):
		# default view, user needs to create default def request(self, request)
		# can be overwritten with default def view(self, request):
		try: 
			response = self.request(request)
		except Exception as e: return self.response(utils.utils.catch_error(e))
		return self.response(response)
	def success(self, message, arguments={}):
		return r3sponse.success(message, arguments, django=True)
	def error(self, error):
		return r3sponse.error(error, django=True)
	def response(self, response):
		if isinstance(response, JsonResponse):
			return response
		else:
			try:
				return JsonResponse(response.dict(), safe=False)
			except AttributeError:
				return JsonResponse(response)
	def maintenance(self, request=None):
		return r3sponse.error("Domain is under maintenance.")
	def permission_denied(self, request=None):
		return self.error("Permission denied.")
	# do not forget the self.parameters's functions.

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

		# defaults.
		syst3m.objects.Object.__init__(self)
		self.parameters = r3sponse.parameters

		# vars.
		self.base = base
		self.id = id
		self.template_data = template_data
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

		# check html.
		if self.type.lower() in ["view"] and "w3bsite/" not in self.html:
			path = FilePath(f"apps/{self.app}/")
			if Files.exists(path):
				path = Files.join(path, "html")
				if not Files.exists(path): 
					r3sponse.log(f"&ORANGE&Creating&END& html base [{path}].")
					Files.create(path, directory=True)
				path = Files.join("apps", self.html)
				if not Files.exists(path):
					r3sponse.log(f"&ORANGE&Creating&END& default html view [{path}].")
					base = FilePath(path).base(back=1)
					if not Files.exists(base): Files.create(base, directory=True)
					os.system(f"cp {SOURCE_PATH}/example/view.html {path}")

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
		if isinstance(template_data, (Dictionary, r3sponse.ResponseObject)): 
			template_data = template_data.raw()
		return render(request, html, template_data)
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
		title = title.replace("\n","")
		message = message.replace("\n","")
		template_data["ERROR"] = {
			"title":title,
			"message":message,
			"icon":icon,
			"redirect":redirect,
			"redirect_button":redirect_button,
		}
		if isinstance(template_data, (Dictionary, r3sponse.ResponseObject)): 
			template_data = template_data.raw()
		return render(request, f"w3bsite/classes/apps/defaults/html/error.html", template_data)
	def maintenance(self, request, template_data=None):
		if template_data == None: template_data = self.template_data
		if isinstance(template_data, (Dictionary, r3sponse.ResponseObject)): 
			template_data = template_data.raw()
		return render(request, f"w3bsite/classes/apps/defaults/html/maintenance.html", template_data)
	def permission_denied(self, request, template_data=None):
		if template_data == None: template_data = self.template_data
		if isinstance(template_data, (Dictionary, r3sponse.ResponseObject)): 
			template_data = template_data.raw()
		return render(request, f"w3bsite/classes/apps/defaults/html/permission_denied.html", template_data)
	# do not forget the self.parameters's functions.









# template data object !!! DEPRICATED !!!.
class TemplateData(syst3m.objects.Object):
	def __init__(self, data={}):
		# defaults.
		syst3m.objects.Object.__init__(self)
		self.assign(data)
	# return raw data.
	def raw(self):
		return self.attributes()
		

#