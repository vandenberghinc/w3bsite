#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.firebase import *
from firebase_admin import credentials, auth, firestore, _auth_utils
from w3bsite.classes import defaults as _defaults_

# the users class.
class Users(_defaults_.Defaults):
	def __init__(self,
		# noreply email settings.
		email_address=None, 
		email_password=None, 
		smtp_host="smtp.gmail.com", 
		smtp_port=587, 
		# objects.
		firestore=None, 
		stripe=None, 
		django=None,
		logging=None, 
		# defaults.
		defaults=None,
	):	

		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# check arguments.
		#response = r3sponse.check_parameters({
		#	#"ip":ip,
		#})
		#if not response.success: raise ValueError(response.error)

		# variables.
		self.email_address = email_address
		self.email_password = email_password
		self.smtp_host = smtp_host 
		self.smtp_port = smtp_port 
		self.visible_email = None

		# objects.
		self.firestore = firestore
		self.logging = logging
		self.stripe = stripe
		self.django = django

		# settings for saving user data.
		self.users_collection = "users/"

		# default user data.
		self.default_user_data = {
			# default data.
			"api_key":None,
			# the requests.
			"requests": {},
			# the permissions.
			"permissions": {
				"email":True,
			},
			# timestamps.
			"timestamps": {
				"signed_up":None,
			},
		}

		#
	def get(self, 
		# define one of the following user id parameters.
		username=None,
		email=None,
	):
		return self.django.users.get(username=username, email=email)
	def create(self,
		# required:
		username=None,
		email=None,
		password=None,
		verify_password=None,
		# optionals:
		name=None,
		superuser=False,
		#phone_number=None,
		#photo_url=None,
		#email_verified=False,
	):

		# check parameters.
		response = r3sponse.check_parameters(empty_value=None, parameters={
			"username":username,
			"email":email,
			"password":password,
			"verify_password":verify_password,
		})

		# check password.
		password = str(password)
		verify_password = str(verify_password)
		if len(password) < 8:
			return r3sponse.error_response("The password must contain at least 8 characters.")
		elif password.lower() == password:
			return r3sponse.error_response("The password must regular and capital letters.")
		elif password != verify_password:
			return r3sponse.error_response("Passwords do not match.")

		# create firebase user ! must be first !
		"""
		response = self.firebase.users.create(
			email=email,
			phone_number=phone_number,
			password=password,
			display_name=name,
			photo_url=photo_url,
			email_verified=email_verified,)
		if not response.success: return response
		"""

		# create django user.
		response = self.django.users.create(
			email=email,
			username=username,
			password=password,
			name=name,
			superuser=superuser,)
		if not response.success: return response
		user = response.user

		# save new user data.
		data = dict(self.default_user_data)
		data["timestamps"]["signed_up"] = Formats.Date().date
		data["api_key"] = Formats.String("").generate(length=68, capitalize=True, digits=True)
		_response_ = self.aes.encrypt(password)
		if not r3sponse.success(_response_): return self.response(_response_)
		try:data["account"]
		except: data["account"] = {}
		data["account"]["username"] = username
		data["account"]["email"] = email
		data["account"]["name"] = name
		data["account"]["password"] = _response_["encrypted"].decode()
		response = self.save_data(email, data)
		if not response.success: return response

		# insert api key cache.
		if "api_keys" in list(self.cache.__cache__.keys()):
			self.cache.__cache__["api_keys"]["value"][data["api_key"]] = {
				"email":email,
			}

		# handle success.
		return r3sponse.success_response(f"Successfully created user [{email}].", {
			"user":user,
			"email":user.email,
			"data":data,
		})

		#
	def update(self,
		# required:
		email=None,
		# optionals:
		name=None,
		password=None,
		verify_password=None,
		superuser=None,
		#phone_number=None,
		#photo_url=None,
		#email_verified=None,
	):

		# load.
		response = self.get(email=email)
		if response.error != None: return response
		user = response["user"]

		# check password.
		if password != None:
			if verify_password == None: return r3sponse.error_response("Specify parameter: verify_password.")
			password = str(password)
			verify_password = str(verify_password)
			if len(password) < 8:
				return r3sponse.error_response("The password must contain at least 8 characters.")
			elif password.lower() == password:
				return r3sponse.error_response("The password must regular and capital letters.")
			elif password != verify_password:
				return r3sponse.error_response("Passwords do not match.")
		
		# create firebase user ! must be first !
		"""
		response = self.firebase.users.update(
			email=email,
			phone_number=phone_number,
			password=password,
			display_name=name,
			photo_url=photo_url,
			email_verified=email_verified,)
		if not response.success: return response
		"""

		# create django user.
		response = self.django.users.update(
			email=email,
			username=username,
			password=password,
			name=name,
			superuser=superuser,)
		if not response.success: return response
		user = response.user

		# update firestore.
		response = self.load_data(email=email)
		if not response.success: return response
		data, edits = response.data, 0
		if email != None:
			edits += 1
			data["account"]["email"] = email
		if name != None:
			edits += 1
			data["account"]["name"] = name
		if edits > 0:
			response = self.save_data(email=email, data=data)
			if not response.success: return response

		# save pass.
		if password != None:
			response = self.save_password(email=user.email, password=password)
			if not response.success: return response

		# handle success.
		return r3sponse.success_response(f"Successfully updated user [{email}].")
		
		#
	def delete(self, 
		# the user's email.
		email=None,
	):
		
		# check parameters.
		response = r3sponse.check_parameters({
			"email":email,})
		if not response.success: return response

		# delete firebase user ! must be first !
		#response = self.firebase.users.delete(email=email,)
		#if not response.success: return response

		# delete django user.
		response = self.django.users.delete(email=email,)
		if not response.success: return response

		# delete firestore data.
		response = self.firestore.delete(f"{self.users_collection}/{email}/")
		if not response.success: return response

		# handle success.
		return r3sponse.success_response(f"Successfully deleted user [{email}].")

		#
	def authenticate(self,
		# the users username.
		username=None,
		# the users password.
		password=None,
		# the 2fa code.
		_2fa_code=None,
		# the 2fa enabled boolean.
		# leave None to use the self._2fa settings and specify to overwrite.
		_2fa=None,
		# the request object.
		request=None,
	):

		# check parameters.
		response = r3sponse.check_parameters({
			"username":username,
			"password":password,})
		if not response.success: return response

		# check first.
		response = self.django.users.authenticate(username=username, password=password, login=not _2fa, request=request)
		if not response.success: return response
		
		# check 2fa.		
		if _2fa == None: _2fa = self._2fa
		if _2fa == True:
			if _2fa_code == None: 

				# send code.
				l_response = self.send_verification_code(username, ip=ip, mode="authentication")
				if not r3sponse.success(l_response): return l_response

				# handler for sign in.
				return r3sponse.error_response(f"Authentication verification code required.")

			# verify code.
			response = self.verify_verification_code(username, code=_2fa_code, mode="authentication")
			if not response.success: return response

		# no 2fa.
		else:
			return response

		# success.
		return self.django.users.authenticate(username=username, password=password, request=request)

		#
	def authenticated(self, request):

		# by request user filled (django).
		if request.user.is_authenticated:
			return r3sponse.success_response(f"User {request.user.username} is authenticated.", {
				"api_key":None,
				"email":request.user.email,
				"username":request.user.username,
			})

		# by api key.
		optional_parameters, response = r3sponse.get_request_parameters(request, [
			"api_key",
			#"id_token",
			], optional=True)
		if optional_parameters["api_key"] != None:
			return self.verify_api_key(api_key=optional_parameters["api_key"])

		# error.
		return r3sponse.error_response("User is not authenticated, please specify your api key or login.")

		#
	def load_data(self,
		# the user's email.
		email=None,
	):	
		# new.
		response = r3sponse.check_parameters({
			"email":email,})
		if not response.success: return response
		response = self.firestore.load(f"{self.users_collection}/{email}/")
		if response.error != None: return response
		return r3sponse.success_response(f"Successfully loaded the data of user [{email}].", {
			"data":response["document"],
		})
	def save_data(self,
		# the user's email.
		email=None,
		# the user's data.
		data={},
	):
		# new.
		response = r3sponse.check_parameters({
			"email":email,})
		if not response.success: return response
		response = self.firestore.save(f"{self.users_collection}/{email}/", data)
		if response.error != None: return response
		return r3sponse.success_response(f"Successfully saved the data of user [{email}].")
	def send_email(self, 
		# define email to retrieve user.
		email=None, 
		# the email title.
		title="Account Activation",
		# the html (str).
		html="",
	):

		# check email.
		try:
			if self.email == None:
				raise AttributeError("")
		except AttributeError:
			response = self.__initialize_email__()
			if response.error != None: return response
				
		# get user.
		response = self.get(email=email)  
		if response.error != None: return response
		user = response["user"]
		
		# send email.
		response = self.email.send(
			subject=title,
			recipients=[user.email], 
			html=html)
		if response.error != None:
			response = self.__initialize_email__()
			if response.error != None: return response
			response = self.email.send(
				subject=title,
				recipients=[user.email], 
				html=html)
			if response.error != None: return response

		# success.
		return r3sponse.success_response(f"Successfully send an email to user [{user.email}].")

		#
	def send_code(self, 
		# define email to retrieve user.
		email=None, 
		# the clients ip.
		ip="unknown",
		# the mode id.
		mode="verification",
		# the mode title.
		title="Account Activation",
		# the html (str).
		html="",
		# optionally specify the code (leave None to generate).
		code=None,
	):

		# check email.
		try:
			if self.email == None:
				raise AttributeError("")
		except AttributeError:
			response = self.__initialize_email__()
			if response.error != None: return response
				
		# save code.
		if code == None:
			code = Formats.Integer(0).generate(length=6)
		response = self.get(email=email)
		if response.error != None: return response
		user = response["user"]
		try: self.verification_codes[mode]
		except: self.verification_codes[mode] = {}
		self.verification_codes[mode][user.email] = {
			"code":code,
			"stamp":Formats.Date().timestamp,
			"attempts":3,
		}
		
		# send email.
		response = self.email.send(
			subject=f'{title} - Verification Code',
			recipients=[user.email], 
			html=html)
		if response.error != None:
			response = self.__initialize_email__()
			if response.error != None: return response
			response = self.email.send(
				subject=f'{title} - Verification Code',
				recipients=[user.email], 
				html=html)
			if response.error != None: return response

		# success.
		return r3sponse.success_response(f"Successfully send a verification code to user [{user.email}].")

		#
	def verify_code(self, 
		# define email to retrieve user.
		email=None, 
		# the user entered code.
		code=000000, 
		# the message mode.
		mode="verification",
	):


		# get user.
		response = self.get(email=email)
		if response.error != None: return response
		user = response["user"]

		# get success.
		fail = False
		try: self.verification_codes[mode]
		except: self.verification_codes[mode] = {}
		try: success = self.verification_codes[mode][user.email]["attempts"] > 0 and str(self.verification_codes[mode][user.email]["code"]) == str(code)
		except KeyError: fail = True

		# handle.
		if fail: 
			return r3sponse.error_response("Incorrect verification code.")
		elif not success: 
			self.verification_codes[mode][user.email]["attempts"] -= 1
			return r3sponse.error_response("Incorrect verification code.")
		else:
			del self.verification_codes[mode][user.email]
			return r3sponse.success_response("Successfull verification.")

		#
	def verify_api_key(self, api_key=None, request=None):
		
		# by request.
		if request != None:
			parameters, response = r3sponse.get_request_parameters(request, ["api_key"])
			if not response.success: return response
			return self.verify_api_key(api_key=parameters["api_key"])
		
		# by api key.
		else:
			
			# collect api keys from cache.
			response = self.__collect_api_keys_cache__()
			if not response.success: return response
			api_keys = response["api_keys"]

			# check api key.
			for _api_key_, info in api_keys.items():
				if _api_key_ == api_key: 
					return r3sponse.success_response(f"Successfully verified api key [{api_key}].", {
						"email":info["email"],
						"api_key":api_key,
					})

			# error.
			return r3sponse.error_response(f"Unable to verify api key [{api_key}].")

			#
	def verify_subscription(self,
		# select one of the following user id options:
		email=None,
		api_key=None,
		# the subscription product.
		product=None,
		# the subscription plans that will return a success verification (["*"] for all plans within the product).
		plans=[],
	):

		# set user id.
		if email != None:
			id = email
		elif api_key != None:
			response = self.verify_api_key(api_key=api_key)
			if not response.success: return response
			id = response["email"]
			email = response["email"]

		# collect stripe subscriptions cache.
		response = self.__collect_subscriptions_cache__()
		if not response.success: return response
		subscriptions = response["subscriptions"]

		# create user subscriptions.
		user_subscriptions = {}
		for _product_, _plans_ in self.stripe._subscriptions_.items():
			response = self.stripe.get_product_id(product=_product_)
			if not response.success: return response
			product_id = response["id"]
			user_subscriptions[_product_] = {}
			for plan_name, plan_info in _plans_.items():
				response = self.stripe.get_plan_id(product=_product_, plan=plan_name)
				if not response.success: return response
				plan_id = response["id"]
				active = False
				try: _subscriptions_ = subscriptions[email]
				except: _subscriptions_ = {}
				for _plan_id_, info in _subscriptions_.items():
					if _plan_id_ == plan_id and info["active"]:
						active = True
						break
				user_subscriptions[_product_][plan_name] = active

		# check user subscriptions.
		required_plans = list(plans)
		verified = False
		for allowed_plan in plans:
			if allowed_plan == "*":
				required_plans = list(user_subscriptions[product].keys())
				for _, allowed in user_subscriptions[product].items():
					if allowed:
						verified = True
						break
				break
			else:
				if user_subscriptions[product][allowed_plan] == True:
					verified = True
					break

		# handlers.
		if verified:
			return r3sponse.success_response(f"Successfully verified subscription {product} for user {id}.", {
				"email":email,
				"api_key":api_key,
				"product":product,
				"plans":required_plans,
			})
		else:
			_required_plans_ = ""
			for i in required_plans: 
				if _required_plans_ == "": _required_plans_ = i
				else: _required_plans_ += ", "+i
			return r3sponse.error_response(f"Permission denied ({email}). This request requires at least one of the following plans for {product} [{_required_plans_}].")

		#
	def create_subscription(self,
		# select one of the following user id options:
		email=None,
		api_key=None,
		# the subscription product.
		product=None,
		# the subscription plan.
		plan=None,
		# the card holders name.
		card_name=None,
		# the card number.
		card_number=None,
		# the card expiration month.
		card_expiration_month=None,
		# the card expiration year.
		card_expiration_year=None,
		# the card cvc.
		card_cvc=None,
	):

		# checkparameters.
		if email == None and api_key == None: return r3sponse.error_response("Define one of the following parameters: [email, api_key].")
		response = r3sponse.check_parameters({
			"product":product,
			"plan":plan,})
		if not response.success: return response
		blinded = False
		if card_cvc == "***" and "************" in card_number:
			blinded = True
		if not blinded:
			response = r3sponse.check_parameters({
				"card_name":card_name,
				"card_number":card_number,
				"card_expiration_month":card_expiration_month,
				"card_expiration_year":card_expiration_year,
				"card_cvc":card_cvc,})
			if not response.success: return response
		

		# set user id.
		if email != None:
			id = email
		elif api_key != None:
			response = self.verify_api_key(api_key=api_key)
			if not response.success: return response
			id = response.email

		# get plan id.
		response = self.stripe.get_product_id(product=product)
		if not response.success: return response
		product_id = response.id
		response = self.stripe.get_plan_id(product=product, plan=plan)
		if not response.success: return response
		plan_id = response.id

		# check / create customer.
		response = self.stripe.customers.check(email=id)
		if not response.success: return response
		elif not response.exists:
			response = self.stripe.customers.create(email=id)
			if not response.success: return response
			customer_id = response.id
		else:
			customer_id = response.id

		# map user's stripe subscriptions.
		plan_ids, sub_ids, active_product_subs = [], {}, {}
		response = self.stripe.subscriptions.get(email=email)
		if not response.success and "No subscriptions found for user" not in response.error: return response
		elif not response.success and "No subscriptions found for user" in response.error:
			plan_ids, sub_ids, active_product_subs = [], {}, {}
		else:
			plan_ids, sub_ids, active_product_subs = [], {}, {}
			for _plan_id_,info in response.subscriptions.items():
				response = self.stripe.get_product_id_by_plan_id(_plan_id_)
				if not response.success: return response
				_product_id_ = response.id
				if _product_id_ == product_id:
					active_product_subs[info["plan_id"]] = info["subscription_id"]	
				plan_ids.append(info["plan_id"])
				sub_ids[info["plan_id"]] = info["subscription_id"]

		# check already subscribed.
		if plan_id in plan_ids:
			return r3sponse.error_response(f"User {email} is already subscribed to plan {plan} from product {product}.")

		# create card when card is not blinded (aka retrieved from user).
		if not blinded:
			response = self.stripe.customers.create_card(
				id=customer_id,
				name=card_name,
				number=card_number,
				month=card_expiration_month,
				year=card_expiration_year,
				cvc=card_cvc,)
			if not response.success: return response

		# cancel all plans within the product.	
		for _plan_id_, _subscription_id_ in active_product_subs.items():
			response = self.stripe.subscriptions.cancel(subscription_id=_subscription_id_)
			if not response.success: return response		

		# create subscription.
		response = self.stripe.subscriptions.create(customer_id=customer_id, plans=[plan_id])
		if not response.success: return response
		
		# handlers.
		return r3sponse.success_response(f"Successfully created subscription {product} {plan} for user {id}.")

		#
	def get_api_key(self, email=None, username=None):

		# collect api keys from cache.
		response = self.__collect_api_keys_cache__()
		if not response.success: return response
		api_keys = response["api_keys"]

		# get api key.
		api_key, id = None, None
		if email != None: id = email
		elif username != None: 
			response = self.get(username=username)
			if not response.success: return response
			id = response["user"].email
		else: return r3sponse.error_response("Define parameter email or username.")
		for _api_key_, info in api_keys.items():
			if info["email"] == id: 
				api_key = _api_key_
				break
		if api_key != None:
			return r3sponse.success_response(f"Successfully retrieved the api key [{id}].", {
				"api_key":api_key,
			})
		else:
			return r3sponse.error_response(f"Unable to find api key [{id}].")

		#
	def set_permission(self, email, permission_id, permission=True):
		
		# load user data.
		response = self.load_data(email=email) 
		if not response.success: return response
		data = response["data"]

		# edit data.
		data["permissions"][permission_id] = permission

		# save data.
		response = self.save_data(email=email, data=data) 
		if response.error != None: return response

		# handlers.
		return r3sponse.success_response(f"Successfully set the {permission_id} permission of user [{email}] to [{permission}].")
		#
	def load_password(self, email=None):
		response = r3sponse.check_parameters({
			"email":email,})
		if not response.success: return response
		response = self.load_data(email)
		if not response.success: return response
		data = response.data
		_response_ = self.aes.decrypt(data["account"]["password"])
		if not r3sponse.success(_response_): return self.response(_response_)
		password = _response_["decrypted"].decode()
		return r3sponse.success_response(f"Successfully retrieved the password of user {email}.",{
			"password":password,
			"data":data,
		})
	def save_password(self, email=None, password=None):
		response = r3sponse.check_parameters({
			"email":email,
			"password":password,})
		if not response.success: return response
		response = self.load_data(email)
		if not response.success: return response
		data = response.data
		_response_ = self.aes.encrypt(password)
		if not r3sponse.success(_response_): return self.response(_response_)
		try:data["account"]
		except: data["account"] = {}
		data["account"]["password"] = _response_["encrypted"].decode()
		response = self.save_data(email, data)
		if not response.success: return response
		return r3sponse.success_response(f"Successfully saved the password of user {email}.")
	def iterate(self, emails=False, firestore=False, combined=False):
		if combined:
			firestore = self.iterate(emails=emails, firestore=True)
			django = self.iterate(emails=emails, firestore=False)
			return firestore + django
		else:
			if firestore:
				response = self.firestore.load_collection("users/")
				if not response.success: raise ValueError(response.error)
				users = []
				_emails_ = response["collection"]
				if not emails:
					for email in _emails_:
						users.append(auth.get_user_by_email(email))
					return users
				else:
					return _emails_
			else:
				users, _emails_ = auth.list_users().iterate_all(), []
				if emails:
					for user in users:
						_emails_.append(user.email)
					return _emails_
				else:
					return users
	def synchronize(self, 
		# leave emails=None default to synchronize all users.
		# optionally pass emails=[newuser@email.com] to synchronize new users.
		emails=None, 
	):

		# get all emails.
		if not isinstance(emails, list):
			emails = self.iterate(emails=True, firestore=True)

		# iterate.
		for email in emails: 

			# check django user existance (in case of sql rebuild).
			response = self.django.users.exists(email=email)
			if not response.success: return response
			elif not response.exists:
				response = self.load_password(email=email)
				if not response.success: return response
				data, password = response.data, response.password
				response = self.django.users.create(
					email=email, 
					password=password, 
					username=data["account"]["username"], 
					name=data["account"]["name"])
				if not response.success: return response

			# get user.
			response = self.get(email=email)
			if not response.success: return response
			user = response["user"]

			# load data.
			response = self.load_data(email=email)
			if not response.success: return response
			data, edits = response["data"], 0

			# check user data.
			d = Files.Dictionary(dictionary=data, path=False)
			old = dict(data)
			data = d.check(default=self.default_user_data)
			if old != data:
				edits += 1

			# check user data.
			try:
				if data["api_key"] in [None, ""]: raise KeyError("")
			except KeyError: 
				data["api_key"] = Formats.String("").generate(length=68, capitalize=True, digits=True)
				edits += 1

			# edits.
			if edits > 0:
				response = self.save_data(email=email, data=data)
				if not response.success: return response

		# success.
		return r3sponse.success_response(f"Successfully synchronized {len(emails)} user(s).")

		#
	# system functions.
	def __initialize_email__(self):
		# the email object.
		if self.email_address == None or self.email_password == None:
			return r3sponse.error_response("Define the firebase.users.email_address & firebase.users.email_password variables to send emails.")
		self.email = utils.Email(
			email=self.email_address,
			password=self.email_password,
			smtp_host=self.smtp_host,
			smtp_port=self.smtp_port,
			visible_email=self.visible_email,)
		response = self.email.login()
		if response["success"]:
			return r3sponse.success_response("Successfully initialized the mail object.")
		else: 
			self.email = None
			return response
	def __collect_subscriptions_cache__(self, refresh=False):

		# get cache.
		subscriptions, cache_subscriptions = {}, False
		response = self.cache.get(key="subscriptions")
		if not response.success: 
			cache_subscriptions = True
		else:
			subscriptions = response["value"]

		# collect cache.
		if refresh or cache_subscriptions:
			response = self.stripe.subscriptions.get(active_only=True, by_customer_id=False)
			if not response.success: return response
			subscriptions = response["subscriptions"]

		# set cache.
		if refresh or cache_subscriptions:
			response = self.cache.set(key="subscriptions", value=subscriptions, reset=60)
			if not response.success: return response

		# handler.
		return r3sponse.success_response("Successfully retrieved the stripe subscriptions cache.", {
			"subscriptions":subscriptions,
		})

		#
	def __collect_api_keys_cache__(self, refresh=False):
		
		# get cache.
		api_keys, cache_api_keys = {}, False
		response = self.cache.get(key="api_keys")
		if not response.success: 
			cache_api_keys = True
		else:
			api_keys = response["value"]

		# collect cache.
		if cache_api_keys or refresh:
			api_keys = {}
			for email in self.iterate(emails=True, combined=True):
				response = self.load_data(email=email)
				if not response.success: return response
				_api_key_ = response["data"]["api_key"]
				api_keys[_api_key_] = {
					"email":email,
				}

		# set cache.
		if cache_api_keys or refresh:
			response = self.cache.set(key="api_keys", value=api_keys, reset=60*24)
			if not response.success: return response

		# handler.
		return r3sponse.success_response("Successfully retrieved the api keys cache.", {
			"api_keys":api_keys,
		})

		#

	