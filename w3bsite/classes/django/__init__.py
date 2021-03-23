#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes.utils import utils
from w3bsite.classes import defaults as _defaults_
if not dev0s.env.get("MIGRATIONS", format=bool, default=False):
	try:
		from django.contrib.auth.models import User as DjangoUser
		from django.contrib.auth import authenticate, login
		from django.contrib.auth import login as _login_
	except Exception as e:
		if dev0s.env.get_boolean("DJANGO_RUNNING") == True:
			raise ValueError(e)

# the django object class.
class Django(_defaults_.Defaults):
	def __init__(self, 
		# the security object.
		security=None,
		# defaults.
		defaults=None,
	):


		# docs.
		DOCS = {
			"module":"website.django", 
			"initialized":True,
			"description":[], 
			"chapter": "Django", }

		# defaults.
		_defaults_.Defaults.__init__(self, traceback="w3bsite.Website.django",)
		self.assign(defaults.dict())

		# arguments.
		# ...

		# objects.
		self.security = security
		self.users = Users(defaults=defaults)

		#
	def start(self, host="127.0.0.1", port="8000", production=False):

		# check secret key.
		os.chdir(self.root)
		try:
			add_secret_key = Files.load("__defaults__/env/json", format="json")["DJANGO_SECRET_KEY"] in ["False","True","None","","null",None,False,True]
		except:
			add_secret_key = True
		
		# import main.
		dev0s.env.export(export=["__defaults__/env/json"], env={
			"PRODUCTION": str(production),
			"INTERACTIVE":False,
		})
		if add_secret_key:
			dev0s.env.export(export=["__defaults__/env/json"], env={
				"DJANGO_SECRET_KEY":String().generate(capitalize=True, digits=True, length=128),
			})
		self.migrations()
		if dev0s.defaults.options.log_level >= 1:
			dev0s.response.log(f"Starting {self.name}.", save=True)
		sys.argv = [f"{self.root}/manage.py", "runserver", f"{host}:{port}"]
		import manage
		manage.main()
		
		# handlers.
		return dev0s.response.success(f"Successfully stopped website [{self.root}].")

		#
	def create(self):

		# create.
		if not Files.exists(self.root): os.mkdir(self.root)

		# copy files.
		Files.copy(f"{SOURCE_PATH}/classes/django/lib/django/", f"{self.root}/", delete=False)

		# create proc file
		#path = f"{self.root}/Procfile"
		#Files.save(path, "web: gunicorn __defaults__.django.wsgi")
		#os.system(f"chmod +x {path}")

		# handlers.
		return dev0s.response.success(f"Successfully created django website [{self.root}].")

		#
	def create_app(self, name="home"):

		# checks.
		path = f"{self.root}/apps/{name}"
		if Files.exists(path):
			return dev0s.response.error(f"App [{name}] already exists.")

		# copy.
		Files.copy(f"{SOURCE_PATH}/classes/django/lib/app", path)

		# handlers.
		return dev0s.response.success(f"Successfully created app [{name}].")
	def migrations(self, forced=False, log_level=dev0s.defaults.options.log_level):
		#dev0s.response.log("&RED&Starting migrations&END&")
		if not Files.exists(f"{self.database}/data/"): os.mkdir(f"{self.database}/data/")
		if not Files.exists(f"{self.database}/data/db.sqlite3") or forced:
			dev0s.response.log(f"Applying {ALIAS} webserver migrations.")
			dev0s.env.export(export="__defaults__/env/json", env={"MIGRATIONS": True,})
			os.chdir(self.root)
			#import manage
			#old_argv = list(sys.argv)
			#sys.argv = [f"{self.root}/manage.py", "migrate"]
			#manage.main()
			#os.system(f"cd {self.root} && python3 ./manage.py migrate")
			response = dev0s.code.execute(f"cd {self.root} && {dev0s.defaults.vars.executable} ./manage.py migrate")
			print(response.output)
			if not response.success: return response
			dev0s.env.export(export="__defaults__/env/json", env={"MIGRATIONS": False,})
			#sys.argv = old_argv
		#dev0s.response.log("&GREEN&Done&END&")
		return dev0s.response.success(f"Successfully checked the migrations.")
	def collect_static(self, log_level=dev0s.defaults.options.log_level):
		#dev0s.response.log("&RED&Collecting static&END&")
		if log_level >= 1:
			dev0s.response.log(f"Checking the {ALIAS} webserver migrations.")
		if not Files.exists(f"{self.database}/data/"): os.mkdir(f"{self.database}/data/")
		dev0s.env.export(export="__defaults__/env/json", env={
			"MIGRATIONS": str(True),
		})
		os.system(f"cd {self.root}/ && . __defaults__/env/bash && export MIGRATIONS='true' && {dev0s.defaults.vars.executable} ./manage.py collectstatic" )
		dev0s.env.export(export="__defaults__/env/json", env={
			"MIGRATIONS": str(False),
		})
		#dev0s.response.log("&GREEN&Done&END&")
		return dev0s.response.success(f"Successfully checked the static files.")

