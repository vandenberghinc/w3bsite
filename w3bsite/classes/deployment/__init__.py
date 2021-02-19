#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_

# the deployment object class.
class Deployment(_defaults_.Defaults):
	# deploy the website on a local ubuntu machine.
	def __init__(self,
		# the vps ip (if remote is vps else leave default).
		vps_ip=None,
		# objects.
		namecheap=None,
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
		self.vps_ip = vps_ip

		# objects.
		self.namecheap = namecheap

		#
	# configure also for remove:vps & remote:local.
	def configure(self, reinstall=False, log_level=0):
		
		# configure before loader.
		if reinstall:
			os.system(f"rm -fr {self.root}/.secrets/tls/dhparam.pem")
		if not os.path.exists(f"{self.root}/.secrets/tls/dhparam.pem"):
			tmp = "/tmp/dhparam.pem"
			os.system(f"sudo openssl dhparam -out {tmp} 4096 && sudo chown {USER}:{GROUP} {tmp} && mv {tmp} {self.root}/.secrets/tls/dhparam.pem")

		# loader.
		if log_level >= 0: loader = syst3m.console.Loader(f"Configuring deployment of website {self.domain} ...")

		# check remote.
		if self.remote in ["heroku"]:
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"You can not execute function <Website.deployment.configure> with remote [{self.remote}].")

		# os.
		if OS not in ["macos", "linux"]: 
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"Unsupported operating system [{OS}].")

		# requirements.
		if not os.path.exists(f"{self.root}/requirements"): os.mkdir(f"{self.root}/requirements")
		if not os.path.exists(f"{self.root}/requirements/requirements.pip"): 
			syst3m.utils.__save_file__(f"{self.root}/requirements/requirements.pip", "wheel\nuwsgi\ngunicorn\nwhitenoise\ndjango\npsycopg2-binary\nsyst3m\nw3bsite\ncl1")
		if not os.path.exists(f"{self.root}/requirements/installer"): 
			os.system(f"cp {SOURCE_PATH}/example/requirements/installer {self.root}/requirements/installer && chmod +x {self.root}/requirements/installer")

		# favicon.
		if not os.path.exists(f"{self.root}/static/favicon.ico"):
			output = syst3m.utils.__execute_script__(f"curl https://raw.githubusercontent.com/vandenberghinc/public-storage/master/w3bsite/favicon.ico -o {self.root}/static/favicon.ico")

		# tls.
		if not os.path.exists(f"{self.root}/.secrets/tls/server.key") and not os.path.exists(f"{self.root}/.secrets/tls/server.crt"):
			response = self.generate_tls(log_level=log_level)
			if not response.success: 
				if log_level >= 0: loader.stop(success=False)
				return response

		# deployment.
		if not os.path.exists(f"{self.root}/deployment"): os.mkdir(f"{self.root}/deployment")
		clean_root = f"{self.library}/{self.version}" # <== note the library change instead of root.
		replacements = {
			"***ROOT***":clean_root, 
			"***DOMAIN***":self.domain,
			"***DATABASE***":self.database,
			"***USER***":USER,
		}
		for path in Files.Directory(path=f"{SOURCE_PATH}/classes/deployment/lib/").paths():
			name = Formats.FilePath(path).name()
			try:
				data = syst3m.utils.__load_file__(path)
			except FileNotFoundError:
				data = ""
			new_data = str(data)
			for key,value in replacements.items():
				new_data = new_data.replace(key, value)
			syst3m.utils.__save_file__(f"{self.root}/deployment/{name}", new_data)
		
		# success.
		if log_level >= 0: loader.stop()
		return r3sponse.success_response(f"Successfully configured the deployment of domain {self.domain}.")

		#
	# deploy is for remote:local only. 
	def deploy(self, code_update=False, reinstall=False, log_level=0):
			
		# loader.
		if log_level >= 0: loader = syst3m.console.Loader(f"Deploying domain {self.domain} ...")

		# check namecheap domain.
		if not (self.remote in ["vps"] and self.live):
			response = self.namecheap.check_domain(self.namecheap.post_domain)
			if response.error != None: 
				if log_level >= 0: loader.stop(success=False)
				r3sponse.log(response=response, log_level=log_level)
				return response
			elif not response["exists"]:
				if log_level >= 0: loader.stop(success=False)
				return r3sponse.error_response(f"Specified domain [{self.namecheap.post_domain}] is not owned by namecheap user [{self.namecheap.username}].", log_level=log_level)

		# check remote.
		if self.remote in ["vps"] and not self.live:
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"You can not execute function <Website.deployment.deploy> with remote [{self.remote}].")

		# os.
		if OS not in ["linux"]: 
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"Unsupported operating system [{OS}].")
		
		# configure.
		response = self.configure(reinstall=reinstall, log_level=log_level)
		if not response.success: 
			if log_level >= 0: loader.stop(quiet=True)
			return response

		# check tls domain.
		if not os.path.exists(f"{self.root}/.secrets/tls/.domain"): syst3m.utils.__save_file__(f"{self.root}/.secrets/tls/.domain", self.domain)
		tls_domain = syst3m.utils.__load_file__(f"{self.root}/.secrets/tls/.domain").replace('\n',"")
		if tls_domain != self.domain:
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"TLS Certificate mis match. Installed tls certificate [{self.root}/.secrets/tls] is linked to domain {tls_domain}, not specified domain {self.domain}.", log_level=0)
		
		# checks.
		if not os.path.exists(f"{self.root}/.secrets/tls/server.key") or not os.path.exists(f"{self.root}/.secrets/tls/server.crt"):
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response("No tls certificate exists.\nExecute the following command to generate a tls certificate:\n$ ./website.py --generate-tls", log_level=log_level)
		if not os.path.exists(f"{self.root}/.secrets/tls/signed.server.crt"):
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response("No activated tls certificate exists. \nExecute the following command to activate the generated tls certificate:\n$ ./website.py --activate-tls", log_level=log_level)
		if not os.path.exists(f"{self.root}/.secrets/tls/server.ca-bundle"):
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response("No bundled tls certificate exists. \nDownload the signed certificate send to your email, extr the zip to a directory and execute \n$ ./website.py --bundle-tls /path/to/extracted/directory/", log_level=log_level)
		
		# arguments.
		arguments = ""
		if code_update: arguments += " --code-update"
		if reinstall: arguments += " --reinstall"
		
		# execute & handle.
		os.system(f"chmod +x {self.root}/deployment/installer")
		output = syst3m.utils.__execute_script__(f"bash {self.root}/deployment/installer{arguments}").replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n')
		if "Error:" in output or ("nginx: the configuration file /etc/nginx/nginx.conf syntax is ok" not in output and "nginx: configuration file /etc/nginx/nginx.conf test is successful" not in output): #"Successfully deployed domain " not in output
			print(output)
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"Failed to deploy website {self.domain}.", log_level=log_level)
		else:
			if log_level >= 0: loader.stop()
			return r3sponse.success_response(f"Successfully deployed domain https://{self.domain}.", log_level=log_level)

		#
	def generate_tls(self, log_level=0):
		# https://devcenter.heroku.com/articles/acquiring-an-ssl-certificate

		# check base.
		base = f"{self.root}/.secrets/"
		if not os.path.exists(base): os.mkdir(base)
		base = f"{self.root}/.secrets/tls"
		if not os.path.exists(base): os.mkdir(base)

		# check duplicate.
		if os.path.exists(f"{self.root}/.secrets/tls/server.key") or os.path.exists(f"{self.root}/.secrets/tls/server.crt"):
			return r3sponse.error_response("The tls certificate already exists.", log_level=log_level)

		# generate.
		if log_level >= 0: loader = syst3m.console.Loader("Generating a tls certificate ...")
		output = syst3m.utils.__execute_script__(f"""
			cd {base}

			# Generate a passphrase
			openssl rand -base64 48 > passphrase.txt

			# Generate a Private Key
			openssl genrsa -aes128 -passout file:passphrase.txt -out server.key 4096 # 2048

			# Generate a CSR (Certificate Signing Request)
			openssl req -new -passin file:passphrase.txt -key server.key -out server.csr \
			    -subj "/C={self.country_code}/ST={self.province}/L={self.city}/O={self.organization}/OU={self.organization_unit}/CN={self.domain}/emailAddress={self.email}"

			# Remove Passphrase from Key
			cp server.key server.pass.key
			openssl rsa -in server.pass.key -passin file:passphrase.txt -out server.key

			# Do not self sign.
			# Generating a Self-Signed Certificate for 100 years
			openssl x509 -req -sha256 -days 36500 -in server.csr -signkey server.key -out server.crt

		""")

		# handler.
		if not os.path.exists(f"{self.root}/.secrets/tls/server.key") or not os.path.exists(f"{self.root}/.secrets/tls/server.crt"):
			if log_level >= 0: loader.stop(success=False)
			os.system(f"rm -fr {base}")
			return r3sponse.error_response(f"Failed to generate a tls certificate.", log_level=log_level)
		else:
			if log_level >= 0: loader.stop()
			syst3m.utils.__save_file__(f"{self.root}/.secrets/tls/.domain", self.domain)
			return r3sponse.success_response(f"Successfully generated a tls certificate.", log_level=log_level)

		#
	def activate_tls(self, log_level=0):

		# check existsance.
		if not os.path.exists(f"{self.root}/.secrets/tls/server.key") or not os.path.exists(f"{self.root}/.secrets/tls/server.crt"):
			return r3sponse.error_response("No generated tls certificate exists.", log_level=log_level)

		# check duplicate.
		if os.path.exists(f"{self.root}/.secrets/tls/signed.server.key"):
			return r3sponse.error_response("A signed tls certificate already exists.", log_level=log_level)

		response = self.namecheap.get_tls()
		if response.error != None: 
			r3sponse.log(response=response, log_level=log_level)
			return response
		tls, certificates = response["tls"], response["certificates"]
		
		# check no certificates.
		if certificates == 0:

			# create tls.
			loader = syst3m.console.Loader("Purchasing a namecheap tls certificate ...")
			response = self.namecheap.create_tls(
				# the expiration years.
				years=2,
				# the tls type.
				type="PositiveSSL",)
			r3sponse.log(response=response, log_level=log_level)
			if response.error != None: 
				loader.stop(success=False)
				return response	
			loader.stop()
			
			# get tls again.
			response = self.namecheap.get_tls()
			if response.error != None: 
				loader.stop(success=False)
				r3sponse.log(response=response, log_level=log_level)
				return response
			loader.stop()
			tls, certificates = response["tls"], response["certificates"]

		# check root domain tls.
		tls_activated = False
		for certificate_id, info in tls.items():
			if info["host_name"] == self.domain:
				tls_activated = True
				break
		if not tls_activated:

			# get new purchase certficiate.
			id = None
			for certificate_id, info in tls.items():
				if info["status"] == "newpurchase":
					id = certificate_id
					break

			# create certficiate on no new purchase found.
			if id == None:
				loader = syst3m.console.Loader("Purchasing a namecheap tls certificate ...")
				response = self.namecheap.create_tls(
					# the expiration years.
					years=2,
					# the tls type.
					type="PositiveSSL",)
				r3sponse.log(response=response, log_level=log_level)
				if response.error != None: 
					loader.stop(success=False)
					return response	
				loader.stop()
				id = response["certificate_id"]

			# activate tls for root domain.
			loader = syst3m.console.Loader("Activating tls certificate ...")
			response = self.namecheap.activate_tls(
				# the certificate's id.
				certificate_id=id,)
			loader.stop(success=response["success"])
			r3sponse.log(response=response, log_level=log_level)
			if response.error != None: return response
			
		# handlers.
		return r3sponse.success_response(f"Successfully activated the tls certificate of domain [{self.domain}]. Wait for the CA to send you a .zip file with your signed certificate. Extract the zip & bundle the certificate with: $ ./website.py --bundle-tls /path/to/extracted/directory/certificate/", log_level=log_level)

		#
	def bundle_tls(self, directory, log_level=0):
		
		# check dir.
		if not os.path.exists(directory):
			return r3sponse.error_response(f"Specified directory [{directory}] does not exist.", log_level=log_level)
		if ".zip" in directory:
			return r3sponse.error_response(f"Specified directory [{directory}] is zip format, extract the zip first.", log_level=log_level)
		if not os.path.isdir(directory):
			return r3sponse.error_response(f"Specified directory [{directory}] is not a directory.", log_level=log_level)
		
		# move x.crt to server.crt
		if not os.path.exists(f"{directory}/server.crt") and not os.path.exists(f'{directory}/{self.domain.replace(".","_")}.crt'):
			return r3sponse.success_response(f'You must rename the [{directory}/{self.domain.replace(".","_")}.crt] file manually to [{directory}/server.crt] in order to proceed.', log_level=log_level)
		if not os.path.exists(f"{directory}/server.crt") and os.path.exists(f'{directory}/{self.domain.replace(".","_")}.crt'):
			os.system(f'mv {directory}/{self.domain.replace(".","_")}.crt {directory}/server.crt')
		if not os.path.exists(f"{directory}/server.crt"):
			return r3sponse.success_response(f'Failed to rename the [{directory}/{self.domain.replace(".","_")}.crt] file to [{directory}/server.crt].', log_level=log_level)

		# bundle ca.
		syst3m.utils.__execute_script__(f"""
			cat {directory}/AAACertificateServices.crt {directory}/SectigoRSADomainValidationSecureServerCA.crt {directory}/USERTrustRSAAAACA.crt > {self.root}/.secrets/tls/server.ca-bundle
			cat {directory}/server.crt {self.root}/.secrets/tls/server.ca-bundle > {self.root}/.secrets/tls/signed.server.crt
			mv {self.root}/.secrets/tls/server.crt {self.root}/.secrets/tls/original.server.crt
			cp {self.root}/.secrets/tls/signed.server.crt {self.root}/.secrets/tls/server.crt
			""")
		if os.path.exists(f"{self.root}/.secrets/tls/signed.server.crt"):
			return r3sponse.success_response(f"Successfully bundled ssl certificate [{directory}].", log_level=log_level)
		else:
			return r3sponse.error_response(f"Failed to bundle ssl certificate [{directory}].", log_level=log_level)
	def check_dns(self, log_level=0):

		# loader.
		if log_level >= 0: loader = syst3m.console.Loader(f"Checking dns settings of domain {self.domain} ...")

		# check namecheap domain.
		response = self.namecheap.check_domain(self.namecheap.post_domain)
		if response.error != None: 
			if log_level >= 0: loader.stop(success=False)
			r3sponse.log(response=response, log_level=log_level)
			return response
		elif not response["exists"]:
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"Specified domain [{self.namecheap.post_domain}] is not owned by namecheap user [{self.namecheap.username}].", log_level=log_level)

		# add dns records.
		ip = NETWORK_INFO["public_ip"]
		if self.remote in ["vps"]: ip = self.vps_ip
		host = "@"
		www_host = "www"
		if self.namecheap.pre_domain != "":
			host = self.namecheap.pre_domain
			www_host = f"www.{self.namecheap.pre_domain}"
		response = self.namecheap.add_dns(
			# the domain.
			domain=self.namecheap.post_domain,
			# the dns record type,
			type="A",
			# the dns record host,
			host=www_host,
			# the dns record value/address,
			value=ip,)
		if response.error != None and "] already exists." not in response.error: 
			r3sponse.log(response=response, log_level=log_level)
			if log_level >= 0: loader.stop(success=False)
			return response
		elif response.error == None: 
			r3sponse.log(response=response, log_level=log_level)
		response = self.namecheap.add_dns(
			# the domain.
			domain=self.namecheap.post_domain,
			# the dns record type,
			type="A",
			# the dns record host,
			host=host,
			# the dns record value/address,
			value=ip,)
		if response.error != None and "] already exists." not in response.error: 
			r3sponse.log(response=response, log_level=log_level)
			if log_level >= 0: loader.stop(success=False)
			return response
		elif response.error == None: 
			r3sponse.log(response=response, log_level=log_level)
		
		# handlers.
		if log_level >= 0: loader.stop()
		return r3sponse.success_response(f"Successfully checked the deployment dns settings for domain {self.domain}.", log_level=log_level)

		#

