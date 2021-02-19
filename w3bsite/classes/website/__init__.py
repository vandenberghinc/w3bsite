#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import security, heroku, namecheap, utils, git, firebase, users, stripe, logging, rate_limit, aes, deployment, vps, cache, defaults, apps, views

# the main website class.
class Website(cl1.CLI):
	def __init__(self,
		#
		# General.
		# 	the root path (must include version).
		root=None, # example: Formats.FilePath(__file__).base(back=1).replace("./","")
		#
		# Website.
		# 	the root domain.
		domain=None,
		# 	the website name.
		name=None,
		#
		# Deployment.
		# 	remote depoyment, options: [local, vps, heroku].
		remote="local",
		#
		# Developers.
		#	the developer users (emails).
		developers=[],
		#
		# Django.
		#	running the website on django (enable in config.py).
		django=False,
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
		#	the passphrase of the aes master-key.
		aes_master_key=None,
		#
		# Namecheap.
		# 	your namecheap username.
		namecheap_username=None,
		# 	your namecheap api key.
		namecheap_api_key=None,
		#
		# Firebase.
		# 	your firebase admin service account key, (dict) [https://console.firebase.google.com > Service Accounts > Firebase admin].
		firebase_admin={},
		# 	your firebase sdk javascript configuration, (dict) [https://console.firebase.google.com > Settings > General > Web JS SDK].
		firebase_js={},
		#
		# Stripe.
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
		#
		#
		# 
		# optionally initizialize from a serialized dict (for config.py) (still requires parameters: root).
		serialized=None,
	):	

		# w3bsite values.
		self.SOURCE_PATH = SOURCE_PATH
		self.VERSION = VERSION

		# argurments.
		if root != None:
			if root[len(root)-1] != "/": root += "/"
			if root[-3:] == "/./": root = root[:-3]
			if root[len(root)-1] != "/": root += "/"
			root = root.replace("//","/").replace("//","/")
			if firebase_admin != None:
				if isinstance(firebase_admin, str) and firebase_admin[:len(".secrets")] == ".secrets":
					firebase_admin = f"{root}/{firebase_admin}".replace("//","/").replace("//","/")
		self.root = root # root includes version.
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
		self.aes_master_key = aes_master_key
		self.stripe_subscriptions = stripe_subscriptions
		self.stripe_products = stripe_products
		self.developers = developers
		self.remote = remote.lower()
		self.vps_ip = vps_ip
		self.vps_port = vps_port
		self.vps_username = vps_username
		self._2fa = _2fa
		self.template_data = template_data
		# cli only (aka non serialized required) arguments.
		self.prevent_heroku_deployment = prevent_heroku_deployment
		self.interactive = interactive
		self.production = production
		self.maintenance = maintenance
		if self.domain != None:
			self.domain = utils.naked_url(self.domain)
		if serialized == None or serialized == {}:
			self.database = f"/etc/{self.domain}/" # set also over here.
			self.serialize(save=True)
		else:
			if isinstance(serialized, str):
				serialized = utils.__load_json__(serialized)
			self.init_from_serialized(serialized=serialized)
		if self.aes_master_key == None and "--generate-aes" not in sys.argv:
			raise ValueError("Generate a passphrase for the aes master key with [ $ ./website.py --generate-aes] and pass it as the 'aes_master_key' parameter.")
		#if root != syst3m.utils.__execute_script__("pwd").replace("\n",""):
		#	raise ValueError("The ")

		# overall arguments.
		response = r3sponse.check_parameters({
			"root":self.root,
			"name":self.name,
			"author":self.author,
			"email":self.email,
			"city":self.city,
			"province":self.province,
			"organization":self.organization,
			"organization_unit":self.organization_unit,
			"country_code":self.country_code,
			"namecheap_username":self.namecheap_username,
			"namecheap_api_key":self.namecheap_api_key,
			"domain":self.domain,
			"firebase_admin":self.firebase_admin,
			"firebase_js":self.firebase_js,
			"stripe_secret_key":self.stripe_secret_key,
			"stripe_publishable_key":self.stripe_publishable_key,
			"email_address":self.email_address,
			"email_password":self.email_password,
			"email_smtp_host":self.email_smtp_host,
			"email_smtp_port":self.email_smtp_port,
			"stripe_subscriptions":self.stripe_subscriptions,
			"stripe_products":self.stripe_products,
			"developers":self.developers,
			"remote":self.remote,
			"_2fa":self._2fa,
		})
		if not response.success: raise ValueError(response.error)

		# remote: vps arguments.
		if self.remote in ["vps"]:
			response = r3sponse.check_parameters({
				"vps_ip":self.vps_ip,
				"vps_port":self.vps_port,
				"vps_username":self.vps_username,
			})
			if not response.success: raise ValueError(response.error)

		# set variables.
		self.version = Formats.FilePath(self.root).name().replace("/","").replace("/","").replace("/","").replace("/","")
		self.library = f"/usr/local/lib/{self.domain}/"
		self.database = f"/etc/{self.domain}/"
		self.live = utils.equalize_path(self.root, striplast=True) == utils.equalize_path(f"{self.library}/{self.version}", striplast=True)
		self.http_domain = f"http://{self.domain}"
		self.https_domain = f"https://{self.domain}"

		# environment for settings.py.
		os.chdir(self.root)
		secrets = utils.__load_json__(".secrets/env.json")
		os.environ["PRODUCTION"] = str(self.production)
		os.environ["DOMAIN"] = self.domain
		os.environ["DATABASE"] = self.database
		try:
			os.environ["DJANGO_SECRET_KEY"] = secrets["DJANGO_SECRET_KEY"]
		except KeyError: a=1
		os.environ["DJANGO_RUNNING"] = str(django)
		os.environ["leftbar_width"] = "250px"

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
		self.template_data = views.TemplateData(utils.__append_dict__(new=self.template_data, overwrite=True,  old={
			"COLORS":colors,"colors":colors,
			"DOMAIN":self.domain,
			"PRODUCTION":self.production,
			"AUTHOR":self.author,
			"ORGANIZATION":self.organization,
			"STRIPE":{},
			"FIREBASE":{},
		}))

		# defaults objects.
		self.logging = logging.Logging(
			name=self.name,
			root=self.root,)
		self.aes = aes.AES(
			passphrase=self.aes_master_key)
		self.cache = cache.Cache()
		self.defaults = defaults.Defaults(
			root=self.root,
			version=self.version,
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
			template_data=self.template_data,
			aes=self.aes,
			cache=self.cache,
			logging=self.logging,)

		# objects.
		self.security = security.Security(
			defaults=self.defaults,)
		self.firebase = firebase.Firebase(
			key=self.firebase_admin,
			firebase_js=self.firebase_js,
			defaults=self.defaults)
		self.stripe = stripe.Stripe(
			secret_key=self.stripe_secret_key,
			publishable_key=self.stripe_publishable_key,
			subscriptions=self.stripe_subscriptions,
			products=self.stripe_products,
			defaults=self.defaults)
		self.rate_limit = rate_limit.RateLimit(
			firebase=self.firebase,
			defaults=self.defaults,)
		#from django.conf import settings
		#settings.configure()
		lroot = self.root.replace("//","/").replace("//","/").replace("//","/").replace("/",".")
		if lroot[len(lroot)-1] == ".": lroot = lroot[:-1]
		if lroot[0] == ".": lroot = lroot[1:]
		#os.chdir(self.root)
		os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'website.settings')
		#os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{lroot}.website.settings')
		from w3bsite.classes import django
		self.django = django.Django(
			security=self.security,
			defaults=self.defaults,)
		self.users = users.Users(
			email_address=self.email_address,
			email_password=self.email_password,
			smtp_host=self.email_smtp_host,
			smtp_port=self.email_smtp_port,
			firestore=self.firebase.firestore,
			stripe=self.stripe,
			django=self.django,
			defaults=self.defaults,)
		self.namecheap = namecheap.Namecheap(
			username=self.namecheap_username,
			api_key=self.namecheap_api_key,
			sandbox=False,
			defaults=self.defaults,)
		self.git = git.Git(
			defaults=self.defaults,
			)#
		# mode dependend objects.
		self.deployment = None
		self.heroku = None
		self.vps = None
		if self.remote in ["local", "vps"]:
			self.deployment = deployment.Deployment(
				vps_ip=self.vps_ip,
				namecheap=self.namecheap,
				defaults=self.defaults,)
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
		else:
			raise ValueError(f"Selected an invalid remote [{self.remote}], options: [local, vps, heroku]")
		self.apps = apps.Apps(
			rate_limit=self.rate_limit,
			users=self.users,
			stripe=self.stripe,
			defaults=self.defaults,)

		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"Development":"",
				"    --create":"Create the website.",
				"    --create-app dashboard":"Create a new application.",
				"    --start --developer":"Start the production webserver.",
				"Production":"",
				"    --start":"Start the nginx webserver.",
				"    --stop":"Stop the nginx webserver.",
				"    --restart":"Restart the nginx webserver.",
				"    --status":"Retrieve the status of the nginx webserver.",
				"Deployment":"",
				"    --generate-aes":"Generate an aes passphrase.",
				"    --generate-tls":"Generate a tls certificate.",
				"    --activate-tls":"Activate the generated tls certificate.",
				"    --bundle-tls /path/to/downloaded/cert/":"Bundle the downloaded signed certificate from the CA.",
				"    --deploy":"Deploy the website.",
				"Logs":"",
				"    --tail [optional: --nginx]":"Tail the (deployed) website.",
				"Documentation":"",
				"    -h / --help":"Show the documentation.",
			},
			options={
				#"-c":"Do not clear the logs.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		# logs.
		#if not self.argument_present("-c"):
		#	os.system("clear")
		if syst3m.defaults.vars.log_level > 0:
			print(f"Website: {self.name}")
			print(f"Domain: {self.domain}")
			print(f"Root: {self.root}")
			print(f"Library: {self.library}")
			print(f"Database: {self.database}")
			print(f"Remote: {self.remote}")
			print(f"Live: {self.live}")

		#
	def cli(self):

		# help.
		if self.argument_present("-h"):
			print(self.documentation)
			sys.exit(1)

		# developer start.
		elif self.argument_present("--start") and self.argument_present("--developer"):
			response = self.django.start()
			r3sponse.log(response=response)

		# start.
		elif self.argument_present('--start'):
			if not self.live: 
				r3sponse.log(error="The executing library is not live.")
				sys.exit(1)
			syst3m.defaults.operating_system(supported=["linux"])
			command = ""
			for i in ["gunicorn.socket", "gunicorn", "nginx"]:
				command += f"sudo systemctl start {i} &&"
			command = command[:-3]
			output = syst3m.utils.__execute_script__(command)
			if output in ["", "\n"]:
				print(f"Successfully started {self.domain}")
			else:
				print(f"Failed to started {self.domain};\n{output}")

		# stop.
		elif self.argument_present('--stop'):
			if not self.live: 
				r3sponse.log(error="The executing library is not live.")
				sys.exit(1)
			syst3m.defaults.operating_system(supported=["linux"])
			command = ""
			for i in ["gunicorn.socket", "gunicorn", "nginx"]:
				command += f"sudo systemctl stop {i} &&"
			command = command[:-3]
			output = syst3m.utils.__execute_script__(command)
			if output in ["", "\n"]:
				print(f"Successfully stopped {self.domain}")
			else:
				print(f"Failed to stopped {self.domain};\n{output}")

		# restart.
		elif self.argument_present('--restart'):
			if not self.live: 
				r3sponse.log(error="The executing library is not live.")
				sys.exit(1)
			syst3m.defaults.operating_system(supported=["linux"])
			command = ""
			for i in ["gunicorn.socket", "gunicorn", "nginx"]:
				command += f"sudo systemctl restart {i} &&"
			command = command[:-3]
			output = syst3m.utils.__execute_script__(command)
			if output in ["", "\n"]:
				print(f"Successfully restarted {self.domain}")
			else:
				print(f"Failed to restarted {self.domain};\n{output}")

		# status.
		elif self.argument_present('--status'):
			if not self.live: 
				r3sponse.log(error="The executing library is not live.")
				sys.exit(1)
			syst3m.defaults.operating_system(supported=["linux"])
			os.system("sudo systemctl status gunicorn")

		# reset logs.
		elif self.argument_present('--reset-logs'):
			if not self.live: 
				r3sponse.log(error="The executing library is not live.")
				sys.exit(1)
			os.system(f"echo '' > {self.database}/logs/logs.txt")
			r3sponse.log("Successfully resetted the logs.", log_level=0, save=True)

		# tail.
		elif self.argument_present('--tail'):
			if not self.live: 
				r3sponse.log(error="The executing library is not live.")
				sys.exit(1)
			if self.arguments_present(["--nginx", "-n"]):
				if self.arguments_present(["--debug", "-d"]):
					os.system(f"cat /var/log/nginx/{self.domain}.debug")
				else:
					os.system(f"cat /var/log/nginx/{self.domain}")
			else:
				os.system(f"cat {self.database}/logs/logs.txt")

		# deploy.
		elif self.argument_present("--deploy"):
			response = self.deploy(
				code_update=self.get_argument("--code-update", required=False, default=False),
				reinstall=self.get_argument("--reinstall", required=False, default=False),
			)
			r3sponse.log(response=response)

		# generate tls.
		elif self.argument_present("--generate-tls"):
			response = self.deployment.generate_tls()
			r3sponse.log(response=response)

		# activate tls.
		elif self.argument_present("--activate-tls"):
			response = self.deployment.activate_tls()
			r3sponse.log(response=response)

		# bundle tls.
		elif self.argument_present("--bundle-tls"):
			response = self.deployment.bundle_tls(directory=self.get_argument("--bundle-tls"))
			r3sponse.log(response=response)
		
		# create.
		elif self.argument_present("--create"):
			response = self.create()
			r3sponse.log(response=response)

		# create app.
		elif self.argument_present("--create-app"):
			response = self.django.create_app(name=self.get_argument("--create-app"))
			r3sponse.log(response=response)

		# generate aes passphrase.
		elif self.argument_present("--generate-aes"):
			print(f"Generated AES Passphrase: {utils.__generate__(length=64, capitalize=True, digits=True)}")

		# invalid.
		else:
			print(self.documentation)
			print("Selected an invalid mode.")
			sys.exit(1)

		#
	def deploy(self, code_update=False, reinstall=False, log_level=0):

		# check git.
		loader = syst3m.console.Loader("Checking git repository ...")
		response = self.git.installed()
		if not response.success: 
			loader.stop(success=False)
			return response
		elif not response["installed"]:
			loader.stop()
			loader = syst3m.console.Loader("Installing git repository ...")
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
			return r3sponse.success_response(f"Successfully deployed website https://{self.domain}.")
		else:
			return r3sponse.success_response(f"Successfully deployed the code updates of website https://{self.domain}.")

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
		return r3sponse.success_response(f"Successfully checked the dns settings of website [{self.name}].", log_level=log_level)

		#
	def create(self):

		# create root.
		if not os.path.exists(self.root):
			#return r3sponse.error_response(f"Website [{self.root}] already exists.")
			os.mkdir(self.root)

		# create django.
		loader = syst3m.console.Loader("Creating website ...")
		response = self.django.create()
		loader.stop(success=response["success"])
		if response.error != None: return response

		# generate tls.
		loader = syst3m.console.Loader("Generating tls ...")
		response = self.security.generate_tls()
		loader.stop(success=response["success"])
		if response.error != None: return response

		# handlers.
		return r3sponse.success_response(f"Successfully created website [{self.name}].")

		#
	def serialize(self, save=False):
		# serizalized is used by the config.py in deployment.
		# all non secret variables are stored in website.json inside the root/. directory .
		# all secret variables are stored in environment variables from env.sh & env.json.
		# all keys of the stored secrets are stored in the serialzed website.json.

		# serialize and save all non secret variables in the website.json.
		serialized = {
			"root":self.root,
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
			"AES_MASTER_KEY":self.aes_master_key,
			"NAMECHEAP_USERNAME":self.namecheap_username,
			"NAMECHEAP_API_KEY":self.namecheap_api_key,
			# add these for the settings.py
			"DOMAIN":self.domain,
			"DATABASE":self.database,
			"PRODUCTION":self.production,
			"MAINTENANCE":self.maintenance,
			"LOG_LEVEL":LOG_LEVEL,
		})

		# save.
		if save: 
			utils.__save_json__(f"{self.root}/website.json", serialized)


		# return serizaled.
		return serialized

		#
	def init_from_serialized(self, serialized=None):

		# load non secrets.
		if serialized == None:
			serialized = utils.__load_json__(f"{self.root}/website.json")
		#self.root = serialized["root"]
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


		# load secrets.
		local_security = security.Security(
			# the root path.
			root=self.root,)
		self.firebase_admin = {
			"type":local_security.get_secret_env("FIREBASE_ADMIN_"+"type".upper(), default=None),
			"project_id":local_security.get_secret_env("FIREBASE_ADMIN_"+"project_id".upper(), default=None),
			"private_key_id":local_security.get_secret_env("FIREBASE_ADMIN_"+"private_key_id".upper(), default=None),
			"private_key":local_security.get_secret_env("FIREBASE_ADMIN_"+"private_key".upper(), default=None),
			"client_email":local_security.get_secret_env("FIREBASE_ADMIN_"+"client_email".upper(), default=None),
			"client_id":local_security.get_secret_env("FIREBASE_ADMIN_"+"client_id".upper(), default=None),
			"auth_uri":local_security.get_secret_env("FIREBASE_ADMIN_"+"auth_uri".upper(), default=None),
			"token_uri":local_security.get_secret_env("FIREBASE_ADMIN_"+"token_uri".upper(), default=None),
			"auth_provider_x509_cert_url":local_security.get_secret_env("FIREBASE_ADMIN_"+"auth_provider_x509_cert_url".upper(), default=None),
			"client_x509_cert_url":local_security.get_secret_env("FIREBASE_ADMIN_"+"client_x509_cert_url".upper(), default=None),
		}
		self.firebase_js = {
			"api_key":syst3m.env.get_string("FIREBASE_JS_"+"API_KEY", default=None),
			"auth_domain":syst3m.env.get_string("FIREBASE_JS_"+"AUTH_DOMAIN", default=None),
			"database_url":syst3m.env.get_string("FIREBASE_JS_"+"DATABASE_URL", default=None),
			"project_id":syst3m.env.get_string("FIREBASE_JS_"+"PROJECT_ID", default=None),
			"storage_bucket":syst3m.env.get_string("FIREBASE_JS_"+"STORAGE_BUCKET", default=None),
			"messaging_sender_id":syst3m.env.get_string("FIREBASE_JS_"+"MESSAGING_SENDER_ID", default=None),
			"app_id":syst3m.env.get_string("FIREBASE_JS_"+"APP_ID", default=None),
			"measurement_id":syst3m.env.get_string("FIREBASE_JS_"+"MEASUREMENT_ID", default=None),
		}
		self.stripe_secret_key = local_security.get_secret_env("STRIPE_SECRET_KEY", default=None)
		self.stripe_publishable_key = local_security.get_secret_env("STRIPE_PUBLISHABLE_KEY", default=None)
		self.email_address = local_security.get_secret_env("EMAIL_ADDRESS", default=None)
		self.email_password = local_security.get_secret_env("EMAIL_PASSWORD", default=None)
		self.aes_master_key = local_security.get_secret_env("AES_MASTER_KEY", default=None)
		self.namecheap_username = local_security.get_secret_env("NAMECHEAP_USERNAME", default=None)
		self.namecheap_api_key = local_security.get_secret_env("NAMECHEAP_API_KEY", default=None)

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
