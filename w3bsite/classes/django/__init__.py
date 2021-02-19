#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_
try:
	from django.contrib.auth.models import User as DjangoUser
	from django.contrib.auth import authenticate, login
	from django.contrib.auth import login as _login_
except Exception as e:
	if syst3m.env.get_boolean("DJANGO_RUNNING") == True:
		raise ValueError(e)

# the django object class.
class Django(_defaults_.Defaults):
	def __init__(self, 
		# the security object.
		security=None,
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
		
		# arguments.
		# ...

		# objects.
		self.security = security
		self.users = Users(defaults=defaults)

		#
	def start(self):

		# check migrations.
		migrations = ""
		if not os.path.exists(f"{self.database}/data/db.sqlite3"):
			migrations = "export MIGRATIONS=True && ./manage.py migrate"

		# start django.
		print(f"Starting website [{self.root}].")
		file = Files.File('/tmp/django.start.sh')
		if OS in ["macos"]:
			file.save(f"""
				cd {self.root}/
				source .secrets/env.sh
				export PRODUCTION=False
				export MAINTENANCE=False
				{migrations}
				./manage.py runserver
			""")
		else:
			file.save(f"""
				cd {self.root}/
				. .secrets/env.sh
				export PRODUCTION=False
				export MAINTENANCE=False
				{migrations}
				./manage.py runserver
			""")
		file.file_path.permission.set(755)
		self.django_process = subprocess.Popen(["sh", file.file_path.path])
		try:
			self.django_process.wait()
		except KeyboardInterrupt:
			self.django_process.terminate()
			os.system(f"pkill -9 -f {file.file_path.name()}")
			file.file_path.delete(forced=True)

		# handlers.
		return r3sponse.success_response(f"Successfully stopped website [{self.root}].")

		#
	def create(self):

		# create.
		output = utils.__execute_script__(f"""
			cd {self.root}
			django-admin startproject website
			mv website/manage.py manage.py
			mv website/website website-
			rm -fr website
			mv website- website
		""")

		# secrets.
		path = f"{self.root}/website/settings.py"
		if not os.path.exists(path):
			return r3sponse.error_response(f"Failed to create django project [{self.root}].")
		data = utils.__load_file__(path)
		secret_key = data.split("SECRET_KEY = '")[1].split("'")[0]
		if not os.path.exists(f"{self.root}/.secrets"):
			os.mkdir(f"{self.root}/.secrets")
		#utils.__save_file__(f"{self.root}/.secrets/env.sh", f"# Django environment variables.\nexport DJANGO_SECRET_KEY='{secret_key}'\n")
		#utils.__save_json__(f"{self.root}/.secrets/env.json", {f"DJANGO_SECRET_KEY":secret_key})
		self.security.set_secret_env("DJANGO_SECRET_KEY", secret_key)

		# copy urls.py
		path = f"{self.root}/website/urls.py"
		os.system(f"rm -fr {path}")
		os.system(f"cp {SOURCE_PATH}/example/website/urls.py {path}")

		# copy settings.py
		path = f"{self.root}/website/settings.py"
		os.system(f"rm -fr {path}")
		os.system(f"cp {SOURCE_PATH}/example/website/settings.py {path}")

		# copy requirements
		path = f"{self.root}/requirements/"
		os.system(f"rm -fr {path}")
		os.system(f"cp -r {SOURCE_PATH}/example/requirements {path}")

		# create requirements.txt
		#path = f"{self.root}/requirements.pip"
		#os.system(f"cp {SOURCE_PATH}/example/requirements.txt {path}")

		# copy classes
		path = f"{self.root}/classes/"
		os.system(f"rm -fr {path}")
		os.system(f"cp -r {SOURCE_PATH}/example/classes {path}")

		# copy apps
		path = f"{self.root}/apps/"
		os.system(f"rm -fr {path}")
		os.system(f"cp -r {SOURCE_PATH}/example/apps {path}")

		# copy static
		path = f"{self.root}/static/"
		os.system(f"rm -fr {path}")
		os.system(f"cp -r {SOURCE_PATH}/example/static {path}")

		# copy templates
		path = f"{self.root}/templates/"
		os.system(f"rm -fr {path}")
		os.system(f"cp -r {SOURCE_PATH}/example/templates {path}")

		# copy .gitignore
		path = f"{self.root}/.gitignore"
		os.system(f"cp {SOURCE_PATH}/example/.gitignore {path}")

		# create proc file
		path = f"{self.root}/Procfile"
		utils.__save_file__(path, "web: gunicorn website.wsgi")
		os.system(f"chmod +x {path}")

		# replace manage.py
		path = f"{self.root}/manage.py"
		data = utils.__load_file__(path)
		utils.__save_file__(path, data.replace("#!/usr/bin/env python", "#!/usr/bin/env python3"))

		# handlers.
		return r3sponse.success_response(f"Successfully created django website [{self.root}].")
	def create_app(self, name="home"):

		# checks.
		path = f"{self.root}/apps/{name}"
		if os.path.exists(path):
			return r3sponse.error_response(f"App [{name}] already exists.")

		# copy.
		os.system(f"cp -r {SOURCE_PATH}/example/app {path}")

		# handlers.
		return r3sponse.success_response(f"Successfully created app [{name}].")

# the django database users.
class Users(_defaults_.Defaults):
	def __init__(self, 
		# defaults.
		defaults=None,
	):

		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		#
	def create(self,
		username=None,
		email=None,
		password=None,
		name=None,
		superuser=False,
	):
		# check arguments.
		response = r3sponse.check_parameters({
			"username":username,
			"email":email,
			"password":password,})
		if not response.success: return response

		# create.
		#try:
		print("USERNAME:",username)
		print("EMAIL:",email)
		print("PASSWORD:",password)

		if True:
			django_user = DjangoUser.objects.create_user(username, email, password)
			if isinstance(name, str): django_user.last_name = name
			if isinstance(superuser, bool): django_user.is_superuser = superuser
			django_user.save()

			# success.
			return r3sponse.success_response(f"Successfully created django user {username}.", {
				"user":django_user,
			})

		# error.
		#except Exception as e:  return r3sponse.error_response(f"Failed to create django user {username}, error: {e}.")

		#
	def update(self,
		# required.
		username=None,
		# optionals.
		email=None,
		password=None,
		name=None,
		superuser=None,
	):
		# check arguments.
		response = r3sponse.check_parameters({
			"username":username,
			"email":email,
			"password":password,})
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
			if isinstance(superuser, bool): 
				edits += 1
				django_user.is_superuser = superuser
			if password != None: 
				edits += 1
				django_user.set_password(password)
			if edits > 0: django_user.save()

			# success.
			return r3sponse.success_response(f"Successfully updated django user {username}.", {
				#"user":django_user,
			})

		# error.
		except Exception as e:  return r3sponse.error_response(f"Failed to update django user {username}, error: {e}.")

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
		response = r3sponse.check_parameters({
			"username":username,
			"password":password,})
		if not response.success: return response

		# authenticate.
		try:
			user = authenticate(username=username, password=password)
			if user is not None: a=1
			else:
				response["error"] = f"Invalid verification."
				utils.__log__(f"Invalid verification attempt for user [{username}] ip address [{ip}].")
				return response

			# success.
			if login:
				_login_(request, user)

			# success.
			return r3sponse.success_response(f"Successfully authenticated user {username}.", {
				#"user":django_user,
			})
		# error.
		except Exception as e:  return r3sponse.error_response(f"Failed to login user {username}, error: {e}.")

		#
	def delete(self, username=None):

		# check arguments.
		response = r3sponse.check_parameters({
			"username":username,})
		if not response.success: return response

		# create.
		try:
			django_user = DjangoUser.objects.get(username=username)
			django_user.delete()

			# success.
			return r3sponse.success_response(f"Successfully deleted django user {username}.", {
				#"user":django_user,
			})

		# error.
		except Exception as e:  return r3sponse.error_response(f"Failed to delete django user {username}, error: {e}.")

		#
	def get(self, 
		# select one of the following user id options:
		username=None, 
		email=None,
	):

		# by username.
		identifier = None
		if username != None:
			identifier = username

			# create.
			try:
				django_user = DjangoUser.objects.get(username=username)

			# error.
			except Exception as e:  return r3sponse.error_response(f"Failed to retrieve django user {username}, error: {e}.")

		# by email.
		elif email != None:
			identifier = email

			# create.
			try:
				django_user = DjangoUser.objects.get(email=email)

			# error.
			except Exception as e:  return r3sponse.error_response(f"Failed to retrieve django user {email}, error: {e}.")

		# invalid.
		else: return r3sponse.error_response(f"Define one of the following parameters: [username, email].")

		# success.
		return r3sponse.success_response(f"Successfully retrieved django user {identifier}.", {
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
				return r3sponse.success_response(f"Successfully checked the existsance of django user {username}.", {
					"exists":exists,
				})

			# error.
			except Exception as e:  return r3sponse.error_response(f"Failed to check the existsance of django user {username}, error: {e}.")

		# by email.
		elif email != None:
			identifier = email

			# get.
			exists = True
			response = self.get(email=email)
			if response.error != None and "User matching query does not exist" not in response.error: return response
			elif response.error != None and "User matching query does not exist" in response.error: exists = False
			return r3sponse.success_response(f"Successfully checked the existsance of django user {identifier}.", {
				"exists":exists,
			})

		# invalid.
		else: return r3sponse.error_response(f"Define one of the following parameters: [username, email].")


		#



