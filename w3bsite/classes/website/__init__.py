#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import security, heroku, namecheap, utils, git, users, stripe, logging, rate_limit, deployment, vps, defaults, apps, views
from w3bsite.classes import database as _database_
import django as pypi_django

# the main website class.
class Website(CLI.CLI,Traceback):
	def __init__(self,
		#
		# General.
		# 	the root path.
		root=None, # example: FilePath(__file__).base(back=1).replace("./","")
		# 	the root domain.
		domain=None,
		# 	the website name.
		name=None,
		# 	the database path (optional).
		database=None,
		# 	the library path (optional).
		library=None,
		#a
		# Deployment.
		# 	remote depoyment, options: [local, vps, heroku].
		remote="local",
		#
		# Developers.
		#	the developer users (emails).
		developers=[],
		#
		# Django.
		#	maintenance boolean.
		maintenance=False,
		# 	the template data (only required when running the website) (overwrites the w3bsite template data keys).
		template_data={},
		#	2fa required for login.
		_2fa=False,
		#
		# Organization.
		# 	the author's / comitters name.
		author=None,
		# 	the admin's email.
		email=None,
		# 	the organization name.
		organization=None,
		# 	the organization unit.
		organization_unit="Information Technology",
		# 	the organization country code.
		country_code="NL",
		# 	the organization localization's city name.
		city=None,
		# 	the organization localization's province / state.
		province=None,
		#
		# AES.
		#	the passphrase of the aes master-key (defaults is no passphrase).
		aes_passphrase=None,
		#
		# Namecheap.
		#	namecheap enabled.
		namecheap_enabled=True,
		# 	your namecheap username.
		namecheap_username=None,
		# 	your namecheap api key.
		namecheap_api_key=None,
		#
		# Firebase.
		#	firebase enabled.
		firebase_enabled=True,
		# 	your firebase admin service account key, (dict) [https://console.firebase.google.com > Service Accounts > Firebase admin].
		firebase_admin={},
		# 	your firebase sdk javascript configuration, (dict) [https://console.firebase.google.com > Settings > General > Web JS SDK].
		firebase_js={},
		#
		# Stripe.
		# enable strip.e
		stripe_enabled=True,
		# 	your stripe secret key (str) [https://stripe.com > Dashboard > Developer > API Keys > Secret Key].
		stripe_secret_key=None,
		# 	your stripe publishable key (str) [https://stripe.com > Dashboard > Developer > API Keys > Secret Key].
		stripe_publishable_key=None,
		#	the stripe subscriptions.
		#		do not edit the plan & product names after creation.
		#		price changes are not supported yet, will be in the future.
		stripe_subscriptions={
			#"nas-server": {
			#	"basic": {
			#		"rank":1,
			#		"price":50,
			#		"currency":"eur",
			#		"favicon":"https://raw.githubusercontent.com/vandenberghinc/public-storage/master/nas-server/icon/icon.png"
			#	},
			#	"premium": {
			#		"rank":2,
			#		"price":100,
			#		"currency":"eur",
			#	},
			#	"pro": {
			#		"rank":3,
			#		"price":250,
			#		"currency":"eur",
			#	},
			#}
		},
		# 	the stripe products.
		stripe_products={
			#"nas-server": {
			#	"basic": {
			#		"rank":1,
			#		"price":50,
			#		"currency":"eur",
			#		"favicon":"https://raw.githubusercontent.com/vandenberghinc/public-storage/master/nas-server/icon/icon.png"
			#	},
			#	"premium": {
			#		"rank":2,
			#		"price":100,
			#		"currency":"eur",
			#	},
			#	"pro": {
			#		"rank":3,
			#		"price":250,
			#		"currency":"eur",
			#	},
			#}
		},
		#
		#
		# Smtp Email
		# 	sending emails [https://gmail.com > Security > Enable Unsafe 3th party applications].
		email_enabled=True,
		email_address=None,
		email_password=None,
		email_smtp_host="smtp.gmail.com",
		email_smtp_port=587,
		#
		# VPS.
		# 	the public ip of the vps.
		vps_ip=None,
		#	the vps ssh port.
		vps_port=22,
		#	the executing username on the vps.
		vps_username=None,
		#
		# Additional Options.
		# 	prevent heroku deployment.
		prevent_heroku_deployment=False,
		# 	purchase tls/ssl certificate from namecheap.
		purchase_tls_certificate=False,
		# 	interactive mode.
		interactive=False,
		#	production mode.
		production=True,
		# 	the users sub path.
		users_subpath="users/",
		# 	id users by username.
		id_by_username=True,
		#
		# the logs.
		log_level=Defaults.options.log_level,
		# styling options.
		styling={},
		#
		# 
		# optionally initizialize from a serialized dict (for config.py) (still requires parameters: root).
		serialized=None,
	):	

		# defaults.
		Traceback.__init__(self, traceback="w3bsite.Website",)

		# w3bsite values.
		self.SOURCE_PATH = SOURCE_PATH

		# argurments.
		if root != None:
			if root[len(root)-1] != "/": root += "/"
			if root[-3:] == "/./": root = root[:-3]
			if root[len(root)-1] != "/": root += "/"
			root = root.replace("//","/").replace("//","/")
			if firebase_admin != None:
				if isinstance(firebase_admin, str) and firebase_admin[:len("__defaults__/env")] == "__defaults__/env":
					firebase_admin = f"{root}/{firebase_admin}".replace("//","/").replace("//","/")
		self.root = gfp.clean(root)
		self.name = name
		self.author = author
		self.email = email
		self.city = city
		self.province = province
		self.organization = organization
		self.organization_unit = organization_unit
		self.country_code = country_code
		self.domain = domain
		self.namecheap_username = namecheap_username
		self.namecheap_api_key = namecheap_api_key
		self.firebase_admin = firebase_admin
		self.firebase_js = firebase_js
		self.stripe_secret_key = stripe_secret_key
		self.stripe_publishable_key = stripe_publishable_key
		self.email_address = email_address
		self.email_password = email_password
		self.email_smtp_host = email_smtp_host
		self.email_smtp_port = email_smtp_port
		self.purchase_tls_certificate = purchase_tls_certificate
		self.aes_passphrase = aes_passphrase
		self.stripe_subscriptions = stripe_subscriptions
		self.stripe_products = stripe_products
		self.developers = developers
		if remote == None: self.remote = remote
		else: self.remote = remote.lower()
		self.vps_ip = vps_ip
		self.vps_port = vps_port
		self.vps_username = vps_username
		self._2fa = _2fa
		self.template_data = template_data
		self.database = database
		self.library = library
		self.prevent_heroku_deployment = prevent_heroku_deployment
		self.interactive = interactive
		self.production = production
		self.maintenance = maintenance
		self.firebase_enabled = firebase_enabled
		self.stripe_enabled = stripe_enabled
		self.namecheap_enabled = namecheap_enabled
		self.email_enabled = email_enabled
		self.log_level = log_level
		self.users_subpath = users_subpath
		self.id_by_username = id_by_username
		self.styling = styling
		# checks.
		if self.database == None: self.database = f"/etc/{self.domain}/"
		if self.library == None: self.library = f"/usr/local/lib/{self.domain}/"
		if self.domain != None: self.domain = utils.naked_url(self.domain)

		# serialize.
		if serialized == None or serialized == {}:
			self.serialize(save=True)
		else:
			if isinstance(serialized, str):
				serialized = Files.load(serialized, format="json")
			self.init_from_serialized(serialized=serialized)
		#if root != dev0s.utils.__execute_script__("pwd").replace("\n",""):
		#	raise ValueError("The ")

		# init.
		response = self.initialize()
		if not response.success: response.crash()

		#
	def initialize(self):

		# overall arguments.
		response = Response.parameters.check(
			traceback=self.__traceback__(),
			parameters={
				"root":self.root,
				"database":self.database,
				"library":self.library,
				"name":self.name,
				"organization":self.organization,
				"domain":self.domain,
				"developers":self.developers,
				"_2fa":self._2fa,
			})
		if not response.success: raise ValueError(response.error)

		# namecheap arguments.
		if self.namecheap_enabled:
			response = Response.parameters.check(
				traceback=self.__traceback__(),
				parameters={
					"author":self.author,
					"email":self.email,
					"city":self.city,
					"province":self.province,
					"organization_unit":self.organization_unit,
					"country_code":self.country_code,
					"namecheap_username":self.namecheap_username,
					"namecheap_api_key":self.namecheap_api_key,
				})
			if not response.success: raise ValueError(response.error)

		# firebase arguments.
		if self.firebase_enabled:
			response = Response.parameters.check(
				traceback=self.__traceback__(),
				parameters={
					"firebase_admin":self.firebase_admin,
					"firebase_js":self.firebase_js,
				})
			if not response.success: raise ValueError(response.error)

		# stripe arguments.
		if self.stripe_enabled:
			response = Response.parameters.check(
				traceback=self.__traceback__(),
				parameters={
					"stripe_secret_key":self.stripe_secret_key,
					"stripe_publishable_key":self.stripe_publishable_key,
					"stripe_subscriptions":self.stripe_subscriptions,
					"stripe_products":self.stripe_products,
				})
			if not response.success: raise ValueError(response.error)

		# email arguments.
		if self.email_enabled:
			response = Response.parameters.check(
				traceback=self.__traceback__(),
				parameters={
					"email_address":self.email_address,
					"email_password":self.email_password,
					"email_smtp_host":self.email_smtp_host,
					"email_smtp_port":self.email_smtp_port,
				})
			if not response.success: raise ValueError(response.error)

		# remote: vps arguments.
		if self.remote in ["vps"]:
			response = Response.parameters.check(
				traceback=self.__traceback__(),
				parameters={
					"vps_ip":self.vps_ip,
					"vps_port":self.vps_port,
					"vps_username":self.vps_username,
				})
			if not response.success: raise ValueError(response.error)

		# set variables.
		self.live = utils.equalize_path(self.root, striplast=True) == utils.equalize_path(self.library, striplast=True)
		self.http_domain = f"http://{self.domain}"
		self.https_domain = f"https://{self.domain}"

		# environment for settings.py.
		os.chdir(gfp.clean(self.root))
		if not os.path.exists("__defaults__/env"): os.mkdir("__defaults__/env")
		SECRET_KEY = Environment.get("DJANGO_SECRET_KEY", default=None)
		if SECRET_KEY == None:  SECRET_KEY = String().generate(length=128, capitalize=True, digits=True, special=True)
		Environment.export(export="__defaults__/env/json", env={
			"DJANGO_SECRET_KEY":SECRET_KEY,
			"WEBSITE_BASE":gfp.base(SOURCE_PATH),
			"DOMAIN":str(self.domain),
			"DATABASE":str(self.database),
			"PRODUCTION":str(self.production),
		})

		# template data.
		colors = {
			"white":"#FAFAFA",
			"light_white":"#E9F0FD",
			"grey":"#E5E5E5",
			"light_grey":"#D6D6D6",
			"dark_grey":"#424242",
			"blue":"#5A8FE6",
			"purple":"#323B83",#"#B32FCA",
			#"purple":"#9B00AA",
			"red":"#FD304E",
			"pink":"#F62B7D",
			"orange":"#FF8800",
			"green":"#006633",
			"darkest":"#1F2227",
			"darker": "#20242A",
			"dark": "#262B30",
			# background color.
			"topbar":"#FAFAFA",#1F2227", #"#FAFAFA",
			"background":"#323B83",#"#E7E9EF", #"#FAFAFA",
			"topbar_darkmode":"#1F2227",#1F2227", #"#FAFAFA",
			"background_darkmode":"#1F2227",#"#E7E9EF", #"#FAFAFA",
			"background_img":None,
			# elements.
			"widgets":"#FAFAFA",
			"widgets_reversed":"#323B83",#"#1F2227",
			"widgets_darkmode":"#20242A",
			"widgets_reversed_darkmode":"#323B83",#"#1F2227",
			# text.
			"text":"#1F2227",
			"text_reversed":"#FAFAFA",
			"text_darkmode":"#FAFAFA",
			"text_reversed_darkmode":"#FAFAFA",
			# input & textareas.
			"input_txt":"#6C6B6D",
			"input_txt_reversed":"#FAFAFA",
			"input_bg":"#E9F0FD", #"#FAFAFA", 
			"input_bg_reversed":"#323B83",
			
			# buttons.
			"button_txt":"#FAFAFA",
			"button_txt_reversed":"#1F2227",
			"button_bg":"#323B83",
			"button_bg_reversed":"#FAFAFA",
			# custom colors.
			# ...
		}

		# check styling.
		d = {}
		for key,value in self.styling.items(): d[key.upper()] = value
		styling = Dictionary(d).check(default={
			# styling options.
			"LEFTBAR_WIDTH":280, # px
			"RIGHTBARBAR_WIDTH":280, # px
			"TOPBAR_HEIGHT":50 #px
			})
		self.template_data = Dictionary(utils.__append_dict__(new=self.template_data, overwrite=True,  old=styling))

		# add safe template data.
		self.template_data = Dictionary(utils.__append_dict__(new=self.template_data, overwrite=True,  old={
			# colors.
			"COLORS":colors,
			# wbsite info.
			"NAME":self.name,
			"DOMAIN":self.domain,
			"PRODUCTION":self.production,
			"AUTHOR":self.author,
			"ORGANIZATION":self.organization,
			# include other tempalte data's.
			"STRIPE":{},
			"FIREBASE":{},
			# options.
			"2FA":self._2fa,
			# styling options.
			"LEFTBAR_WIDTH":280, # px
			"RIGHTBARBAR_WIDTH":280, # px
			"TOPBAR_HEIGHT":50 #px
		}))

		# defaults objects.
		self.logging = logging.Logging(
			name=self.name,
			root=self.root,
			database=self.database,)
		self.aes = encrypti0n.aes.AsymmetricAES(
			private_key=f"{self.root}/__defaults__/aes/private_key",
			public_key=f"{self.root}/__defaults__/aes/public_key",
			passphrase=self.aes_passphrase)
		self.defaults = defaults.Defaults(
			root=self.root,
			library=self.library,
			database=self.database,
			name=self.name,
			author=self.author,
			email=self.email,
			organization=self.organization,
			country_code=self.country_code,
			province=self.province,
			city=self.city,
			organization_unit=self.organization_unit,
			domain=self.domain,
			https_domain=self.https_domain,
			developers=self.developers,
			remote=self.remote,
			live=self.live,
			interactive=self.interactive,
			_2fa=self._2fa,
			maintenance=self.maintenance,
			users_subpath=self.users_subpath,
			template_data=self.template_data,
			id_by_username=self.id_by_username,
			aes=self.aes,
			logging=self.logging,)
		self.utils = utils.Utils(attributes=self.defaults.attributes())

		# objects.
		self.security = security.Security(
			defaults=self.defaults,)
		if self.firebase_enabled and Defaults.vars.os not in ["macos"]:
			from w3bsite.classes import firebase
			self.firebase = firebase.Firebase(
				key=self.firebase_admin,
				firebase_js=self.firebase_js,
				defaults=self.defaults)
			self.firestore = self.firebase.firestore
			self.db = _database_.Database(
				firestore=self.firebase.firestore,
				path=self.database,
				live=self.live,)
		else:
			self.firebase = None
			self.firestore = None
			self.db = _database_.Database(path=self.database, live=self.live)
		if self.stripe_enabled:
			self.stripe = stripe.Stripe(
				secret_key=self.stripe_secret_key,
				publishable_key=self.stripe_publishable_key,
				subscriptions=self.stripe_subscriptions,
				products=self.stripe_products,
				defaults=self.defaults)
		else: self.stripe = None
		self.rate_limit = rate_limit.RateLimit(
			db=self.db,
			defaults=self.defaults,)
		if not os.path.exists("__defaults__/django/settings.py"): raise ImportError(f"Invalid website hierarchy, unable to find: __defaults__.django.settings, required location: {self.root}/__defaults__/django/settings.py")
		os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'__defaults__.django.settings')
		from __defaults__.django import settings
		try:pypi_django.setup()
		except: a=1
		from w3bsite.classes import django
		self.django = django.Django(
			security=self.security,
			defaults=self.defaults,)
		self.users = users.Users(
			email_address=self.email_address,
			email_password=self.email_password,
			smtp_host=self.email_smtp_host,
			smtp_port=self.email_smtp_port,
			firestore=self.firestore,
			email_enabled=self.email_enabled,
			db=self.db,
			stripe=self.stripe,
			django=self.django,
			defaults=self.defaults,)
		if self.namecheap_enabled:
			self.namecheap = namecheap.Namecheap(
				username=self.namecheap_username,
				api_key=self.namecheap_api_key,
				root=self.root,
				domain=self.domain,
				email=self.email_address,)
		else: self.namecheap = None
		self.git = git.Git(
			defaults=self.defaults,)#
		# mode dependend objects.
		self.deployment = None
		self.heroku = None
		self.vps = None
		if self.remote in ["local", "vps"]:
			self.deployment = deployment.Deployment(
				root=self.root,
				library=self.library,
				name=self.name,
				domain=self.domain,
				database=self.database,
				remote=self.remote,
				vps_ip=self.vps_ip,
				vps_username=self.vps_username,
				namecheap=self.namecheap,)
			if self.remote in ["vps"]:
				self.vps = vps.VPS(
					ip=self.vps_ip,
					port=self.vps_port,
					username=self.vps_username,
					namecheap=self.namecheap,
					deployment=self.deployment,
					defaults=self.defaults,)
		elif self.remote == "heroku":
			self.heroku = heroku.Heroku(
				root=self.root,
				domain=self.doman,
				name=self.name,
				namecheap=self.namecheap,
				logging=self.logging,)
		elif self.remote != None:
			raise ValueError(f"Selected an invalid remote [{self.remote}], options: [local, vps, heroku]")
		self.apps = apps.Apps(
			template_data=self.template_data,
			rate_limit=self.rate_limit,
			users=self.users,
			stripe=self.stripe,
			utils=self.utils,
			defaults=self.defaults,)

		# defaults.
		CLI.CLI.__init__(self,
			modes={
				"Development":"*chapter*",
				"    --create":"Create the website.",
				"    --create-app dashboard":"Create a new application.",
				"    --start --developer":"Start the production webserver.",
				"Production":"*chapter*",
				"    --start":"Start the nginx webserver.",
				"    --stop":"Stop the nginx webserver.",
				"    --restart":"Restart the nginx webserver.",
				"    --status":"Retrieve the status of the nginx webserver.",
				"Deployment":"*chapter*",
				"    --generate-aes-passphrase":"Generate an aes passphrase.",
				"    --generate-tls":"Generate a tls certificate.",
				"    --activate-tls":"Activate the generated tls certificate.",
				"    --bundle-tls /path/to/downloaded/cert/":"Bundle the downloaded signed certificate from the CA.",
				"    --deploy":"Deploy the website.",
				"Logs":"*chapter*",
				"    --tail [optional: --nginx]":"Tail the (deployed) website.",
				"Documentation":"*chapter*",
				"    -h / --help":"Show the documentation.",
			},
			options={
				#"-c":"Do not clear the logs.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		# logs.
		if Defaults.options.log_level >= 1:
			print(f"Website: {self.name}")
			print(f" * domain: {self.domain}")
			print(f" * root: {self.root}")
			print(f" * library: {self.library}")
			print(f" * database: {self.database}")
			print(f" * pwd: {Defaults.pwd()}")
			print(f" * remote: {self.remote}")
			print(f" * live: {self.live}")

		# handler.
		return Response.success(f"Successfully initialized website [{self.name}].")

		#
	def cli(self):

		# check args.
		self.arguments.check(exceptions=["--log-level", "--non-interactive", "--create-alias", "--developer", "--nginx", "--code-update", "--forced", "-f"])

		# activate enc.
		if self.remote in ["vps"] and not self.vps.live:
			if not ssht00ls_agent.generated:
				response = ssht00ls_agent.generate()
				if not response.success: self.stop(response=response, json=Defaults.options.json)
			elif not ssht00ls_agent.activated:
				response = ssht00ls_agent.activate()
				if not response.success: self.stop(response=response, json=Defaults.options.json)

		# help.
		if self.arguments.present("-h"):
			self.docs(success=True)

		# version.
		elif self.arguments.present(['--version']):
			self.stop(message=f"{ALIAS} version:"+Files.load(f"{SOURCE_PATH}/.version").replace("\n",""), json=Defaults.options.json)

		# developer start.
		elif self.arguments.present("--start") and self.arguments.present("--developer"):
			response = self.django.start()
			Response.log(response=response)

		# start.
		elif self.arguments.present('--start'):
			if not self.live: 
				Response.log(error="The executing library is not live.")
				sys.exit(1)
			Defaults.operating_system(supported=["linux"])
			command = ""
			for i in ["gunicorn.socket", "gunicorn", "nginx"]:
				command += f"sudo systemctl start {i} &&"
			command = command[:-3]
			output = dev0s.utils.__execute_script__(command)
			if output in ["", "\n"]:
				print(f"Successfully started {self.domain}")
			else:
				print(f"Failed to started {self.domain};\n{output}")

		# stop.
		elif self.arguments.present('--stop'):
			if not self.live: 
				Response.log(error="The executing library is not live.")
				sys.exit(1)
			Defaults.operating_system(supported=["linux"])
			command = ""
			for i in ["gunicorn.socket", "gunicorn", "nginx"]:
				command += f"sudo systemctl stop {i} &&"
			command = command[:-3]
			output = dev0s.utils.__execute_script__(command)
			if output in ["", "\n"]:
				print(f"Successfully stopped {self.domain}")
			else:
				print(f"Failed to stopped {self.domain};\n{output}")

		# restart.
		elif self.arguments.present('--restart'):
			if not self.live: 
				Response.log(error="The executing library is not live.")
				sys.exit(1)
			Defaults.operating_system(supported=["linux"])
			command = ""
			for i in ["gunicorn.socket", "gunicorn", "nginx"]:
				command += f"sudo systemctl restart {i} &&"
			command = command[:-3]
			output = dev0s.utils.__execute_script__(command)
			if output in ["", "\n"]:
				print(f"Successfully restarted {self.domain}")
			else:
				print(f"Failed to restarted {self.domain};\n{output}")

		# status.
		elif self.arguments.present('--status'):
			if not self.live: 
				Response.log(error="The executing library is not live.")
				sys.exit(1)
			Defaults.operating_system(supported=["linux"])
			os.system("sudo systemctl status gunicorn")

		# reset logs.
		elif self.arguments.present('--reset-logs'):
			if not self.live: 
				Response.log(error="The executing library is not live.")
				sys.exit(1)
			os.system(f"echo '' > {self.database}/logs/logs.txt")
			Response.log("Successfully resetted the logs.", log_level=0, save=True)

		# tail.
		elif self.arguments.present('--tail'):
			if not self.live: 
				Response.log(error="The executing library is not live.")
				sys.exit(1)
			if self.arguments.present(["--nginx", "-n"]):
				if self.arguments.present(["--debug", "-d"]):
					os.system(f"cat /var/log/nginx/{self.domain}.debug")
				else:
					os.system(f"cat /var/log/nginx/{self.domain}")
			else:
				os.system(f"cat {self.database}/logs/logs.txt")

		# deploy.
		elif self.arguments.present("--deploy"):
			response = self.deploy(
				code_update=self.arguments.present("--code-update"),
				reinstall=self.arguments.present("--reinstall"),
			)
			Response.log(response=response)

		# generate tls.
		elif self.arguments.present("--generate-tls"):
			response = self.deployment.generate_tls()
			Response.log(response=response)

		# activate tls.
		elif self.arguments.present("--activate-tls"):
			response = self.deployment.activate_tls()
			Response.log(response=response)

		# bundle tls.
		elif self.arguments.present("--bundle-tls"):
			response = self.deployment.bundle_tls(directory=self.arguments.get("--bundle-tls"))
			Response.log(response=response)
		
		# create.
		elif self.arguments.present("--create"):
			response = self.create()
			Response.log(response=response)

		# create app.
		elif self.arguments.present("--create-app"):
			response = self.django.create_app(name=self.arguments.get("--create-app"))
			Response.log(response=response)

		# generate aes passphrase.
		elif self.arguments.present("--generate-aes-passphrase"):
			print(f"Generated AES Passphrase: {utils.__generate__(length=64, capitalize=True, digits=True)}")

		# invalid.
		else: self.invalid()

		#
	def deploy(self, code_update=False, reinstall=False, log_level=0):

		# check git.
		loader = Console.Loader("Checking git repository ...")
		response = self.git.installed()
		if not response.success: 
			loader.stop(success=False)
			return response
		elif not response["installed"]:
			loader.stop()
			loader = Console.Loader("Installing git repository ...")
			response = self.git.install()
			if not response.success: 
				loader.stop(success=False)
				return response
			loader.stop()
		else: loader.stop()

		# heroku remote.
		if self.remote in ["heroku"]:

			# deploy on heroku.
			response = self.heroku.deploy(log_level=log_level)
			if not response.success: return response

		# local remote (& local when vps live).
		elif (self.remote in ["local"]) or (self.remote in ["vps"] and self.live):

			# deploy on local.
			response = self.deployment.deploy(code_update=code_update, reinstall=reinstall, log_level=log_level)
			if not response.success: return response

		# vps remote.
		elif self.remote in ["vps"]:

			# push to vps.
			response = self.vps.deploy(code_update=code_update, reinstall=reinstall, log_level=log_level)
			if not response.success: return response


		# check dns settings.
		if not code_update:
			response = self.check_dns(log_level=log_level)
			if response.error != None: return response
			return Response.success(f"Successfully deployed website https://{self.domain}.")
		else:
			return Response.success(f"Successfully deployed the code updates of website https://{self.domain}.")

		#
	def check_dns(self, log_level=0):
		
		# remote: heroku.
		if self.remote in ["heroku"]:
			response = self.heroku.check_dns(log_level=log_level)
			if not response.success: return response

		# remote: local & vps.
		elif self.remote in ["local", "vps"]:
			if not (self.remote in ["vps"] and self.live):
				response = self.deployment.check_dns(log_level=log_level)
				if not response.success: return response

		# handlers.
		return Response.success(f"Successfully checked the dns settings of website [{self.name}].", log_level=log_level)

		#
	def create(self):

		# create root.
		if not Files.exists(self.root):
			#return Response.error(f"Website [{self.root}] already exists.")
			os.mkdir(self.root)

		# create django.
		loader = Console.Loader("Creating website ...")
		response = self.django.create()
		loader.stop(success=response["success"])
		if response.error != None: return response

		# generate tls.
		loader = Console.Loader("Generating tls ...")
		response = self.security.generate_tls()
		loader.stop(success=response["success"])
		if response.error != None: return response

		# handlers.
		return Response.success(f"Successfully created website [{self.name}].")

		#
	def serialize(self, save=False):
		# serizalized is used by the config.py in deployment.
		# all non secret variables are stored in __defaults__/env/website inside the root/. directory .
		# all secret variables are stored in environment variables from env.sh & env.json.
		# all keys of the stored secrets are stored in the serialzed __defaults__/env/website.

		# serialize and save all non secret variables in the __defaults__/env/website.
		serialized = {
			"root":self.root,
			"database":self.database,
			"library":self.library,
			"name":self.name,
			"email":self.email,
			"city":self.city,
			"province":self.province,
			"organization":self.organization,
			"organization_unit":self.organization_unit,
			"country_code":self.country_code,
			"domain":self.domain,
			"author":self.author,
			#"namecheap_username":self.namecheap_username,
			#"namecheap_api_key":self.namecheap_api_key,
			#"firebase_admin":self.firebase_admin,
			#"stripe_secret_key":self.stripe_secret_key,
			#"stripe_publishable_key":self.stripe_publishable_key,
			#"email_address":self.email_address,
			#"email_password":self.email_password,
			"email_smtp_host":self.email_smtp_host,
			"email_smtp_port":self.email_smtp_port,
			"purchase_tls_certificate":self.purchase_tls_certificate,
			"stripe_subscriptions":self.stripe_subscriptions,
			"stripe_products":self.stripe_products,
			"developers":self.developers,
			"remote":self.remote,
			"vps_ip":self.vps_ip,
			"vps_port":self.vps_port,
			"vps_username":self.vps_username,
			"_2fa":self._2fa,
			"firebase_enabled":self.firebase_enabled,
			"stripe_enabled":self.stripe_enabled,
			"namecheap_enabled":self.namecheap_enabled,
			"email_enabled":self.email_enabled,
			"log_level":self.log_level,
			"users_subpath":self.users_subpath,
			"id_by_username":self.id_by_username,
			"styling":self.styling,
		}

		# save all secret variables in secrets.
		def __handle_dict__(dictionary={}, base=""):
			stored = []
			for key, value in dictionary.items():
				key = key.upper().replace("-","_").replace(".","_")
				if base == "": full_key = key
				else: full_key = base+"_"+key
				_format_ = None
				if isinstance(value, str):
					_format_ = "str"
					local_security.set_secret_env(full_key, value)
				elif isinstance(value, int):
					_format_ = "int"
					local_security.set_secret_env(full_key, str(value))
				elif isinstance(value, bool):
					_format_ = "bool"
					local_security.set_secret_env(full_key, str(value))
				elif value == None:
					_format_ = "null"
					local_security.set_secret_env(full_key, "None")
				elif isinstance(value, dict):
					_format_ = "dict"
					stored += __handle_dict__(value, base=full_key)
				else:
					raise ValueError(f"Cannot secretly serialize [{key}:{value}].")
				#print(f"Stored secret environment variable: {key}.")
				stored.append([full_key, _format_])
			return stored
		local_security = security.Security(
			# the root path.
			root=self.root,)
		stored = __handle_dict__({
			"FIREBASE_ADMIN":self.firebase_admin,
			"FIREBASE_JS":self.firebase_js,
			"STRIPE": {
				"SECRET_KEY":self.stripe_secret_key,
				"PUBLISHABLE_KEY":self.stripe_publishable_key,
			},
			"EMAIL": {
				"ADDRESS":self.email_address,
				"PASSWORD":self.email_password,
			},
			"AES_PASSPHRASE":self.aes_passphrase,
			"NAMECHEAP_USERNAME":self.namecheap_username,
			"NAMECHEAP_API_KEY":self.namecheap_api_key,
			# add these for the settings.py
			"DOMAIN":self.domain,
			"DATABASE":self.database,
			"PRODUCTION":self.production,
			"MAINTENANCE":self.maintenance,
			"LOG_LEVEL":self.log_level,
		})

		# save.
		if save: 
			Files.save(f"{self.root}/__defaults__/env/website", serialized, format="json")


		# return serizaled.
		return serialized

		#
	def init_from_serialized(self, serialized=None):

		# load non secrets.
		if serialized == None:
			serialized = Files.load(f"{self.root}/__defaults__/env/website", format="json")
		#self.root = serialized["root"]
		self.database = serialized["database"]
		self.library = serialized["library"]
		self.name = serialized["name"]
		self.author = serialized["author"]
		self.email = serialized["email"]
		self.city = serialized["city"]
		self.province = serialized["province"]
		self.organization = serialized["organization"]
		self.organization_unit = serialized["organization_unit"]
		self.country_code = serialized["country_code"]
		self.domain = serialized["domain"]
		#self.namecheap_username = serialized["namecheap_username"]
		#self.namecheap_api_key = serialized["namecheap_api_key"]
		#self.firebase_admin = serialized["firebase_admin"]
		#self.stripe_secret_key = serialized["stripe_secret_key"]
		#self.stripe_publishable_key = serialized["stripe_publishable_key"]
		#self.email_address = serialized["email_address"]
		#self.email_password = serialized["email_password"]
		self.email_smtp_host = serialized["email_smtp_host"]
		self.email_smtp_port = serialized["email_smtp_port"]
		self.purchase_tls_certificate = serialized["purchase_tls_certificate"]
		self.stripe_subscriptions = serialized["stripe_subscriptions"]
		self.stripe_products = serialized["stripe_products"]
		self.developers = serialized["developers"]
		self.remote = serialized['remote']
		self.vps_ip = serialized["vps_ip"]
		self.vps_port = serialized["vps_port"]
		self.vps_username = serialized["vps_username"]
		self._2fa = serialized["_2fa"]
		self.firebase_enabled = serialized["firebase_enabled"]
		self.stripe_enabled = serialized["stripe_enabled"]
		self.namecheap_enabled = serialized["namecheap_enabled"]
		self.email_enabled = serialized["email_enabled"]
		self.log_level = serialized["log_level"]
		self.users_subpath = serialized["users_subpath"]
		self.id_by_username = serialized["id_by_username"]
		self.styling = serialized["styling"]

		# load secrets.
		local_security = security.Security(
			# the root path.
			root=self.root,)
		required = False
		migrations = Environment.get("MIGRATIONS", format=bool, default=False)
		if self.firebase_enabled and not migrations: required = True
		self.firebase_admin = {
			"type":local_security.get_secret_env("FIREBASE_ADMIN_"+"type".upper(), default=None, required=required),
			"project_id":local_security.get_secret_env("FIREBASE_ADMIN_"+"project_id".upper(), default=None, required=required),
			"private_key_id":local_security.get_secret_env("FIREBASE_ADMIN_"+"private_key_id".upper(), default=None, required=required),
			"private_key":local_security.get_secret_env("FIREBASE_ADMIN_"+"private_key".upper(), default=None, required=required),
			"client_email":local_security.get_secret_env("FIREBASE_ADMIN_"+"client_email".upper(), default=None, required=required),
			"client_id":local_security.get_secret_env("FIREBASE_ADMIN_"+"client_id".upper(), default=None, required=required),
			"auth_uri":local_security.get_secret_env("FIREBASE_ADMIN_"+"auth_uri".upper(), default=None, required=required),
			"token_uri":local_security.get_secret_env("FIREBASE_ADMIN_"+"token_uri".upper(), default=None, required=required),
			"auth_provider_x509_cert_url":local_security.get_secret_env("FIREBASE_ADMIN_"+"auth_provider_x509_cert_url".upper(), default=None, required=required),
			"client_x509_cert_url":local_security.get_secret_env("FIREBASE_ADMIN_"+"client_x509_cert_url".upper(), default=None, required=required),
		}
		self.firebase_js = {
			"api_key":local_security.get_secret_env("FIREBASE_JS_"+"API_KEY", default=None, required=required),
			"auth_domain":local_security.get_secret_env("FIREBASE_JS_"+"AUTH_DOMAIN", default=None, required=required),
			"database_url":local_security.get_secret_env("FIREBASE_JS_"+"DATABASE_URL", default=None, required=False),
			"project_id":local_security.get_secret_env("FIREBASE_JS_"+"PROJECT_ID", default=None, required=required),
			"storage_bucket":local_security.get_secret_env("FIREBASE_JS_"+"STORAGE_BUCKET", default=None, required=required),
			"messaging_sender_id":local_security.get_secret_env("FIREBASE_JS_"+"MESSAGING_SENDER_ID", default=None, required=required),
			"app_id":local_security.get_secret_env("FIREBASE_JS_"+"APP_ID", default=None, required=required),
			"measurement_id":local_security.get_secret_env("FIREBASE_JS_"+"MEASUREMENT_ID", default=None, required=False),
		}
		self.stripe_secret_key = local_security.get_secret_env("STRIPE_SECRET_KEY", default=None, required=self.stripe_enabled)
		self.stripe_publishable_key = local_security.get_secret_env("STRIPE_PUBLISHABLE_KEY", default=None, required=self.stripe_enabled)
		self.email_address = local_security.get_secret_env("EMAIL_ADDRESS", default=None, required=self.email_enabled)
		self.email_password = local_security.get_secret_env("EMAIL_PASSWORD", default=None, required=self.email_enabled)
		self.aes_passphrase = local_security.get_secret_env("AES_PASSPHRASE", default=None, required=not migrations)
		self.namecheap_username = local_security.get_secret_env("NAMECHEAP_USERNAME", default=self.namecheap_enabled)
		self.namecheap_api_key = local_security.get_secret_env("NAMECHEAP_API_KEY", default=self.namecheap_enabled)

		# success.
		return True

		#
	def __str__(self, indent=0):
		def __indent__(indent):
			s = ""
			for i in range(indent): s += " "
			return s
		serialized = self.serialize(save=False)
		_serialized_ = {}
		_serialized_["root"] = serialized["root"]
		_serialized_["name"] = serialized["name"]
		_serialized_["email"] = serialized["email"]
		_serialized_["country_code"] = serialized["country_code"]
		_serialized_["city"] = serialized["city"]
		_serialized_["organization"] = serialized["organization"]
		_serialized_["domain"] = serialized["domain"]
		_indent_ = __indent__(indent)
		str = json.dumps(_serialized_, indent=indent).replace('": "', ': ').replace('": ', ': ').replace('",', "").replace(f'\n{_indent_}"', f'\n{_indent_} * ').replace("{\n", "").replace('"\n}', "").replace("\n}", "").replace("{", "")
		return f"<w3bsite.Website; \n{str}\n>"

	def template(self, dictionary={}, update=False):
		new = utils.__append_dict__(new=dictionary, overwrite=True,  old=dict(self.template_data))
		if update:
			self.template_data.dictionary = new
		return new