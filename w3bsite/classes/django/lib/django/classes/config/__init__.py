#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# alias.
ALIAS = "vbackups"

# updates.
import os, sys
from dev0s.shortcuts import *
if dev0s.cli.arguments_present(["--update"]) and ALIAS in sys.argv[0]:
	os.system(f"curl -s https://raw.githubusercontent.com/vandenberghinc/{ALIAS}/master/requirements/installer.remote | bash ")
	sys.exit(0)

# imports.
import os, sys, ast, requests, json, glob, subprocess, random, platform, time, socket, time, threading, urllib
from datetime import datetime

# inc imports.
from dev0s.shortcuts import *
from inc_package_manager import inc_package_manager

# source.	
SOURCE = Directory(path=dev0s.defaults.source_path(__file__, back=3))

# checks.
dev0s.defaults.operating_system(supported=["linux", "macos"])
dev0s.defaults.alias(alias=ALIAS, executable=SOURCE.fp.path, venv=SOURCE.join("venv"))

# env settings.
PRODUCTION = dev0s.env.get_boolean("PRODUCTION", default=True)
DAEMON_PRODUCTION = dev0s.env.get_boolean("DAEMON_PRODUCTION", default=True)
MIGRATIONS = dev0s.env.get_boolean("MIGRATIONS", default=False)

# universal variables.
ADMINISTRATOR = "administrator"

# database.
DATABASE = Directory(path=dev0s.env.get_string("VBACKUPS_DATABASE", default=f"{dev0s.defaults.vars.home}/.{ALIAS}"))
if not DATABASE.fp.exists():
	dev0s.response.log(f"{color.orange}Root permission{color.end} required to create {ALIAS} database [{DATABASE}].")
	os.system(f" sudo mkdir -p {DATABASE}")
	Files.chown(str(DATABASE), owner=dev0s.defaults.vars.owner, group=dev0s.defaults.vars.group, sudo=True, recursive=True)
	Files.chmod(str(DATABASE), permission=700, sudo=True, recursive=True)

# ssht00ls.
for dir in [
	SOURCE.join("__defaults__/env"),
	DATABASE.join("keys/ssht00ls"),
]:
	if not Files.exists(dir): Files.create(dir, directory=True)
dev0s.system.env.export(export=[SOURCE.join("__defaults__/env/bash"), SOURCE.join("__defaults__/env/json")], env={
	"INTERACTIVE":False,
	"SSHT00LS_CONFIG":DATABASE.join("keys/ssht00ls/config"),
	"SSHT00LS_PRIVATE_KEY":DATABASE.join("keys/ssht00ls/private_key"),
	"SSHT00LS_PUBLIC_KEY":DATABASE.join("keys/ssht00ls/public_key"),
})
import ssht00ls, w3bsite
from ssht00ls import ssht00ls_agent

# w3bsite.

# variables.
LOG_FILE = f"{DATABASE}/logs/logs"
ERROR_FILE = f"{DATABASE}/logs/errors"
dev0s.response.log_file = LOG_FILE

# config.
CONFIG = Dictionary(path=DATABASE.join("config",""), load=True, default={
})
edits = 0
if edits > 0: CONFIG.save()

# limit migrations.
if not MIGRATIONS:

	# check db.
	SUDO, PERMISSION = True, 770
	DATABASE.check(
		owner=dev0s.defaults.vars.user,
		group=dev0s.defaults.vars.group,
		permission=PERMISSION,
		sudo=SUDO,
		recursive=False,
		silent=False,
		hierarchy={
			"data/":{
				"path":"data/",
				"directory":True,
				"owner":dev0s.defaults.vars.user,
				"group":dev0s.defaults.vars.group,
				"permission":PERMISSION,
				"sudo":SUDO,
			},
			"backups/":{
				"path":"backups/",
				"directory":True,
				"owner":dev0s.defaults.vars.user,
				"group":dev0s.defaults.vars.group,
				"permission":PERMISSION,
				"sudo":SUDO,
			},
			"clients/":{
				"path":"clients/",
				"directory":True,
				"owner":dev0s.defaults.vars.user,
				"group":dev0s.defaults.vars.group,
				"permission":PERMISSION,
				"sudo":SUDO,
			},
			f"clients/{ADMINISTRATOR}/":{
				"path":f"clients/{ADMINISTRATOR}/",
				"directory":True,
				"owner":dev0s.defaults.vars.user,
				"group":dev0s.defaults.vars.group,
				"permission":PERMISSION,
				"sudo":SUDO,
			},
			"logs/":{
				"path":"logs/",
				"directory":True,
				"owner":dev0s.defaults.vars.user,
				"group":dev0s.defaults.vars.group,
				"permission":PERMISSION,
				"sudo":SUDO,
			},
		})

	# website.
	website = w3bsite.Website(
		# main
		root=SOURCE.fp.path,
		database=DATABASE.fp.path,
		library=f"/usr/local/lib/{ALIAS}",
		domain="0.0.0.0:8002",
		name="VBackups",
		remote=None,
		# the template data (only required when running the website) (overwrites the w3bsite template data keys).
		template_data={
			# customize colors.
			"COLORS":{
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
				"background":"#FAFAFA",#"#E7E9EF", #"#FAFAFA",
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
			},
		},
		# custom styling.
		styling={
			"LEFTBAR_WIDTH":"280px", # px
			"RIGHTBAR_WIDTH":"280px", # px
			"TOPBAR_HEIGHT":"50px", #px
		},
		# 	the organization name.
		organization="VanDenBerghInc",
		# aes.
		aes_passphrase=None,
		# options.
		namecheap_enabled=False,
		firebase_enabled=False,
		stripe_enabled=False,
		email_enabled=False,
		users_subpath="clients/",
		id_by_username=True,
		interactive=False,
		_2fa=False,
		production=PRODUCTION,
	)

	# export env.
	website.security.set_secret_env("VBACKUPS_DATABASE", str(DATABASE))
		
	#