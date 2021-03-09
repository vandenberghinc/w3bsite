#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random, requests, urllib, threading, time, string, traceback

# inc imports.
import dev0s, netw0rk, syst3m, ssht00ls
from ssht00ls import ssht00ls_agent
from dev0s import *

# source.	
ALIAS = "w3bsite"
SOURCE_PATH = Defaults.source_path(__file__, back=3)
BASE = Defaults.source_path(SOURCE_PATH)
OS = Defaults.operating_system(supported=["linux", "macos"])
LOG_LEVEL = Defaults.log_level(default=0)
#Defaults.alias(alias=ALIAS, executable=SOURCE_PATH)

# network info.
NETWORK_INFO = netw0rk.network.info()
if not NETWORK_INFO["success"]: raise ValueError(NETWORK_INFO["error"])

# check lib.
lib = Directory(f"{SOURCE_PATH}/classes/deployment/lib")
if not lib.fp.exists():# or len(lib.paths()) != 7) and Environment.get("HOST") not in ["macbookpro_daan"]:
	Response.log("Installing the w3bsite library.")
	os.system(f"rm -fr /tmp/w3bsite && git clone -q https://github.com/vandenberghinc/w3bsite /tmp/w3bsite 2> /dev/null && rsync -azq /tmp/w3bsite/w3bsite/classes/deployment/lib/ {SOURCE_PATH}/classes/deployment/lib/")

# the cache.
from w3bsite.classes.cache import cache
