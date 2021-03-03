#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# the x views.
class Views(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())
		
		# urlpatterns.
		self.urls = w3bsite.build_urls([
			self.Purchase(defaults=defaults),
			self.Cancel(defaults=defaults),
		])

	# purchase.
	class Purchase(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "dashboard/payments/", "purchase", template_data=self.template_data, html="/payments/purchase.html")
		def view(self, request):
			if MAINTENANCE: return self.maintenance(request)
			return self.render(request)

	# cancel.
	class Cancel(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "dashboard/payments/", "cancel", template_data=self.template_data, html="/payments/cancel.html")
		def view(self, request):
			if MAINTENANCE: return self.maintenance(request)
			return self.render(request)


# the x requests.
class Requests(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		defaults=None,
	):
		# defaults.
		defaults.rate_limit = rate_limit
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())
		
		# urlpatterns.
		self.urls = w3bsite.build_urls([
			self.SignUp(defaults=defaults),
		])

	# sign up.
	class SignUp(views.Request):
		def __init__(self, defaults=None,):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.Request.__init__(self, "requests/authentication/", "signup")
		def view(self, request):

			# permission denied.
			#return self.permission_denied()

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# check signup rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="signup", limit=3, reset_minutes=3600*24, increment=False)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = r3sponse.get_request_parameters(request, [
				"username",
				"email",
				"password",
				"verify_password",])
			if not response.success: return self.response(response)
			optional_parameters, _ = r3sponse.get_request_parameters(request, [
				"name",], optional=True)

			# make request.
			response = self.users.create(
				email=parameters["email"],
				username=parameters["username"],
				password=parameters["password"],
				verify_password=parameters["verify_password"],
				name=optional_parameters["name"],)
			if not response.success: return self.response(response)

			# increment.
			_response_ = self.rate_limit.increment(ip=utils.get_client_ip(request), mode="signup")
			if not _response_.success: return _response_

			# send activation code.
			_response_ = SendCode().send_code(email=parameters["email"], mode="activation", request=request)
			if not _response_.success: return self.response(_response_)

			# return create response.
			if response.success:
				del response["user"]
			return self.response(response)
