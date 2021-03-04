# user wide cache to share variables accross tty sessions since default env variables is instable.
import syst3m
from fil3s import *
if not Files.exists(f"{syst3m.defaults.vars.home}/.w3bsite/"): 
	Files.create(path=f"{syst3m.defaults.vars.home}/.w3bsite/", directory=True)
cache = syst3m.cache.Cache(
	path=f"{syst3m.defaults.vars.home}/.w3bsite/.cache/")