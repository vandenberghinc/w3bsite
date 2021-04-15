# user wide cache to share variables across tty sessions since default env variables is instable.
from dev0s.shortcuts import *
if not Files.exists(f"{dev0s.defaults.vars.home}/.w3bsite/"): 
	Files.create(path=f"{dev0s.defaults.vars.home}/.w3bsite/", directory=True)
cache = dev0s.database.Database(
	path=f"{dev0s.defaults.vars.home}/.w3bsite/.cache/")