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

			# post sign up.
			"""
			_response_ = self.users.load_data(email=parameters["email"])
			if not r3sponse.success(_response_): return self.response(_response_)
			data = _response_["data"]
			rsa = w3bsite.rsa.RSA()
			_response_ = rsa.generate_keys()
			if not r3sponse.success(_response_): return self.response(_response_)
			_response_ = self.aes.encrypt(rsa.public_key_pem)
			if not r3sponse.success(_response_): return self.response(_response_)
			public_key = _response_["encrypted"]
			_response_ = self.aes.encrypt(rsa.private_key_pem)
			if not r3sponse.success(_response_): return self.response(_response_)
			private_key = _response_["encrypted"]
			data["rsa"] = {
				"public_key":public_key.decode(),
				"private_key":private_key.decode(),
			}
			_response_ = self.aes.encrypt(parameters["password"])
			if not r3sponse.success(_response_): return self.response(_response_)
			data["account"] = {
				"password":_response_["encrypted"].decode(),
			}
			_response_ = self.users.save_data(email=parameters["email"], data=data)
			if not r3sponse.success(_response_): return self.response(_response_)
			"""

			# send activation code.
			_response_ = SendCode().send_code(email=parameters["email"], mode="activation", request=request)
			if not r3sponse.success(_response_): return self.response(_response_)

			# return create response.
			if response.success:
				del response["user"]
			return self.response(response)
