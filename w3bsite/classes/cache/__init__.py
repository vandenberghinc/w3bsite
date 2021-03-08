# user wide cache to share variables accross tty sessions since default env variables is instable.
import syst3m
from dev0s import *
if not Files.exists(f"{Defaults.vars.home}/.w3bsite/"): 
	Files.create(path=f"{Defaults.vars.home}/.w3bsite/", directory=True)
cache = syst3m.cache.Cache(
	path=f"{Defaults.vars.home}/.w3bsite/.cache/")