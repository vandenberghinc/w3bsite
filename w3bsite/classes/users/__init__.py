#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
if not syst3m.env.get("MIGRATIONS", format=bool, default=False):
	try:
		from django.contrib.auth.models import User as DjangoUser
		from django.contrib.auth import authenticate, login
		from django.contrib.auth import login as _login_
	except Exception as e:
		if syst3m.env.get_boolean("DJANGO_RUNNING") == True:
			raise ValueError(e)
try:
	from w3bsite.classes.firebase import *
	from firebase_admin import credentials, auth, firestore, _auth_utils
except ModuleNotFoundError: a=1
from w3bsite.classes import defaults as _defaults_
from w3bsite.classes import email

# the users class.
class Users(_defaults_.Defaults):
	def __init__(self,
		# noreply email settings.
		email_enabled=True,
		email_address=None, 
		email_password=None, 
		smtp_host="smtp.gmail.com", 
		smtp_port=587, 
		# objects.
		db=None,
		firestore=None, 
		stripe=None, 
		django=None,
		logging=None, 
		# defaults.
		defaults=None,
	):	

		# defaults.
		_defaults_.Defaults.__init__(self, traceback="w3bsite.Website.users",)
		self.assign(defaults.dict())

		# variables.
		self.email_enabled = email_enabled
		self.email_address = email_address
		self.email_password = email_password
		self.smtp_host = smtp_host 
		self.smtp_port = smtp_port 
		self.visible_email = None

		# objects.
		self.db = db
		self.firestore = firestore
		self.logging = logging
		self.stripe = stripe
		self.django = django

		# default user data.
		self.default_user_data = {
			"account": {
				"username":None,
				"email":None,
				"name":None,
				"password":None,
			},
			"keys": {
				"api_key":None,
			},
			# the requests.
			"requests": {
			},
			# the permissions.
			"permissions": {
				"email":True,
			},
			# timestamps.
			"timestamps": {
				"created":None,
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
		# optionals:
		verify_password=None,
		name=None,
		superuser=False,
	):

		# check parameters.
		response = r3sponse.check_parameters(
			traceback=self.__traceback__(function="create"),
			parameters={
				"username":username,
				"email":email,
				"password":password,
			})

		# check password.
		password = str(password)
		if len(password) < 8:
			return r3sponse.error("The password must contain at least 8 characters.")
		elif password.lower() == password:
			return r3sponse.error("The password must regular and capital letters.")
		elif verify_password != None and password != str(verify_password):
			return r3sponse.error("Passwords do not match.")

		# create django user.
		response = self.django.users.create(
			email=email,
			username=username,
			password=password,
			name=name,
			superuser=superuser,)
		if not response.success: return response
		user = response.user

		# try load existing data.
		response = self.load_data(email=email, username=username, create=True)
		if response.success and response.data != None:
			data = Dictionary(response.data).check(default=dict(self.default_user_data))
		else:
			data = dict(self.default_user_data)

		# save new user data.
		data["timestamps"]["created"] = Date().date
		data["keys"]["api_key"] = String().generate(length=48, capitalize=True, digits=True)
		_response_ = self.aes.encrypt(password)
		if not _response_.success: return _response_
		try:data["account"]
		except: data["account"] = {}
		data["account"]["username"] = username
		data["account"]["email"] = email
		data["account"]["name"] = name
		data["account"]["password"] = _response_["encrypted"].decode()
		response = self.save_data(email=email, username=username, data=data)
		if not response.success: return response

		# insert api key cache.
		try: self.__api_keys__
		except AttributeError: self.__api_keys__ = {}
		self.__api_keys__[data["keys"]["api_key"]] = {
			"email":email,
			"username":username
		}

		# handle success.
		return r3sponse.success(f"Successfully created user [{email}].", {
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
			if verify_password == None: return r3sponse.error("Specify parameter: verify_password.")
			password = str(password)
			verify_password = str(verify_password)
			if len(password) < 8:
				return r3sponse.error("The password must contain at least 8 characters.")
			elif password.lower() == password:
				return r3sponse.error("The password must regular and capital letters.")
			elif password != verify_password:
				return r3sponse.error("Passwords do not match.")
		
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
		response = self.load_data(email=email, username=username)
		if not response.success: return response
		data, edits = response.data, 0
		if email != None:
			edits += 1
			data["account"]["email"] = email
		if name != None:
			edits += 1
			data["account"]["name"] = name
		if edits > 0:
			response = self.save_data(email=email, username=username, data=data)
			if not response.success: return response

		# save pass.
		if password != None:
			response = self.save_password(email=user.email, username=username, password=password)
			if not response.success: return response

		# handle success.
		return r3sponse.success(f"Successfully updated user [{email}].")
		
		#
	def delete(self, 
		# the user's email.
		email=None,
		# the user's username.
		username=None,
	):
		
		# check parameters.
		if [username,email] == [None,None]:
			return r3sponse.error(self.__traceback__(function="load_data")+" Define one of the following parameters [email, username].")

		# delete django user.
		response = self.django.users.delete(username=username, email=email)
		if not response.success: return response

		# delete firestore data.
		response = self.db.delete(self.__get_path__(email=email, username=username))
		if not response.success: return response

		# handle success.
		return r3sponse.success(f"Successfully deleted user [{email}].")

		#
	def exists(self, 
		# one of the user id options is required.
		username=None,
		email=None,
		# the filter (django).
		filter="django",
	):
		if filter == "django":
			if email != None:
				return DjangoUser.objects.filter(email=email).exists()
			elif username != None:
				return DjangoUser.objects.filter(username=username).exists()
		else: 
			raise ValueError(f"Invalid filter [{filter}], valid options: [django].")
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
		response = r3sponse.check_parameters(
			traceback=self.__traceback__(function="authenticate"),
			parameters={
				"username":username,
				"password":password,
			})
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
				if not l_response.success: return l_response

				# handler for sign in.
				return r3sponse.error(f"Authentication verification code required.")

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
			return r3sponse.success(f"User {request.user.username} is authenticated.", {
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
		return r3sponse.error("User is not authenticated, please specify your api key or login.")

		#
	def root_permission(self, request):

		# by request user filled (django).
		if request.user != None and request.user.is_authenticated and request.user.is_superuser:
			return r3sponse.success(f"Root permission granted ({request.user.username}).", {
				"api_key":None,
				"email":request.user.email,
				"username":request.user.username,
			})

		# by api key.
		# never root permission.

		# error.
		return r3sponse.error("Root permission denied.")

		#
	def load_data(self,
		# the user's email.
		email=None,
		# the user's username.
		username=None,
		# the create boolean (do not use).
		create=False,
	):	
		if [username,email] == [None,None]:
			return r3sponse.error(self.__traceback__(function="load_data")+" Define one of the following parameters [email, username].")
		response = self.db.load(path=self.__get_path__(email=email, username=username, create=create))
		if response.error != None: return response
		return r3sponse.success(f"Successfully loaded the data of user [{email}].", {
			"data":response["data"],
		})
	def save_data(self,
		# the user's email.
		email=None,
		# the user's username.
		username=None,
		# the user's data.
		data={},
	):
		if [username,email] == [None,None]:
			return r3sponse.error(self.__traceback__(function="load_data")+" Define one of the following parameters [email, username].")
		print('saving data:',data)
		response = self.db.save(path=self.__get_path__(email=email, username=username, create=True), data=data)
		if response.error != None: return response
		return r3sponse.success(f"Successfully saved the data of user [{email}].")
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
		if syst3m.defaults.options.log_level >= 1:
			r3sponse.log(f"Sending email to user [{user.username}], email [{user.email}].")
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
		return r3sponse.success(f"Successfully send an email to user [{user.email}].")

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
			code = Integer(0).generate(length=6)
		response = self.get(email=email)
		if response.error != None: return response
		user = response["user"]
		try: self.verification_codes[mode]
		except: self.verification_codes[mode] = {}
		self.verification_codes[mode][user.email] = {
			"code":code,
			"stamp":Date().timestamp,
			"attempts":3,
		}
		
		# send email.
		if syst3m.defaults.options.log_level >= 1:
			r3sponse.log(f"Sending [{mode}] code to user [{user.username}], email [{user.email}].")
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
		return r3sponse.success(f"Successfully send a verification code to user [{user.email}].")

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
			return r3sponse.error("Incorrect verification code.")
		elif not success: 
			self.verification_codes[mode][user.email]["attempts"] -= 1
			return r3sponse.error("Incorrect verification code.")
		else:
			del self.verification_codes[mode][user.email]
			return r3sponse.success("Successfull verification.")

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
				#print(f"api_key [{api_key}] vs _api_key_ [{_api_key_}].")
				if _api_key_ == api_key: 
					return r3sponse.success(f"Successfully verified api key [{api_key}].", {
						"email":info["email"],
						"username":info["username"],
						"api_key":api_key,
					})

			# error.
			return r3sponse.error(f"Unable to verify api key [{api_key}].")

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
			return r3sponse.success(f"Successfully verified subscription {product} for user {id}.", {
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
			return r3sponse.error(f"Permission denied ({email}). This request requires at least one of the following plans for {product} [{_required_plans_}].")

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
		if email == None and api_key == None: return r3sponse.error("Define one of the following parameters: [email, api_key].")
		response = r3sponse.check_parameters(
			traceback=self.__traceback__(function="create_subscription"),
			parameters={
				"product":product,
				"plan":plan,
			})
		if not response.success: return response
		blinded = False
		if card_cvc == "***" and "************" in card_number:
			blinded = True
		if not blinded:
			response = r3sponse.check_parameters(
				traceback=self.__traceback__(function="create_subscription"),
				parameters={
					"card_name":card_name,
					"card_number":card_number,
					"card_expiration_month":card_expiration_month,
					"card_expiration_year":card_expiration_year,
					"card_cvc":card_cvc,
				})
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
			return r3sponse.error(f"User {email} is already subscribed to plan {plan} from product {product}.")

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
		return r3sponse.success(f"Successfully created subscription {product} {plan} for user {id}.")

		#
	def get_api_key(self, email=None, username=None):

		# check.
		if [username,email] == [None,None]:
			return r3sponse.error("Define one of the following parameters: [email, username].")
		if username == None: id = email
		elif email == None: id = username

		# collect api keys from cache.
		response = self.__collect_api_keys_cache__()
		if not response.success: return response
		api_keys = response["api_keys"]

		# get api key.
		for _api_key_, info in api_keys.items():
			if (email != None and email == info["email"]) or (username != None and username == info["username"]): 
				api_key = _api_key_
				break
		if api_key != None:
			return r3sponse.success(f"Successfully retrieved the api key [{id}].", {
				"api_key":api_key,
			})
		else:
			return r3sponse.error(f"Unable to find api key [{id}].")

		#
	def set_permission(self, email=None, username=None, permission_id=None, permission=True):
		
		# load user data.
		response = self.load_data(email=email, username=username) 
		if not response.success: return response
		data = response["data"]

		# edit data.
		data["permissions"][permission_id] = permission

		# save data.
		response = self.save_data(email=email, username=username, data=data) 
		if response.error != None: return response

		# handlers.
		return r3sponse.success(f"Successfully set the {permission_id} permission of user [{email}] to [{permission}].")
		#
	def load_password(self, email=None, username=None):
		if [username,email] == [None,None]:
			return r3sponse.error(self.__traceback__(function="load_data")+" Define one of the following parameters [email, username].")
		response = self.load_data(email=email, username=username)
		if not response.success: return response
		data = response.data
		_response_ = self.aes.decrypt(data["account"]["password"])
		if not _response_.success: return _response_
		password = _response_["decrypted"].decode()
		return r3sponse.success(f"Successfully retrieved the password of user {email}.",{
			"password":password,
			"data":data,
		})
	def save_password(self, email=None, username=None, password=None):
		if [username,email] == [None,None]:
			return r3sponse.error(self.__traceback__(function="load_data")+" Define one of the following parameters [email, username].")
		response = r3sponse.check_parameters(
			traceback=self.__traceback__(function="save_password"),
			parameters={
				"password":password,
			})
		if not response.success: return response
		response = self.load_data(email=email, username=username)
		if not response.success: return response
		data = response.data
		_response_ = self.aes.encrypt(password)
		if not _response_.success: _response_
		try:data["account"]
		except: data["account"] = {}
		data["account"]["password"] = _response_["encrypted"].decode()
		response = self.save_data(email=email, username=username, data=data)
		if not response.success: return response
		return r3sponse.success(f"Successfully saved the password of user {email}.")
	def iterate(self, 
		# iterating user objects (True) or email strings (False).
		users=True,
		# iterating the database (True) or django (False). 
		database=False,
	):
		if database:
			if self.db.mode == "firestore":
				response = self.firestore.load_collection(self.users_subpath)
				if not response.success: raise ValueError(response.error)
				_users_ = []
				_emails_ = response["collection"]
				if users:
					for email in _emails_:
						_users_.append(auth.get_user_by_email(email))
					return _users_
				else:
					return _emails_
			else:
				_users_ = []
				_emails_ = []
				for path in Directory(Files.join(self.database, self.users_subpath)).paths(dirs_only=True):
					id = gfp.name(path=path)
					info = self.load_data(username=id, email=id).data
					if info != None:
						_users_.append(info["account"]["username"])
						_emails_.append(info["account"]["email"])
				if users:
					return _users_
				else:
					return _emails_
		else:
			_users_, _emails_ = auth.list_users().iterate_all(), []
			if not users:
				for user in _users_:
					_emails_.append(user.email)
				return _emails_
			else:
				return _users_
	def synchronize(self, 
		# leave emails=None default to synchronize all users.
		# optionally pass emails=[newuser@email.com] to synchronize new users.
		ids=None, 
	):

		# get all emails.
		if not isinstance(ids, list):
			ids = self.iterate(users=False, database=True)

		# iterate.
		api_keys = {}
		for id in ids: 

			# get user.
			if self.id_by_username:
				username = id
				email = None
			else:
				username = None
				email = id

			# get.
			response = self.get(email=email, username=username)
			if not response.success: 
				response = self.load_password(email=email, username=username)
				if not response.success: return response
				data, password = response.unpack(["data", "password"])
				response = self.django.users.create(
					email=data["account"]["email"], 
					password=password, 
					username=data["account"]["username"], 
					name=data["account"]["name"])
				if not response.success: return response
			user = response["user"]

			# load data.
			response = self.load_data(email=user.email, username=user.username)
			if not response.success: return response
			data, edits = response["data"], 0

			# check user data.
			d = Dictionary(dictionary=data, path=False)
			old = dict(data)
			data = d.check(default=dict(self.default_user_data))
			if Dictionary(old) != Dictionary(data):
				edits += 1

			# check user data.
			try:
				if data["keys"]["api_key"] in [None, ""]: raise KeyError("")
			except KeyError: 
				data["keys"]["api_key"] = String().generate(length=48, capitalize=True, digits=True)
				edits += 1

			# edits.
			if edits > 0:
				response = self.save_data(email=user.email, username=user.username, data=data)
				if not response.success: return response

			# api keys.
			api_keys[data["keys"]["api_key"]] = {
				"username":user.username,
				"email":user.email,
			}

		# success.
		return r3sponse.success(f"Successfully synchronized {len(ids)} user(s).", {
			"api_keys":api_keys,
		})

		#
	# system functions.
	def __initialize_email__(self):
		# the email object.
		if not self.email_enabled:
			return r3sponse.error("The email object is disabled.")
		if self.email_address == None or self.email_password == None:
			return r3sponse.error("Define the firebase.users.email_address & firebase.users.email_password variables to send emails.")
		self.email = email.Email(
			email=self.email_address,
			password=self.email_password,
			smtp_host=self.smtp_host,
			smtp_port=self.smtp_port,
			visible_email=self.visible_email,)
		response = self.email.login()
		if response["success"]:
			return r3sponse.success("Successfully initialized the mail object.")
		else: 
			self.email = None
			return response
	def __collect_subscriptions_cache__(self, refresh=False):

		# get cache.
		subscriptions, cache_subscriptions = {}, False
		try:
			subscriptions = dict(self.__subscriptions__)
		except AttributeError:
			self.__subscriptions__ = {}
			cache_subscriptions = True

		# collect cache.
		if refresh or cache_subscriptions:
			response = self.stripe.subscriptions.get(active_only=True, by_customer_id=False)
			if not response.success: return response
			subscriptions = response["subscriptions"]

		# set cache.
		if refresh or cache_subscriptions:
			self.__subscriptions__ = dict(subscriptions)

		# handler.
		return r3sponse.success("Successfully retrieved the stripe subscriptions cache.", {
			"subscriptions":subscriptions,
		})

		#
	def __collect_api_keys_cache__(self, refresh=False):
		
		# get cache.
		api_keys, cache_api_keys = {}, False
		try:
			api_keys = dict(self.__api_keys__)
		except AttributeError:
			self.__api_keys__ = {}
			cache_api_keys = True

		# collect cache.
		if cache_api_keys or refresh:
			response = self.synchronize()
			if not response.success: return response
			api_keys = response["api_keys"]

		# set cache.
		if cache_api_keys or refresh:
			self.__api_keys__ = dict(api_keys)

		# handler.
		return r3sponse.success("Successfully retrieved the api keys cache.", {
			"api_keys":api_keys,
		})

		#
	def __get_path__(self, email=None, username=None, create=False):
		if self.id_by_username:
			if username == None and email != None:
				response = self.get(email=email)
				if not response.success: response.crash()
				username = response.user.username
			id = username
			if "@" in username:
				raise ValueError(f"Forbidden @ character found in username: [{username}].")
		else:
			if email == None and username != None:
				response = self.get(username=username)
				if not response.success: response.crash()
				email = response.user.email
			id = email
			if "@" not in email:
				raise ValueError(f"Required @ character not found in email: [{email}].")
		if self.db.mode == "cache":
			path = f"{self.users_subpath}/{id}/settings"
			if create and not Files.exists(gfp.base(path)): Files.create(gfp.base(path), directory=True)
		else:
			path = f"{self.users_subpath}/{id}"
		return path
	def __username_to_email__(self, username):
		try:
			return self.get(username=username).email
		except Exception as e:
			raise ValueError(f"Unable retrieve the email of username [{username}], error: {e}.")
	def __email_to_username__(self, email):
		try:
			return self.get(email=email).username
		except Exception as e:
			raise ValueError(f"Unable retrieve the username of email [{email}], error: {e}.")