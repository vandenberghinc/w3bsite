#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils

# check installation.
"""
if os.environ.get("DJANGO_SECRET_KEY") == None and not Files.exists("/usr/local/bin/heroku"):
	if OS in ["macos"]:
		os.system("brew tap heroku/brew && brew install heroku")
	else:
		os.system("curl https://cli-assets.heroku.com/install.sh | sh")
	if not Files.exists("/usr/local/bin/heroku"):
		raise ImportError("Failed to install the heroku cli.")
"""

# the heroku object class.
class Heroku(object):
	def __init__(self, 
		# the root path.
		root=None,
		# the domain.
		doman=None,
		# the website name.
		name=None,
		# passed objects.
		namecheap=None,
	):

		# docs.
		DOCS = {
			"module":"website.heroku", 
			"initialized":True,
			"description":[], 
			"chapter": "Deployment", }

		# arguments.
		self.root = root
		self.domain = domain
		self.sub_domain = sub_domain
		self.name = name
		self.namecheap = namecheap
		response = self.check_logged_in()
		if response.error != None: raise RuntimeError(response.error)

		#
	# x.
	def check(self):
		os.system("cd "+self.root+"/" + " && " + "heroku ps:scale web=1" + " && " + "./manage.py makemigrations" + " && " + "./manage.py migrate")
	def tail(self):
		os.system("cd "+self.root+"/" + " && " + "heroku logs --tail")
	def add_environment_variables(self, variables={}, silent=True):
		c = "cd "+self.root+"/"
		c += " && heroku config:set"
		for key, value in variables.items():
			c += " {}='{}'".format(key, str(value).replace("\n","\\n"))
		output = utils.__execute_script__(c)
		success = True
		for key, _ in variables.items():
			if key+":" not in output: success = False ; break
		if success:
			return dev0s.response.success("Success")
		else:
			return dev0s.response.error(f"Error, output: {output}")
	def remove_environment_variables(self, variables={}):
		c = "cd "+self.root+"/"
		for key, value in variables.items():
			c += "&&" + f"heroku config:unset {key}"
		output = utils.__execute_script__(c)
		print(output)
	def get_environment_variables(self, variables={}):
		c = "cd "+self.root+"/"
		for key, value in variables.items():
			c += "&&" + f"heroku config:get {key}"
		output = utils.__execute_script__(c)
		print(output)
	# x.
	def push(self, log_level=0):
		output = utils.__execute_script__(f"""
		cd {self.root}/ && 
		git add . && 
		git commit -am 'automatic updates' && 
		git push heroku master
		""", silent=log_level!=0)
		if "Verifying deploy... done." in output:
			return dev0s.response.success(f"Successfully pushed website [{self.root}] to heroku.")
		elif "Everything up-to-date" in output or "nothing to commit, working tree clean" in output:
			return dev0s.response.error(f"Website [{self.root}] is already up to date.")
		else:
			return dev0s.response.error(f"Failed to push website [{self.root}] to heroku.")
	def get_deploy_app(self):

		# variables.
		domains = {}

		# get.
		output = utils.__execute_script__(f"""
			cd {self.root}/
			heroku domains
		""", return_format="array")

		# iterate.
		app, mode, domain = None, None, None
		new = False
		for line in output:
			if line not in ["", " "]:

				# set app and mode.
				if line[:len("=== ")] == "=== ":
					l_app = line.split("=== ")[1].split(" ")[0]
					mode = line.split(f"=== {l_app} ")[1].split("\n")[0]
					try: domains[l_app]
					except KeyError: domains[l_app] = {}
					if app == None:
						app = str(l_app)
					elif mode == "Heroku Domain":
						return dev0s.response.error(f"Detected multiple heroku apps for project [{self.root}].")				

				
		# handlers.
		return dev0s.response.success(f"Successfully retrieved the heroku app name of project [{self.root}].", {"app":app})

		#
	def get_deploy_domain(self,
		# the heroku app name (optional to increase speed).
		app=None,
	):

		# get info.
		if app == None:
			response = self.get_deploy_app()
			if response.error != None: return response
			app = response["app"]
		response = self.get_domains()
		if response.error != None: return response

		# handlers.
		try:
			dict = response["domains"][app]
		except KeyError:
			return dev0s.response.error(f"Unable to find heroku app [{app}] from project [{self.root}.")
		if len(dict) == 0:
			return dev0s.response.error(f"Unable to find any heroku domains for heroku app [{app}] from project [{self.root}].")
		elif len(dict) > 1:
			return dev0s.response.error(f"Found multiple heroku domains for heroku app [{app}] from project [{self.root}].")
		else:
			return dev0s.response.success(f"Successfully found the deploy domain for project [{self.root}].", {
				"domain":list(dict.keys())[0]
			})

		#
	def get_domains(self):

		# variables.
		domains = {}

		# get.
		output = utils.__execute_script__(f"""
			cd {self.root}/
			heroku domains
		""", return_format="array")

		# iterate.
		app, mode, domain = None, None, None
		for line in output:
			if line not in ["", " "]:

				# set app and mode.
				if line[:len("=== ")] == "=== ":
					app = line.split("=== ")[1].split(" ")[0]
					mode = line.split(f"=== {app} ")[1].split("\n")[0]
					try: domains[app]
					except KeyError: domains[app] = {}
				
				# by mode.
				elif mode == "Heroku Domain":
					domain = line.split('\n')[0]
					try: domains[app][domain]
					except KeyError: domains[app][domain] = {}
				elif mode == "Custom Domains":
					if "Domain Name" not in line and "DNS" not in line and "Record Type" not in line and "Target" not in line:
						custom_domain = line.split(" ")[0]
						for i in range(101):
							if "  " not in line: break
							line = line.replace("  "," ")
						if line[len(line)-1] == " ": line = line[:-1]
						target = line.split(" ")[len(line.split(" "))-1]
						if target[len(target)-1] == ".": target = target[:-1]
						domains[app][domain][custom_domain] = target

		# handlers.
		return dev0s.response.success(f"Successfully retrieved the heroku domains of project [{self.root}].", {"domains":domains})

		#
	def check_domain(self, domain=None):
		# set default domain.
		if domain == None: domain = self.domain
		response = self.get_domains()
		if response.error != None: return response
		match = False
		for app, info in response["domains"].items():
			for heroku_domain, info_i in info.items():
				for _domain_, target in info_i.items():
					if _domain_ == domain:
						match = True
						break
		return dev0s.response.success(f"Successfully checked the existance of domain [{domain}].", {"exists":match})
	def add_domain(self, domain=None):

		# set default domain.
		if domain == None: domain = self.domain

		# check duplicates.
		response = self.check_domain(domain)
		if response.error != None: return response
		elif response["exists"]:
			return dev0s.response.error(f"Domain [{domain}] is already added to heroku project [{self.root}].")

		# add.
		output = utils.__execute_script__(f"""
			cd {self.root}
			heroku domains:add {domain}
		""", return_format="array")

		# check existsnce.
		response = self.check_domain(domain)
		if response.error != None: return response
		elif response["exists"]:
			return dev0s.response.success(f"Successfully added domain [{domain}] to heroku project [{self.root}].")
		else:
			return dev0s.response.error(f"Failed to add domain [{domain}] to heroku project [{self.root}].")

		#
	def check_logged_in(self):
		output = utils.__execute_script__(f"""
			cd {self.root}
			heroku auth:whoami
		""")
		if "Error: not logged in" in output:
			return dev0s.response.error("The heroku cli is not signed in. Open a terminal and execute the following command to login: [ $ heroku login].")
		else:
			return dev0s.response.success("The heroku cli is Successfully signed in.")

		#	
	def install_tls(self,
		# the heroku app name (optional to increase speed).
		app=None,
	):
		#source: https://www.namecheap.com/support/knowledgebase/article.aspx/9756/33/installing-an-ssl-certificate-on-heroku-paid-ssl-endpoint

		# get app name.
		if app == None:
			response = self.get_deploy_app()
			if response.error != None: return response
			app = response["app"]

		# add.
		output = utils.__execute_script__(f"""
			cd {self.root}
			heroku certs:add __defaults__/tls/server.crt __defaults__/tls/server.key
		""")

		# update.
		if "try certs:update instead" in output:
			output = utils.__execute_script__(f"""
				cd {self.root}
				heroku certs:update --confirm {app} __defaults__/tls/server.crt __defaults__/tls/server.key
			""")

		# handlers.
		if "Your certificate has been added successfully." in output or ("Updating SSL certificate " in output and "... done" in output):
			return dev0s.response.success(f"Successfully installed the tls certificate of domain [{domain}].")
		else:
			return dev0s.response.error(f"Failed to install the tls certificate of domain [{domain}].")
	def check_dns(self, log_level=0):

		# check heroku (sub) domains.
		domains = [self.domain]
		for domain in domains:
			response = self.check_domain(domain)
			if response.error != None: 
				dev0s.response.log(response=response, log_level=log_level)
				return response
			elif not response["exists"]:
				loader = dev0s.console.Loader(f"Adding domain [{domain}].")
				response = self.add_domain(domain)
				loader.stop(response=response)
				if response.error != None: 
					dev0s.response.log(response=response, log_level=log_level)
					return response

		# get heroku app.
		response = self.get_domains()
		if response.error != None: 
			dev0s.response.log(response=response, log_level=log_level)
			return response
		heroku_domains = response["domains"]

		# get heroku app.
		response = self.get_deploy_app()
		if response.error != None: 
			dev0s.response.log(response=response, log_level=log_level)
			return response
		app = response["app"]
		print(f"Heroku deploy app: {app}")

		# get heroku deploy domain.
		response = self.get_deploy_domain(app=app)
		if response.error != None: 
			dev0s.response.log(response=response, log_level=log_level)
			return response
		deploy_domain = response["domain"]
		print(f"Heroku deploy domain: {deploy_domain}")

		# check dns settings.
		for domain in domains:

			# check namecheap domain.
			response = self.namecheap.check_domain(domain)
			if response.error != None: 
				dev0s.response.log(response=response, log_level=log_level)
				return response
			elif not response["exists"]:
				return dev0s.response.error(f"Specified domain [{domain}] is not owned by namecheap user [{self.namecheap.username}].", log_level=log_level)

			# get dns target.
			try:
				target = heroku_domains[app][deploy_domain][domain]
			except KeyError:
				return dev0s.response.error(f"Specified domain [{domain}] is not added to the domains of heroku app [{app}] from project [{self.name}].", log_level=log_level)
			print(f"Heroku DNS target: {target}")

			# add dns records.
			response = self.namecheap.add_dns(
				# the domain (optional).
				domain=domain,
				# the dns record type,
				type="CNAME",
				# the dns record host,
				host="www",
				# the dns record value/address,
				value=target,
				# the get_dns.dns dictionary (optionally to increase speed).
				records=None,)
			if response.error != None and "] already exists." not in response.error: 
				dev0s.response.log(response=response, log_level=log_level)
				return response
			elif response.error == None: 
				dev0s.response.log(response=response, log_level=log_level)
			response = self.namecheap.add_dns(
				# the domain (optional).
				domain=domain,
				# the dns record type,
				type="ALIAS",
				# the dns record host,
				host="@",
				# the dns record value/address,
				value=target,
				# the get_dns.dns dictionary (optionally to increase speed).
				records=None,)
			if response.error != None and "] already exists." not in response.error: 
				dev0s.response.log(response=response, log_level=log_level)
				return response
			elif response.error == None: 
				dev0s.response.log(response=response, log_level=log_level)
		
		# handlers.
		return dev0s.response.success(f"Successfully checked the heroku dns settings for domain {self.domain}.", log_level=log_level)

		#
	def deploy(self, log_level=0):

		# set heroku env.
		loader = dev0s.console.Loader("Configuring heroku environment ...")
		response = self.add_environment_variables(variables=utils.__load_json__(f"{self.root}/__defaults__/env/json"))
		if not response.success: 
			loader.stop(success=False)
			return response
		loader.stop()

		# push to heroku.
		loader = dev0s.console.Loader("Pushing to heroku ...")
		response = self.push(log_level=log_level)
		if response.error != None and "] is already up to date." not in response.error: 
			loader.stop(success=False)
			return response
		elif response.error == None:
			loader.stop()
			dev0s.response.log(response=response, log_level=log_level)

		# handlers.
		return dev0s.response.success(f"Successfully deployed website {self.domain} on heroku.", log_level=log_level)

		#

#