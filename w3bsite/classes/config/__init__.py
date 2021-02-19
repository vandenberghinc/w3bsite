#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random, requests, urllib, threading, time, string, traceback

# inc imports.
import cl1, netw0rk, syst3m, ssht00ls
from fil3s import Files, Formats
from r3sponse import r3sponse

# source.
ALIAS = SOURCE_NAME = "w3bsite"
SOURCE_PATH = syst3m.defaults.source_path(__file__, back=4)
BASE = syst3m.defaults.source_path(SOURCE_PATH)
OS = syst3m.defaults.operating_system(supported=["linux", "macos"])
#syst3m.defaults.alias(alias=ALIAS, executable=f"{SOURCE_PATH}/")

# universal variables.
OWNER = USER = os.environ.get("USER")
GROUP = "root"
HOME = f"/home/"
MEDIA = f"/media/{USER}/"
if OS in ["macos"]: 
	HOME = f"/Users/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"

# network info.
NETWORK_INFO = netw0rk.network.info()
if not r3sponse.success(NETWORK_INFO): raise ValueError(NETWORK_INFO["error"])

# log level.
LOG_LEVEL = syst3m.defaults.get_log_level()
