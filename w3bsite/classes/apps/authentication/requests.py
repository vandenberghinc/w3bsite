#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# the authentication requests.
class Requests(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# urlpatterns.
		if dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
			self.urls = []
		else:
			send_code = self.SendCode(defaults=defaults)
			self.urls = views.build_urls([
				self.SignUp(defaults=defaults, send_code=send_code),
				self.SignIn(defaults=defaults),
				send_code,
				self.ResetPassword(defaults=defaults),
				self.Activate(defaults=defaults),
				self.Authenticated(defaults=defaults),
			])

	# sign up.
	class SignUp(views.Request):
		def __init__(self, defaults=None, send_code=None):
			views.Request.__init__(self, "requests/authentication/", "signup", website=defaults.website)
			self.assign(defaults.dict())
			self.send_code = send_code
		def request(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# check signup rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="signup", limit=3, reset_minutes=3600*24, increment=False)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = self.parameters.get(request, [
				"username",
				"email",
				"password",
				"verify_password",])
			if not response.success: return self.response(response)
			optional_parameters, _ = self.parameters.get(request, {
				"name":None,
			})

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
			_response_ = self.send_code.send_code(username=parameters["username"], mode="activation", request=request)
			if not _response_.success: return self.response(_response_)

			# return create response.
			if response.success:
				del response["user"]
			return self.response(response)

			
			#

	# sign in.
	class SignIn(views.Request):
		def __init__(self, defaults=None,):
			views.Request.__init__(self, "requests/authentication/", "signin", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: 
				self.website.metrics.count_auth_request(request, data={
					"url":self.url,
					"response":response,
				})
				return self.response(response)

			# check signin rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="signin", limit=10, reset_minutes=5, increment=True)
			if not response.success: 
				self.website.metrics.count_auth_request(request, data={
					"url":self.url,
					"response":response,
				})
				return self.response(response)

			# retrieve params.
			parameters, response = self.parameters.get(request, [
				"username",
				"password",])
			if not response.success: 
				self.website.metrics.count_auth_request(request, data={
					"url":self.url,
					"response":response,
				})
				return self.response(response)
			optional_parameters, _ = self.parameters.get(request, {
				"code":None,
			})

			# html
			html = ""
			if self._2fa:
				title = "Sign In - Verification Code"
				html = Files.load(f"{SOURCE_PATH}/classes/apps/authentication/mail/authentication.html")

			# make request.
			response = self.users.authenticate(
				username=parameters["username"],
				password=parameters["password"],
				_2fa_code=optional_parameters["code"],
				_2fa=self._2fa,
				html=html,
				request=request,)
			self.website.metrics.count_auth_request(request, data={
				"url":self.url,
				"response":response,
			})
			return self.response(response)
			
			#

	# sign out.
	class SignOut(views.Request):
		def __init__(self, defaults=None,):
			views.Request.__init__(self, "requests/authentication/", "signout", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# make request.
			return self.response(self.users.signout(
				request=request,))
			
			#

	# send reset password email.
	class SendCode(views.Request):
		def __init__(self, defaults=None,):
			views.Request.__init__(self, "requests/authentication/", "send_code", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# check 2fa rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="2fa", limit=15, reset_minutes=3600, increment=True)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = self.parameters.get(request, [
				"username",
				"mode",])
			if not response.success: return self.response(response)
			if parameters["username"] in ["undefined", "null", "None", "none", ""]:
				return self.error("Refresh the web page.")

			# make request.
			return self.response(self.send_code(
				username=parameters["username"],
				mode=parameters['mode'],
				request=request,))
			
			#

			#
		def send_code(self, username=None, mode=None, request=None):

			# check library.
			#if not Files.exists("templates/mail"): os.mkdir("templates/mail")
			#response = utils.__check_package_files__([
			#	["templates/mail/reset_password.html","w3bsite","/classes/requests/mail/reset_password.html"],
			#	["templates/mail/authentication.html","w3bsite","/classes/requests/mail/authentication.html"],
			#	["templates/mail/activation.html","w3bsite","/classes/requests/mail/activation.html"],
			#])
			#if not response.success: return response

			# set mode.
			code = Integer(0).generate(length=6)
			if mode == "reset_password":
				title = "Reset Password - Verification Code"
				path = f"{SOURCE_PATH}/classes/apps/authentication/mail/reset_password.html"
			elif mode == "authentication":
				title = "Sign In - Verification Code"
				path = f"{SOURCE_PATH}/classes/apps/authentication/mail/authentication.html"
			elif mode == "activation":
				title = "Account Activation - Verification Code"
				path = f"{SOURCE_PATH}/classes/apps/authentication/mail/activation.html"
			else:
				return dev0s.response.error("Selected an invalid mode.")

			# parse html.
			ip = utils.get_client_ip(request)
			html = Files.load(path)

			# make request.
			return self.users.send_code(
				username=username,
				mode=mode,
				ip=ip,
				code=code,
				html=html,
				title=title,)

	# reset password.
	class ResetPassword(views.Request):
		def __init__(self, defaults=None,):
			views.Request.__init__(self, "requests/authentication/", "reset_password", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = self.parameters.get(request, [
				"code",
				"email",
				"password",
				"verify_password",])
			if not response.success: return self.response(response)
			if parameters["email"] in ["undefined", "null", "None", "none", ""]:
				return self.error("Refresh the web page.")

			# make request.
			response = self.users.verify_code(
				email=parameters["email"],
				code=parameters["code"],
				mode="reset_password",)
			if not response.success: return self.response(response)

			# make request.
			response = self.users.update(
				email=parameters["email"], # for id.
				password=parameters["password"],
				verify_password=parameters["verify_password"],)
			if response.success: 
				response["message"] = f"Succesfully resetted the password of user [{user.email}]."
				_response_ = self.users.save_password(email=user.email, username=user.username, password=parameters["password"])
				if not _response_.success: return self.response(_response_)
			return self.response(response)
			
			#

	# activate account.
	class Activate(views.Request):
		def __init__(self, defaults=None,):
			views.Request.__init__(self, "requests/authentication/", "activate", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = self.parameters.get(request, [
				"code",
				"email",])
			if not response.success: return self.response(response)
			if parameters["email"] in ["undefined", "null", "None", "none", ""]:
				return self.error("Refresh the web page.")

			# make request.
			response = self.users.verify_code(
				email=parameters["email"],
				code=parameters["code"],
				mode="activation",)
			if not response.success: return self.response(response)

			# make request.
			response = self.users.update(
				email=parameters["email"],
				email_verified=True,)
			if response.success: response["message"] = f"Succesfully activated the account user [{user.email}]."
			return self.response(response)
			
			#

	# is authenticated.
	class Authenticated(views.Request):
		def __init__(self, defaults=None,):
			views.Request.__init__(self, "requests/authentication/", "authenticated", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# handler.
			try:
				email = request.user.email
			except AttributeError:
				email = None
			return self.success("Successfully checked if the user is authenticated.", {
				"authenticated":request.user.username != None and request.user.is_authenticated == True,
				"username":request.user.username,
				"email":email,
			})
			
			#

		#

	#

#