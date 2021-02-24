#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes import *

# version.
import fil3s
try: version = int(fil3s.Files.load(fil3s.gfp.base(__file__)+".version.py").replace("\n","").replace(" ",""))
except: version = None
