#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_

# the git object class.
class Git(_defaults_.Defaults):
	def __init__(self,
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

		#
	def installed(self):
		return r3sponse.success_response(f"Successfully checked the installation of git repository [{self.name}].", {
				"installed":os.path.exists(f"{self.root}/.git"),
			})
		#
	def install(self):

		# install git.
		response = utils.__execute_script__(f"""
			cd  {self.root}/
			git init
			git config --global user.name "{self.author}
			git config --global user.email {self.email}
		""")
		if not "Initialized empty Git repository in " in response:
			return r3sponse.error_response(f"Failed to install git repository [{self.name}].")

		# check remote.
		response = utils.__execute_script__(f"""
			cd  {self.root}/
			git remote -v
		""")
		if response == "":
			response = utils.__execute_script__(f"""
				cd  {self.root}/
				heroku create {self.name.lower().replace(" ","")}
			""")
			if not "https://" in response:
				return r3sponse.error_response(f"Failed to create a heroku app while installing git repository [{self.name}],")

			# double check.
			response = utils.__execute_script__(f"""
				cd  {self.root}/
				git remote -v
			""")
			if response == "":
				return r3sponse.error_response(f"Failed to link a remote heroku origin to git repository [{self.name}].")

		return r3sponse.success_response(f"Successfully installed git repository [{self.name}].")

		#
	def pull(self, title="Updates", message="updates."):

		# update git.
		response = utils.__execute_script__(f"""
			cd  {self.root}/
			git pull
			""")
		if True or "initialized empty git re" in response.lower():
			return r3sponse.success_response(f"Successfully pulled git repository [{self.name}].")
		else:
			return r3sponse.error_response(f"Failed to pull git repository [{self.name}].")

		#






