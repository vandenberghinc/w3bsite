
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
		#response = self.configure(log_level=-1)
		#if not response.success and "VPS is already live in production." not in response.error: raise ValueError(response.error)

		#
	def configure(self, reinstall=False, log_level=0):

		# check already live.
		#if self.live: return r3sponse.error("VPS is already live in production.", log_level=log_level)

		# loader.
		if log_level >= 0: loader = syst3m.console.Loader(f"Configuring vps settings of website {self.domain} ...")

		# not live.
		if not self.live:

			# ssh key.
			if not Files.exists(f"{self.root}/.secrets/ssh"): 
				response = ssht00ls.keys.generate(
					path=f"{self.root}/.secrets/ssh", 
					comment=f"SSH key for domain {self.domain}", 
					passphrase="",)
				if not response.success: 
					if log_level >= 0: loader.stop(success=False)
					return response

			# ssh config.
			response = ssht00ls.aliases.check(
				alias=self.domain, 
				create=True,
				info={
					"username":self.username, 
					"public_ip":self.ip,
					"private_ip":self.ip,
					"public_port":self.port,
					"private_port":self.port,
					"private_key":f"{self.root}/.secrets/ssh/private_key",
					"public_key":f"{self.root}/.secrets/ssh/public_key",
					"passphrase":"",
				})
			if not response.success: 
				if log_level >= 0: loader.stop(success=False)
				return response

		# handler.
		if log_level >= 0: loader.stop()
		return r3sponse.success("Successfully configured the vps settings.", log_level=log_level)

		#
	def deploy(self, code_update=False, reinstall=False, log_level=0):

		# configure vps.
		response = self.configure(reinstall=reinstall, log_level=log_level)
		if not response.success: return response

		# configure deployment.
		response = self.deployment.configure(reinstall=reinstall, log_level=log_level)
		if not response.success: return response

		# loader.
		if log_level >= 0: loader = syst3m.console.Loader(f"Configuring deployment of website {self.domain} to vps {self.ip} ...")

		# check already live.
		if self.live: 
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error("VPS is already live in production.", log_level=log_level)

		# check installer & requirements file.
		if not Files.exists(f"{self.root}/requirements/installer"):
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error(f"Required requirements file {self.root}/requirements/installer does not exist.", log_level=log_level)
		if not Files.exists(f"{self.root}/requirements/requirements.pip"):
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error(f"Required requirements file {self.root}/requirements/requirements.pip does not exist.", log_level=log_level)
		data = Files.load(f"{self.root}/requirements/installer")
		installed_alias = data.split('alias="')[1].split('"')[0]
		#installed_location = data.split('package="')[1].split('"')[0].replace("$alias", installed_alias)
		installed_location = self.library

		# check connection.
		if log_level >= 0: loader.mark(new_message=f"Attempting to connect with vps {self.ip}")
		output = syst3m.utils.__execute_script__(f"printf 'yes\n' | ssh {self.domain} ' echo Hello World ' ").replace('\n\n','\n')
		if "Permission denied (publickey)" in output:
			if log_level >= 0:  loader.stop(success=False)
			data = Files.load(f'{self.root}/.secrets/ssh/public_key').replace('\n','')
			return r3sponse.error(f"Unable to connect with {self.domain} over ssh (permission denied). Did you install public key {data} into the vps server?", log_level=log_level)
		elif "Hello World" not in output:
			if log_level >= 0:  loader.stop(success=False)
			return r3sponse.error(f"Unable to connect with {self.domain} over ssh, ssh output: \n{output}.", log_level=log_level)

		# installer arguments.
		installer_arguments = ""
		if code_update: installer_arguments += " --code-update"
		if reinstall: installer_arguments += " --reinstall"

		# copy current source to vps & installer script.		
		if log_level >= 0: loader.mark(new_message=f"Installing source code of website {self.domain} on vps {self.ip}")
		package_name = gfp.name(path=self.root)
		tmp = f"/tmp/{package_name}/"
		response = ssht00ls.ssync.push(
			alias=self.domain,
			path=self.root,
			remote=tmp,
			checks=False,
			directory=True,
			delete=True,
			check_base=False,)
		if not response.success: 
			if log_level >= 0: loader.stop(success=False)
			return r3sponse.error(f"Failed to deploy website {self.domain} on vps {self.ip}, error: {response.error}.", log_level=log_level)

		# execute installer script.
		if not code_update:
			if log_level >= 0: loader.mark(new_message=f"Executing installer script of website {self.domain} on vps {self.ip}")
			response = ssht00ls.ssh.command(
				alias=self.domain,
				command=f"chmod +x {tmp}/requirements/installer && bash {tmp}/requirements/installer{installer_arguments}",
				log_level=-1,)
			if not response.success: 
				if log_level >= 0: loader.stop(success=False)
				return r3sponse.error(f"Failed to deploy website {self.domain} on vps {self.ip}, error: {response.error}.", log_level=log_level)

			# deploy.
			if log_level >= 0: loader.mark(new_message=f"Deploying domain {self.domain} on vps {self.ip}")
			output = ssht00ls.ssh.command(
				alias=self.domain,
				command=f"python3 {installed_location}/website.py --deploy{installer_arguments} --non-interactive",
				log_level=-1,)
			if not output.success or "Successfully deployed domain https://" not in output:
				#print(response)
				if log_level >= 0: loader.stop(success=False)
				return r3sponse.error(f"Failed to deploy website {self.domain} on vps {self.ip}, error: {output}.", log_level=log_level)

		# handler.
		if log_level >= 0: loader.stop()
		return r3sponse.success(f"Successfully deployed website {self.domain} on vps {self.ip}.", log_level=log_level)

		#