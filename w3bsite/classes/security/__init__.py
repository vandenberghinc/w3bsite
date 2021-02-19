#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_

# the security class.
class Security(_defaults_.Defaults):
	def __init__(self,
		# optional if defaults not initialized.
		root=None,
		# defaults (optional).
		defaults=None,
	):	
		
		# defaults.
		if defaults != None:
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
		else:
			self.root = root

		# check arguments.
		#response = r3sponse.check_parameters({
		#	#"ip":ip,
		#})
		#if not response.success: raise ValueError(response)
		
		# arguments.
		# ...

		#
	def generate_tls(self):
		# https://devcenter.heroku.com/articles/acquiring-an-ssl-certificate

		# check base.
		base = f"{self.root}/.secrets/"
		if not os.path.exists(base): os.mkdir(base)
		base = f"{self.root}/.secrets/tls"
		if not os.path.exists(base): os.mkdir(base)

		# check duplicate.
		if os.path.exists(f"{base}/tls.key") or os.path.exists(f"{base}/server.crt"):
			return r3sponse.error_response("The tls certificate already exists.")

		# generate.
		print("Generating a tls certificate ...")
		output = utils.__execute_script__(f"""
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
			os.system(f"rm -fr {base}")
			return r3sponse.error_response(f"Failed to generate a tls certificate.")
		else:
			return r3sponse.success_response(f"Successfully generated a tls certificate.")

		#
	def set_secret_env(self, key, value):
		# env.json
		if not os.path.exists(f"{self.root}/.secrets"): os.mkdir(f"{self.root}/.secrets")
		try:
			env = utils.__load_json__(f"{self.root}/.secrets/env.json")
		except FileNotFoundError:
			env = {}
		splitted = key.split(".") ; c, m = 0, len(splitted)
		if m == 1:
			env[key] = value
		else:
			previous = ["Start with null at 0 index to keep c-1."]
			for s in splitted:
				c += 1
				if c == 1:
					try:
						if not isinstance(env[s], dict):
							raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
					except KeyError:
						env[s] = {}
				elif c == 2:
					if c == m:	env[previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-1]][s] = {}
				elif c == 3:
					if c == m:	env[previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-2]][previous[c-1]][s] = {}
				elif c == 4:
					if c == m:	env[previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				elif c == 5:
					if c == m:	env[previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				elif c == 6:
					if c == m:	env[previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				elif c == 7:
					if c == m:	env[previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				elif c == 8:
					if c == m:	env[previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				elif c == 9:
					if c == m:	env[previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				elif c == 10:
					if c == m:	env[previous[c-9]][previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-9]][previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-9]][previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				elif c == 11:
					if c == m:	env[previous[c-10]][previous[c-9]][previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = value
					else:		
						try:
							if not isinstance(env[previous[c-10]][previous[c-9]][previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s], dict):
								raise ValueError(f"The specified key [{key}] can not be stored since there is already a different variable in the env.json with key [{s}] that is not a dictionary.")
						except KeyError:
							env[previous[c-10]][previous[c-9]][previous[c-8]][previous[c-7]][previous[c-6]][previous[c-5]][previous[c-4]][previous[c-3]][previous[c-2]][previous[c-1]][s] = {}
				else:
					raise ValueError(f"Reached max recursive depth with key [{key}].")
				previous.append(s)
		utils.__save_json__(f"{self.root}/.secrets/env.json", env)
		# env.sh
		try:
			env = utils.__load_file__(f"{self.root}/.secrets/env.sh")
		except FileNotFoundError:
			env = ""
		l_key = key.replace(".","-")
		replaced_value = value.replace("\n", "\\n")
		if f'export {l_key}=' in env:
			_env_ = ""
			for line in env.split("\n"):
				if f'export {l_key}=' in line:
					_env_ += f'\nexport {l_key}="{replaced_value}"'
				else:
					_env_ += line+"\n"
		else:
			env += f'\nexport {l_key}="{replaced_value}"'
		for i in range(100):
			if "\n\n" in env: env = env.replace("\n\n","\n")
			else: break
		utils.__save_file__(f"{self.root}/.secrets/env.sh", env)
		return r3sponse.success_response(f"Successfully setted the secret environment variable [{key}].")
	def get_secret_env(self, key, default=None):
		value = syst3m.env.get_string(key, default=default)
		if value == "None": value = None
		if value == None: raise ValueError(f"Secret enironment variable [{key}] is undefined.")
		if "\\n" in value: value = value.replace("\\n", "\n")
		return value