# the django database users.
class Users(_defaults_.Defaults):
	def __init__(self, 
		# defaults.
		defaults=None,
	):

		# docs.
		DOCS = {
			"module":"website.django.users", 
			"initialized":True,
			"description":[], 
			"chapter": "Django", }

		# defaults.
		_defaults_.Defaults.__init__(self, traceback="w3bsite.Website.django.users")
		self.assign(defaults.dict())

		#
	def create(self,
		username=None,
		email=None,
		password=None,
		name=None,
		superuser=False,
		activated=True,
	):
		# check arguments.
		response = dev0s.response.parameters.check(
			traceback=self.__traceback__(function="create"),
			parameters={
				"username":username,
				"email":email,
				"password":password,
			})
		if not response.success: return response

		try:

			django_user = DjangoUser.objects.create_user(username, email, password)
			if isinstance(name, str): django_user.last_name = name
			if isinstance(superuser, (bool,Boolean)): django_user.is_superuser = bool(superuser)
			if isinstance(activated, (bool,Boolean)): django_user.is_active = bool(activated)
			django_user.save()

			# success.
			return dev0s.response.success(f"Successfully created django user {username}.", {
				"user":django_user,
			})

		# error.
		except Exception as e:  return dev0s.response.error(f"Failed to create django user {username}, error: {e}.")

		#
	def update(self,
		# required.
		username=None,
		# optionals.
		email=None,
		password=None,
		name=None,
		superuser=None,
		activated=None,
	):
		# check arguments.
		response = dev0s.response.parameters.check(
			traceback=self.__traceback__(function="update"),
			parameters={
				"username":username,
				#"email":email,
				#"password":password,
			})
		if not response.success: return response

		# create.
		response = self.get(username=username)
		if not response.success: return response
		django_user = response.user
		try:
			edits = 0
			if name != None: 
				edits += 1
				django_user.last_name = name
			if email != None: 
				edits += 1
				django_user.email = email
			if isinstance(superuser, (bool, Boolean)): 
				edits += 1
				django_user.is_superuser = bool(superuser)
			if isinstance(activated, (bool, Boolean)):
				edits += 1
				django_user.is_active = bool(activated)
			if password != None: 
				edits += 1
				django_user.set_password(password)
			if edits > 0: django_user.save()

			# success.
			return dev0s.response.success(f"Successfully updated django user {username}.", {
				#"user":django_user,
			})

		# error.
		except Exception as e:  return dev0s.response.error(f"Failed to update django user {username}, error: {e}.")

		#
	def authenticate(self, 
		# the login credentials.
		username=None,
		password=None,
		# the request.
		request=None,
		# login the user.
		login=True,
	):

		# check arguments.
		response = dev0s.response.parameters.check(
			traceback=self.__traceback__(function="authenticate"),
			parameters={
				"username":username,
				"password":password,
			})
		if not response.success: return response

		# authenticate.
		try:
			user = authenticate(username=username, password=password)
			if user is not None: a=1
			else:
				dev0s.response.log(f"Invalid verification attempt for user [{username}].")
				return dev0s.response.error(f"Invalid verification.")

			# success.
			if login:
				_login_(request, user)

			# success.
			return dev0s.response.success(f"Successfully authenticated user {username}.", {
				#"user":django_user,
			})
		# error.
		except Exception as e:  return dev0s.response.error(f"Failed to login user {username}, error: {e}.")

		#
	def delete(self, username=None):

		# check arguments.
		response = dev0s.response.parameters.check(
			traceback=self.__traceback__(function="delete"),
			parameters={
				"username":username,
			})
		if not response.success: return response

		# create.
		try:
			django_user = DjangoUser.objects.get(username=username)
			django_user.delete()

			# success.
			return dev0s.response.success(f"Successfully deleted django user {username}.", {
				#"user":django_user,
			})

		# error.
		except Exception as e:  return dev0s.response.error(f"Failed to delete django user {username}, error: {e}.")

		#
	def get(self, 
		# select one of the following user id options:
		username=None, 
		email=None,
	):

		# checks.
		if username != None and "@" in username:
			raise dev0s.exceptions.InvalidUsage("An username can not contain a [@] character. You most likely passed an email for the username parameter.")
		if email != None and "@" not in email:
			raise dev0s.exceptions.InvalidUsage(f"Invalid email [{email}].")

		# by username.
		identifier = None
		if username not in [None,"None"]:
			identifier = f"(username: {username})"

			# create.
			try:
				django_user = DjangoUser.objects.get(username=username)

			# error.
			except Exception as e:  return dev0s.response.error(f"Failed to retrieve django user {identifier}, error: {e}.")

		# by email.
		elif email not in [None,"None"]:
			identifier = f"(email: {email})"

			# create.
			try:
				django_user = DjangoUser.objects.get(email=email)

			# error.
			except Exception as e:  return dev0s.response.error(f"Failed to retrieve django user {identifier}, error: {e}.")

		# invalid.
		else: return dev0s.response.error(f"{self.__traceback__(function='get')}: Define one of the following parameters: [username, email].")

		# success.
		return dev0s.response.success(f"Successfully retrieved django user {identifier}.", {
			"user":django_user,
			"username":django_user.username,
			"email":django_user.email,
			"name":django_user.last_name,
			"superuser":django_user.is_superuser,
		})

		#
	def exists(self, 
		# option 1:
		# by username (much faster).
		username=None,
		# option 2:
		# by email.
		email=None,
	):

		# by username.
		identifier = None
		if username != None:
			identifier = username

			# create.
			try:
				exists = DjangoUser.objects.filter(username=username).exists()

				# success.
				return dev0s.response.success(f"Successfully checked the existance of django user {username}.", {
					"exists":exists,
				})

			# error.
			except Exception as e:  return dev0s.response.error(f"Failed to check the existance of django user {username}, error: {e}.")

		# by email.
		elif email != None:
			identifier = email

			# get.
			exists = True
			response = self.get(email=email)
			if response.error != None and "User matching query does not exist" not in response.error: return response
			elif response.error != None and "User matching query does not exist" in response.error: exists = False
			return dev0s.response.success(f"Successfully checked the existance of django user {identifier}.", {
				"exists":exists,
			})

		# invalid.
		else: return dev0s.response.error(f"{self.__traceback__(function='exists')}: Define one of the following parameters: [username, email].")


		#



