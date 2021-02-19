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
		send_code = self.SendCode(defaults=defaults)
		self.urls = views.build_urls([
			self.SignUp(defaults=defaults, send_code=send_code),
			self.SignIn(defaults=defaults),
			send_code,
			self.ResetPassword(defaults=defaults),
			self.Activate(defaults=defaults),
		])

	# sign up.
	class SignUp(views.Request):
		def __init__(self, defaults=None, send_code=None):
			self.assign(defaults.dict())
			views.Request.__init__(self, "requests/authentication/", "signup")
			self.send_code = send_code
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
			_response_ = self.send_code.send_code(email=parameters["email"], mode="activation", request=request)
			if not r3sponse.success(_response_): return self.response(_response_)

			# return create response.
			if response.success:
				del response["user"]
			return self.response(response)

	# sign in.
	class SignIn(views.Request):
		def __init__(self, defaults=None,):
			self.assign(defaults.dict())
			views.Request.__init__(self, "requests/authentication/", "signin")
		def view(self, request):

			# permission denied.
			#return self.permission_denied()

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# check signup rate limit.
			#response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="signin", limit=5, reset_minutes=10, increment=True)
			#if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = r3sponse.get_request_parameters(request, [
				"username",
				"password",])
			if not response.success: return self.response(response)
			optional_parameters, _ = r3sponse.get_request_parameters(request, [
				"code",], optional=True)
			# make request.
			return self.response(self.users.authenticate(
				username=parameters["username"],
				password=parameters["password"],
				_2fa_code=optional_parameters["code"],
				_2fa=self._2fa,
				request=request,))

	# send reset password email.
	class SendCode(views.Request):
		def __init__(self, defaults=None,):
			self.assign(defaults.dict())
			views.Request.__init__(self, "requests/authentication/", "send_code", )
		def view(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# check 2fa rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="2fa", limit=15, reset_minutes=3600, increment=True)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = r3sponse.get_request_parameters(request, [
				"email",
				"mode",])
			if not response.success: return self.response(response)
			if parameters["email"] in ["undefined", "null", "None", "none", ""]:
				return self.error_response("Refresh the web page.")

			# make request.
			return self.response(self.send_code(
				email=parameters["email"],
				mode=parameters['mode'],
				request=request,))

			#
		def send_code(self, email=None, mode=None, request=None):

			# check library.
			#if not os.path.exists("templates/mail"): os.mkdir("templates/mail")
			#response = utils.__check_package_files__([
			#	["templates/mail/reset_password.html","w3bsite","/classes/requests/mail/reset_password.html"],
			#	["templates/mail/authentication.html","w3bsite","/classes/requests/mail/authentication.html"],
			#	["templates/mail/activation.html","w3bsite","/classes/requests/mail/activation.html"],
			#])
			#if not response.success: return response

			# set mode.
			code = Formats.Integer(0).generate(length=6)
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
				return r3sponse.error_response("Selected an invalid mode.")

			# parse html.
			ip = utils.__get_client_ip__(request)
			html = Files.File(path, load=True).data.format(
				# domain info.
				domain=self.https_domain,
				# code.
				code=code,
				# request info.
				ip=ip,
				timestamp=Formats.Date().seconds_timestamp,
				# user info.
				email=email,
				# colors.
				white=self.template_data["COLORS"]["white"],
				grey=self.template_data["COLORS"]["grey"],
				blue=self.template_data["COLORS"]["blue"],
				purple=self.template_data["COLORS"]["purple"],
				red=self.template_data["COLORS"]["red"],
				pink=self.template_data["COLORS"]["pink"],
				orange=self.template_data["COLORS"]["orange"],
				green=self.template_data["COLORS"]["green"],
				darkest=self.template_data["COLORS"]["darkest"],
				darker=self.template_data["COLORS"]["darker"],
				dark=self.template_data["COLORS"]["dark"],
				background=self.template_data["COLORS"]["background"],
				widgets=self.template_data["COLORS"]["widgets"],
				widgets_reversed=self.template_data["COLORS"]["widgets_reversed"],
				text=self.template_data["COLORS"]["text"],
				text_reversed=self.template_data["COLORS"]["text_reversed"],
				)

			# make request.
			return self.users.send_code(
				email=email,
				mode=mode,
				ip=ip,
				code=code,
				html=html,
				title=title,)

	# reset password.
	class ResetPassword(views.Request):
		def __init__(self, defaults=None,):
			self.assign(defaults.dict())
			views.Request.__init__(self, "requests/authentication/", "reset_password",)
		def view(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = r3sponse.get_request_parameters(request, [
				"code",
				"email",
				"password",
				"verify_password",])
			if not response.success: return self.response(response)
			if parameters["email"] in ["undefined", "null", "None", "none", ""]:
				return self.error_response("Refresh the web page.")

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
				_response_ = self.users.save_password(email=user.email, password=parameters["password"])
				if not r3sponse.success(_response_): return self.response(_response_)
			return self.response(response)

	# activate account.
	class Activate(views.Request):
		def __init__(self, defaults=None,):
			self.assign(defaults.dict())
			views.Request.__init__(self, "requests/authentication/", "activate")
		def view(self, request):

			# check overall rate limit.
			response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
			if not response.success: return self.response(response)

			# retrieve params.
			parameters, response = r3sponse.get_request_parameters(request, [
				"code",
				"email",])
			if not response.success: return self.response(response)
			if parameters["email"] in ["undefined", "null", "None", "none", ""]:
				return self.error_response("Refresh the web page.")

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