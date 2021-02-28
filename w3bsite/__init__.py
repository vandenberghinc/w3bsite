#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes import *

# source path & version.
import fil3s
source_path = fil3s.gfp.base(__file__)
try: version = fil3s.Files.load(source_path+".version.py").replace("\n","").replace(" ","")
except: version = None