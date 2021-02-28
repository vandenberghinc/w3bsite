#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random, requests, urllib, threading, time, string, traceback

# inc imports.
import cl1, netw0rk, syst3m, ssht00ls
from fil3s import *
from r3sponse import r3sponse

# source.	
ALIAS = "w3bsite"
SOURCE_PATH = syst3m.defaults.source_path(__file__, back=3)
BASE = syst3m.defaults.source_path(SOURCE_PATH)
OS = syst3m.defaults.operating_system(supported=["linux", "macos"])
LOG_LEVEL = syst3m.defaults.log_level(default=0)
#syst3m.defaults.alias(alias=ALIAS, executable=SOURCE_PATH)

# network info.
NETWORK_INFO = netw0rk.network.info()
if not NETWORK_INFO["success"]: raise ValueError(NETWORK_INFO["error"])

# check lib.
lib = Directory(f"{SOURCE_PATH}/classes/deployment/lib")
if not lib.fp.exists():# or len(lib.paths()) != 7) and syst3m.env.get("HOST") not in ["macbookpro_daan"]:
	r3sponse.log("Installing the w3bsite library.")
	os.system(f"rm -fr /tmp/w3bsite && git clone https://github.com/vandenberghinc/w3bsite /tmp/w3bsite 2> /dev/null && rsync -azq /tmp/w3bsite/w3bsite/classes/deployment/lib/ {SOURCE_PATH}/classes/deployment/lib/")
