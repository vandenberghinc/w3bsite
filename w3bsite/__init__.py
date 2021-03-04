#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes import *

# source path & version.
import fil3s
source = fil3s.gfp.clean(fil3s.gfp.base(__file__), remove_last_slash=True)+"/"
base = fil3s.gfp.clean(fil3s.gfp.base(source), remove_last_slash=True)+"/"
try: version = fil3s.Files.load(source+".version.py").replace("\n","").replace(" ","")
except: version = None