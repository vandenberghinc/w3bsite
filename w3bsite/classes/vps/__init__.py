
# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_

# the vps object class.
class VPS(_defaults_.Defaults):
	def __init__(self,
		# the remote ip address.
		ip=None,
		# the remote ssh port.
		port=22,
		# the remote username.
		username=None,
		# passed objects.
		namecheap=None,
		deployment=None,
		# defaults.
		defaults=None,

	):	

		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# check arguments.
		response = r3sponse.check_parameters({
			"ip":ip,
			"port":port,
			"username":username,
			"namecheap":namecheap,
			"deployment":deployment,})
		if not response.success: raise ValueError(response.error)
		
		# arguments.
		self.ip = ip
		self.port = port
		self.username = username

		# objects.
		self.deployment = deployment
		self.namecheap = namecheap

		# autocheck.
		response = self.configure(log_level=-1)
		if not r3sponse.success(response) and "VPS is already live in production." not in response.error: raise ValueError(response.error)

		#
	def configure(self, reinstall=False, log_level=0):

		# check already live.
		#if self.live: return r3sponse.error_response("VPS is already live in production.", log_level=log_level)

		# loader.
		if log_level >= 0: loader = syst3m.console.Loader(f"Configuring vps settings of website {self.domain} ...")

		# not live.
		if not self.live:

			# ssh key.
			if not os.path.exists(f"{self.root}/.secrets/ssh"): 
				response = ssht00ls.key.generate(directory=f"{self.root}/.secrets/ssh", comment=f"SSH key for domain {self.domain}", passphrase=None)
				if not r3sponse.success(response): 
					if log_level >= 0: loader.stop(success=False)
					return response

			# ssh config.
			response = ssht00ls.config.create_alias(
				server=self.domain,
				alias=self.domain, 
				username=self.username, 
				ip=self.ip,
				port=self.port,
				key=f"{self.root}/.secrets/ssh/private_key",)
			if not r3sponse.success(response): 
				if log_level >= 0: loader.stop(success=False)
				return response

		# handler.
		if log_level >= 0: loader.stop()
		return r3sponse.success_response("Successfully configured the vps settings.", log_level=log_level)

		#
	def deploy(self, code_update=False, reinstall=False, log_level=0):

		# configure deployment.
		response = self.deployment.configure(reinstall=reinstall, log_level=log_level)
		if not response.success: return response

		# loader.
		if log_level >= 0: loader = syst3m.console.Loader(f"Configuring deployment of website {self.domain} to vps {self.ip} ...")

		# check already live.
		if self.live: 
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response("VPS is already live in production.", log_level=log_level)

		# check installer & requirements file.
		if not os.path.exists(f"{self.root}/requirements/installer"):
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"Required requirements file {self.root}/requirements/installer does not exist.", log_level=log_level)
		if not os.path.exists(f"{self.root}/requirements/requirements.pip"):
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"Required requirements file {self.root}/requirements/requirements.txt does not exist.", log_level=log_level)
		data = syst3m.utils.__load_file__(f"{self.root}/requirements/installer")
		installed_alias = data.split('alias="')[1].split('"')[0]
		#installed_location = data.split('package="')[1].split('"')[0].replace("$alias", installed_alias)
		installed_location = self.library

		# check connection.
		if log_level >= 0: loader.mark(new_message=f"Attempting to connect with vps {self.ip}")
		output = syst3m.utils.__execute_script__(f"printf 'yes\n' | ssh {self.domain} ' echo Hello World ' ").replace('\n\n','\n')
		if "Permission denied (publickey)" in output:
			if log_level >= 0:  loader.stop(success=False)
			data = syst3m.utils.__load_file__(f'{self.root}/.secrets/ssh/public_key').replace('\n','')
			return r3sponse.error_response(f"Unable to connect with {self.domain} over ssh (permission denied). Did you install public key {data} into the vps server?", log_level=log_level)
		elif "Hello World" not in output:
			if log_level >= 0:  loader.stop(success=False)
			return r3sponse.error_response(f"Unable to connect with {self.domain} over ssh, ssh output: \n{output}.", log_level=log_level)

		# installer arguments.
		installer_arguments = ""
		if code_update: installer_arguments += " --code-update"
		if reinstall: installer_arguments += " --reinstall"

		# copy current source to vps & installer script.
		name = Formats.FilePath(self.root).name()
		version = None
		for i in range(100):
			if f"v{i}" in name: 
				version = f"v{i}"
				break
		if version == None:
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response("Unable to find the source version, does the root path include a ../source-name/ version hierarchy? (required)", log_level=log_level)
		base = Formats.FilePath(self.root).base()
		package_name = Formats.FilePath(base).name()
		tmp = f"/tmp/{package_name}"
		s = ""
		for i in [
			f"ssh {self.domain} ' rm -fr {tmp} ' ",
			f"scp -r {base} {self.domain}:{tmp}",
			f"ssh {self.domain} ' chmod +x {tmp}/requirements/installer && bash {tmp}/requirements/installer{installer_arguments} ' ",
		]:
			if s == "": s = i
			else: s += " && "+i
		if log_level >= 0: loader.mark(new_message=f"Installing source code of website {self.domain} on vps {self.ip}")
		output = syst3m.utils.__execute_script__(s).replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n')
		if not "Successfully installed " in output:
			print(output)
			if "Error: " in output:
				if log_level >= 0: loader.stop(success=False)
				return r3sponse.error_response(output.split("Error: ")[1], log_level=log_level)
			else:
				if log_level >= 0: loader.stop(success=False)
				return r3sponse.error_response(f"Failed to deploy website {self.domain} on vps {self.ip}.", log_level=log_level)

		# deploy.
		if log_level >= 0: loader.mark(new_message=f"Deploying domain {self.domain} on vps {self.ip}")
		output = syst3m.utils.__execute_script__(f"ssh {self.domain} ' python3 {installed_location}/website.py --deploy{installer_arguments} ' ").replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n')
		#if f"Deploying domain " in output and f" ... {syst3m.color.red}failed{syst3m.color.end}" in output:
		#	output = output.split(f"Deploying domain {self.domain} ... {syst3m.color.red}failed{syst3m.color.end}")[0]
		if not "Successfully deployed domain https://" in output:
			print(output)
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error_response(f"Failed to deploy website {self.domain} on vps {self.ip}.", log_level=log_level)

		# handler.
		if log_level >= 0: loader.stop()
		return r3sponse.success_response(f"Successfully deployed website {self.domain} on vps {self.ip}.", log_level=log_level)

		#