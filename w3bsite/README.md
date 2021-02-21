# W3bsite
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="VanDenBerghInc" width="50"/>
</p>

## Installation
	pip3 install w3bsite --upgrade && python3 -c "import w3bsite"
### Troubleshooting:
#### Apple Silicon M1:
##### Failed to install grpcio
	arch -arch x86_64 /usr/bin/python3 -m pip install firebase-admin

## Setup.

### Namecheap.
1: Go to https://namecheap.com and sign up / sign in.  <br>
2: Link a credit card to your account. <br>
3: $50 balance is required to activate the developer api, so add balance if you did not reach this limit yet. <br>
4: Enable the developer API. <br>
5: Whitelist your public ip (https://aruljohn.com). <br>
6: Note / copy the api key which will be required later. <br>

### Heroku.
1: go to https://heroku.com and sign up / sign in.  <br>
2: login to the heroku cli with [$ heroku login]. <br>

### /.website.py
Create a file named "website.py" in your websites root directory.
	
	my-website/
		website.py
		/

Add the following code to the file.
```python
#!/usr/bin/env python3
from w3bsite import Website
from fil3s import *
website = Website(
	# the root path.
	root=FilePath(__file__).base(back=1),
	# the website name.
	name="My Website",
	# the organization.
	organization="My Business",
	# the organization unit.
	organization_unit="Information Technology",
	# the organization country code.
	country_code="NL",
	# the root domain.
	domain="mydomain.com",
	# the sub domains.
	sub_domains=[],
	# your namecheap username.
	namecheap_username="myusername",
	# your namecheap api key.
	namecheap_api_key=".......",)
if __name__ == "__main__":
	website.cli()
```

## CLI:
	Usage: example <mode> <options> 
	Modes:
	    -h / --help : Show the documentation.
	Options:
	Author: Daan van den Bergh 
	Copyright: © Daan van den Bergh 2020. All rights reserved.

## Python Examples.

Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# initialize the encryption class.
encryption = Encryption(
	key='mykey/',
	passphrase='MyPassphrase123!')
```
