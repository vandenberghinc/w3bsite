#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import requests, sys, os, ast, json, glob, platform, time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

# inc imports.
from dev0s.shortcuts import *

# fyunctions.
def __get_file_path_base__(path, back=1):
	path = path.replace('//','/')
	if path[len(path)-1] == "/": path = path[:-1]
	string, items, c = "", path.split("/"), 0
	for item in items:
		if c == len(items)-(1+back):
			string += "/"+item
			break
		else:
			string += "/"+item
		c += 1
	return string+"/"
def get_boolean_environment_variable(id):
	bool = os.environ.get(id)
	if bool in ["True", "true", True]: return True
	else: return False

# source.
SOURCE_NAME = "w3bsite"
VERSION = "v1"
SOURCE_PATH = __get_file_path_base__(__file__, back=4)

# production settings.
# do not deploy to heroku with production disabled.
PRODUCTION = get_boolean_environment_variable("PRODUCTION")

# template variables.
TEMPLATE_DATA = {
	"colors":{
		"tint":"...",
		"white":"#FAFAFA",
		"blue":"#5A8FE6",
		"purple":"#B32FCA",
		"red":"#FD304E",
		"pink":"#F62B7D",
		"orange":"#FF8800",
		"green":"#006633",
		"darkest":"#1F2227",
		"darker": "#20242A35",
		"dark": "#262B30",
	},
	"PRODUCTION":PRODUCTION,
}

# logs.
if PRODUCTION:
	dev0s.response.log_file = f"{SOURCE_PATH}/{VERSION}/logs/logs.txt"
	r3stapi.dev0s.response.log_file = f"{SOURCE_PATH}/{VERSION}/logs/logs.txt"
else:
	dev0s.response.log_file = f"logs/logs.txt"
	r3stapi.dev0s.response.log_file = f"logs/logs.txt"
