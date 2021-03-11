#!/usr/bin/env python3
import json
from r3sponse import r3sponse
from w3bsite import Website
from dev0s.shortcuts import *
website = Website(
	# the root path.
	root=FilePath(__file__).base(back=2),
	# the root version.
	version="v1",
	# the website name.
	name="PokerStats",
	# the admin's email.
	email="pokerstats.business@gmail.com",
	# the organization.
	organization="VanDenBerghInc",
	# the organization unit.
	organization_unit="Information Technology",
	# the organization country code.
	country_code="NL",
	# the organization localization's city name.
	city="Utrecht",
	# the organization localization's province / state.
	province="Utrecht",
	# the root domain.
	domain="pokerstats.app",
	# the sub domains.
	sub_domains=[],
	# your namecheap username.
	namecheap_username="pokerstatsbusiness",
	# your namecheap api key.
	namecheap_api_key="610649048b9c424f9abf91f472f5bd74",)
if __name__ == "__main__":
	website.cli()
