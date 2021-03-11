#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import requests, sys, os, ast, json, glob, platform, time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

# inc imports.
import w3bsite
from dev0s.shortcuts import *

# source.
SOURCE_NAME = ALIAS = "api.vandenberghinc.com"
SOURCE_PATH = dev0s.defaults.source_path(__file__, back=3)
OS = dev0s.defaults.operating_system(supported=["linux", "macos"])
#dev0s.defaults.alias(alias=ALIAS, executable=SOURCE_PATH, sudo=True)

# production settings.
# do not deploy to heroku with production disabled.
PRODUCTION = dev0s.env.get_boolean("PRODUCTION", default=True)
MAINTENANCE = dev0s.env.get_boolean("MAINTENANCE", default=True)

# website.
website = w3bsite.Website(
	serialized=f"__defaults__/env/website",
	django=True,
	maintenance=True,
	root=SOURCE_PATH, 
	production=PRODUCTION,)

# synchronize users.
if dev0s.env.get_boolean("MIGRATIONS") == False:
	response = website.users.synchronize()
	if not response.success: raise ValueError(response['error'])

# colors.
COLORS = {
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

# template data.
website.template_data["COLORS"] = COLORS

# database.
DATABASE = website.database
if not Files.exists(DATABASE): os.system(f"sudo mkdir {DATABASE} && sudo chown {dev0s.defaults.vars.user}:{dev0s.defaults.vars.group} {DATABASE}")
if not Files.exists(f"{DATABASE}/data/"): os.mkdir(f"{DATABASE}/data/") # for database.
if not Files.exists(f"{DATABASE}/packages/"): os.mkdir(f"{DATABASE}/packages/")
