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

		# docs.
		DOCS = {
			"module":"website.git", 
			"initialized":True,
			"description":[], 
			"chapter": "Deployment", }

		# defaults.
		_defaults_.Defaults.__init__(self, traceback="w3bsite.Website.git",)
		self.assign(defaults.dict())

		# arguments.
		# ...

		#
	def installed(self):
		return dev0s.response.success(f"Successfully checked the installation of git repository [{self.name}].", {
				"installed":Files.exists(f"{self.root}/.git"),
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
			return dev0s.response.error(f"Failed to install git repository [{self.name}].")

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
				return dev0s.response.error(f"Failed to create a heroku app while installing git repository [{self.name}],")

			# double check.
			response = utils.__execute_script__(f"""
				cd  {self.root}/
				git remote -v
			""")
			if response == "":
				return dev0s.response.error(f"Failed to link a remote heroku origin to git repository [{self.name}].")

		return dev0s.response.success(f"Successfully installed git repository [{self.name}].")

		#
	def pull(self, title="Updates", message="updates."):

		# update git.
		response = utils.__execute_script__(f"""
			cd  {self.root}/
			git pull
			""")
		if True or "initialized empty git re" in response.lower():
			return dev0s.response.success(f"Successfully pulled git repository [{self.name}].")
		else:
			return dev0s.response.error(f"Failed to pull git repository [{self.name}].")

		#






