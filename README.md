# w3bsite
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: macos & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"> 
</p>

## Table of content:
  * [Description](#description)
  * [Installation](#installation)
  * [Troubleshooting](#troubleshooting)
  * [Setup.](#setup.)
  * [Code Examples](#code-examples)

# Description:
Website library.

# Installation:
Install the package.

	pip3 install w3bsite --upgrade

# Troubleshooting:

#### Apple Silicon M1:

##### Failed to install grpcio
	arch -arch x86_64 /usr/bin/python3 -m pip install firebase-admin

# Setup.

#### Namecheap.
1: Go to https://namecheap.com and sign up / sign in.  <br>
2: Link a credit card to your account. <br>
3: $50 balance is required to activate the developer api, so add balance if you did not reach this limit yet. <br>
4: Enable the developer API. <br>
5: Whitelist your public ip (https://aruljohn.com). <br>
6: Note / copy the api key which will be required later. <br>

#### /website.py
Create a file named "website.py" in your website's root directory.
	
	my-website/
		website.py
		/

Add the following code to the file.
```python
#!/usr/bin/env python3
from w3bsite import Website
from dev0s import *
website = Website(
	...
)
if __name__ == "__main__":
	website.cli()
```

# Code Examples:

### Table of content:
- [__Customers__](#customers)
  * [check](#check)
  * [create](#create)
  * [delete](#delete)
  * [get_id](#get_id)
  * [get](#get)
  * [get_cards](#get_cards)
  * [create_card](#create_card)
  * [delete_card](#delete_card)
- [__Database__](#database)
  * [load](#load)
  * [save](#save)
  * [delete](#delete-1)
  * [join](#join)
  * [names](#names)
- [__Deployment__](#deployment)
  * [start](#start)
  * [stop](#stop)
  * [restart](#restart)
  * [status](#status)
  * [reset_logs](#reset_logs)
  * [tail](#tail)
  * [configure](#configure)
  * [deploy](#deploy)
  * [generate_tls](#generate_tls)
  * [activate_tls](#activate_tls)
  * [bundle_tls](#bundle_tls)
  * [check_dns](#check_dns)
- [__Django__](#django)
  * [start](#start-1)
  * [create](#create-1)
  * [create_app](#create_app)
  * [migrations](#migrations)
  * [collect_static](#collect_static)
- [__Email__](#email)
  * [login](#login)
  * [send](#send)
- [__FireStore__](#firestore)
  * [list](#list)
  * [load](#load-1)
  * [load_collection](#load_collection)
  * [save](#save-1)
  * [delete](#delete-2)
- [__Firebase__](#firebase)
- [__Logging__](#logging)
  * [log](#log)
- [__Namecheap__](#namecheap)
  * [check_domain](#check_domain)
  * [get_domains](#get_domains)
  * [get_info](#get_info)
  * [get_dns](#get_dns)
  * [check_dns](#check_dns-1)
  * [set_dns](#set_dns)
  * [add_dns](#add_dns)
  * [tag_dns](#tag_dns)
  * [get_sld_and_tld](#get_sld_and_tld)
  * [get_tls](#get_tls)
  * [create_tls](#create_tls)
  * [activate_tls](#activate_tls-1)
- [__Plans__](#plans)
  * [get](#get-1)
  * [create](#create-2)
- [__RateLimit__](#ratelimit)
  * [increment](#increment)
  * [verify](#verify)
- [__Security__](#security)
  * [generate_tls](#generate_tls-1)
  * [set_secret_env](#set_secret_env)
  * [get_secret_env](#get_secret_env)
- [__Stripe__](#stripe)
  * [check](#check-1)
  * [get_product_id](#get_product_id)
  * [get_plan_id](#get_plan_id)
  * [get_product_id_by_plan_id](#get_product_id_by_plan_id)
  * [get_product_name](#get_product_name)
  * [get_plan_name](#get_plan_name)
- [__Subscriptions__](#subscriptions)
  * [create](#create-3)
  * [get](#get-2)
  * [cancel](#cancel)
- [__Users__](#users)
  * [get](#get-3)
  * [create](#create-4)
  * [update](#update)
  * [delete](#delete-3)
  * [verify_id_token](#verify_id_token)
- [__VPS__](#vps)
  * [configure](#configure-1)
  * [deploy](#deploy-1)
- [__Website__](#website)
  * [initialize](#initialize)
  * [cli](#cli)
  * [deploy](#deploy-2)
  * [check_dns](#check_dns-2)
  * [create](#create-5)
  * [serialize](#serialize)
  * [init_from_serialized](#init_from_serialized)
  * [template](#template)

## Customers:
The website.stripe.customers object class.
``` python 

# import the website.stripe.customers object class.
from classes.config import website

```

#### Functions:

##### check:
``` python

# call website.stripe.customers.check.
response = website.stripe.customers.check(
    # the users email.
    email=None, )

```
##### create:
``` python

# call website.stripe.customers.create.
response = website.stripe.customers.create(
    # the users email.
    email=None, )

```
##### delete:
``` python

# call website.stripe.customers.delete.
response = website.stripe.customers.delete(
    # the stripe customer id.
    id=None, )

```
##### get_id:
``` python

# call website.stripe.customers.get_id.
response = website.stripe.customers.get_id(
    # the users email.
    email=None, )

```
##### get:
``` python

# call website.stripe.customers.get.
response = website.stripe.customers.get(
    # the stripe customer id (optional).
    id=None, )

```
##### get_cards:
``` python

# call website.stripe.customers.get_cards.
response = website.stripe.customers.get_cards(
    # the stripe customer id.
    id=None, )

```
##### create_card:
``` python

# call website.stripe.customers.create_card.
response = website.stripe.customers.create_card(
    # the stripe customer id.
    id=None,
    # the card holders name.
    name=None,
    # the card number.
    number=None,
    # the card expiration month.
    month=None,
    # the card expiration year.
    year=None,
    # the card cvc.
    cvc=None, )

```
##### delete_card:
``` python

# call website.stripe.customers.delete_card.
response = website.stripe.customers.delete_card(
    # the stripe customer id.
    id=None, )

```

## Database:
The website.db object class.
``` python 

# import the website.db object class.
from classes.config import website

```

#### Functions:

##### load:
``` python

# call website.db.load.
response = website.db.load(path=None)

```
##### save:
``` python

# call website.db.save.
response = website.db.save(path=None, data=None, overwrite=False)

```
##### delete:
``` python

# call website.db.delete.
response = website.db.delete(path=None, data=None)

```
##### join:
``` python

# call website.db.join.
_ = website.db.join(path)

```
##### names:
``` python

# call website.db.names.
_ = website.db.names(
    # the sub path (leave None to use the root path)
    path=None, )

```

## Deployment:
The website.deployment object class.
``` python 

# import the website.deployment object class.
from classes.config import website

```

#### Functions:

##### start:
``` python

# call website.deployment.start.
response = website.deployment.start()

```
##### stop:
``` python

# call website.deployment.stop.
response = website.deployment.stop()

```
##### restart:
``` python

# call website.deployment.restart.
response = website.deployment.restart()

```
##### status:
``` python

# call website.deployment.status.
response = website.deployment.status()

```
##### reset_logs:
``` python

# call website.deployment.reset_logs.
response = website.deployment.reset_logs()

```
##### tail:
``` python

# call website.deployment.tail.
response = website.deployment.tail(nginx=False, debug=False)

```
##### configure:
``` python

# call website.deployment.configure.
response = website.deployment.configure(reinstall=False, log_level=0, loader=None)

```
##### deploy:
``` python

# call website.deployment.deploy.
response = website.deployment.deploy(code_update=False, reinstall=False, log_level=0)

```
##### generate_tls:
``` python

# call website.deployment.generate_tls.
response = website.deployment.generate_tls(log_level=0)

```
##### activate_tls:
``` python

# call website.deployment.activate_tls.
response = website.deployment.activate_tls(log_level=0)

```
##### bundle_tls:
``` python

# call website.deployment.bundle_tls.
response = website.deployment.bundle_tls(directory, log_level=0)

```
##### check_dns:
``` python

# call website.deployment.check_dns.
response = website.deployment.check_dns(log_level=0)

```

## Django:
The website.django object class.
``` python 

# import the website.django object class.
from classes.config import website

```

#### Functions:

##### start:
``` python

# call website.django.start.
response = website.django.start(host="127.0.0.1", port="8000", production=False)

```
##### create:
``` python

# call website.django.create.
response = website.django.create()

```
##### create_app:
``` python

# call website.django.create_app.
response = website.django.create_app(name="home")

```
##### migrations:
``` python

# call website.django.migrations.
response = website.django.migrations(forced=False, log_level=Defaults.options.log_level)

```
##### collect_static:
``` python

# call website.django.collect_static.
response = website.django.collect_static(log_level=Defaults.options.log_level)

```

## Email:
The website.users.email object class.
``` python 

# import the website.users.email object class.
from classes.config import website

```

#### Functions:

##### login:
``` python

# call website.users.email.login.
response = website.users.email.login(timeout=3)

```
##### send:
``` python

# call website.users.email.send.
response = website.users.email.send(
    # the email's subject.
    subject="Subject.",
    # define either html or html_path.
    html=None,
    html_path=None,
    # the email's recipients.
    recipients=[],
    # optional attachments.
    attachments=[], )

```

## FireStore:
The website.firebase.firestore object class.
``` python 

# import the website.firebase.firestore object class.
from classes.config import website

```

#### Functions:

##### list:
``` python

# call website.firebase.firestore.list.
response = website.firebase.firestore.list(reference)

```
##### load:
``` python

# call website.firebase.firestore.load.
response = website.firebase.firestore.load(reference)

```
##### load_collection:
``` python

# call website.firebase.firestore.load_collection.
response = website.firebase.firestore.load_collection(reference)

```
##### save:
``` python

# call website.firebase.firestore.save.
response = website.firebase.firestore.save(reference, data)

```
##### delete:
``` python

# call website.firebase.firestore.delete.
response = website.firebase.firestore.delete(reference)

```

## Firebase:
The website.firebase object class.
``` python 

# import the website.firebase object class.
from classes.config import website

```
## Logging:
The website.logging object class.
``` python 

# import the website.logging object class.
from classes.config import website

```

#### Functions:

##### log:
``` python

# call website.logging.log.
_ = website.logging.log(
    # option 1.
    #     the message response body.
    message=None,
    # option 2.
    #     the error response body.
    error=None,
    # option 3.
    #     the entire response.
    response=None, )

```

## Namecheap:
The website.namecheap object class.
``` python 

# import the website.namecheap object class.
from classes.config import website

```

#### Functions:

##### check_domain:
``` python

# call website.namecheap.check_domain.
response = website.namecheap.check_domain(domain=None)

```
##### get_domains:
``` python

# call website.namecheap.get_domains.
response = website.namecheap.get_domains()

```
##### get_info:
``` python

# call website.namecheap.get_info.
response = website.namecheap.get_info(domain=None)

```
##### get_dns:
``` python

# call website.namecheap.get_dns.
response = website.namecheap.get_dns(domain=None)

```
##### check_dns:
``` python

# call website.namecheap.check_dns.
response = website.namecheap.check_dns(
    # the domain (optional).
    domain=None,
    # the dns record type,
    type=None,
    # the dns record host,
    host=None,
    # the dns record value/address,
    value=None,
    # the get_dns.records dictionary (optionally to increase speed).
    records=None, )

```
##### set_dns:
``` python

# call website.namecheap.set_dns.
response = website.namecheap.set_dns(
    # the domain (optional).
    domain=None,
    # the dns records (erases all others).
    records={
        "$record-1":{
            # the dns record type (required),
            "type":None,
            # the dns record host (required),
            "host":None,
            # the dns record value/address (required),
            "value":None,
            # the dns record ttl (optional default is 1800),
            "ttl":1800,
        },
    }, )

```
##### add_dns:
``` python

# call website.namecheap.add_dns.
response = website.namecheap.add_dns(
    # the domain (optional).
    domain=None,
    # the dns record type,
    type=None,
    # the dns record host,
    host=None,
    # the dns record value/address,
    value=None,
    # the dns record ttl (optional default is 1800),
    ttl=1800,
    # the get_dns.records dictionary (optionally to increase speed).
    records=None, )

```
##### tag_dns:
``` python

# call website.namecheap.tag_dns.
response = website.namecheap.tag_dns(
    # the dns record type,
    type=None,
    # the dns record host,
    host=None,
    # the dns record value/address,
    value=None, )

```
##### get_sld_and_tld:
``` python

# call website.namecheap.get_sld_and_tld.
response = website.namecheap.get_sld_and_tld(domain=None)

```
##### get_tls:
``` python

# call website.namecheap.get_tls.
response = website.namecheap.get_tls()

```
##### create_tls:
``` python

# call website.namecheap.create_tls.
response = website.namecheap.create_tls(
    # the expiration years.
    years=2,
    # the tls type.
    type="PositiveSSL", )

```
##### activate_tls:
``` python

# call website.namecheap.activate_tls.
response = website.namecheap.activate_tls(
    # the certificate's id.
    certificate_id=None, )

```

## Plans:
The website.stripe.plans object class.
``` python 

# import the website.stripe.plans object class.
from classes.config import website

```

#### Functions:

##### get:
``` python

# call website.stripe.plans.get.
response = website.stripe.plans.get(
    # the plan id (plan_***) (optional).
    id=None,
    # get the subscriptions of the plan.
    get_subscriptions=False,
    # get active subscriptions only (required get_subscriptions=True).
    active_only=True, )

```
##### create:
``` python

# call website.stripe.plans.create.
response = website.stripe.plans.create(
    # the plan id.
    id=None,
    # the product id.
    product=None,
    # price per month.
    price=None,
    # the price currencry.
    currency="eur",
    # recurring options (do not edit unless you know what you are doing).
    recurring={"interval": "month"}, )

```

## RateLimit:
The website.ratelimit object class.
``` python 

# import the website.ratelimit object class.
from classes.config import website

```

#### Functions:

##### increment:
``` python

# call website.ratelimit.increment.
response = website.ratelimit.increment(
    # user identification options (select one option):
    #    option 1: user email.
    email=None,
    username=None,
    #    option 2: the requests ip.
    ip=None,
    # rate lmit mode id.
    mode=None,
    # the increment count.
    count=1, )

```
##### verify:
``` python

# call website.ratelimit.verify.
response = website.ratelimit.verify(
    # user identification options (select one option):
    #    option 1: user email.
    email=None,
    username=None,
    #    option 2: the requests ip.
    ip=None,
    # rate lmit mode id.
    mode=None,
    # rate limit.
    limit=1000,
    # reset after.
    reset_minutes=3600*24,
    # increment on succes.
    increment=False,
    increment_count=1, )

```

## Security:
The website.security object class.
``` python 

# import the website.security object class.
from classes.config import website

```

#### Functions:

##### generate_tls:
``` python

# call website.security.generate_tls.
response = website.security.generate_tls()

```
##### set_secret_env:
``` python

# call website.security.set_secret_env.
response = website.security.set_secret_env(key, value)

```
##### get_secret_env:
``` python

# call website.security.get_secret_env.
_ = website.security.get_secret_env(key, default=None, required=True)

```

## Stripe:
The website.stripe object class.
``` python 

# import the website.stripe object class.
from classes.config import website

```

#### Functions:

##### check:
``` python

# call website.stripe.check.
response = website.stripe.check()

```
##### get_product_id:
``` python

# call website.stripe.get_product_id.
response = website.stripe.get_product_id(product=None)

```
##### get_plan_id:
``` python

# call website.stripe.get_plan_id.
response = website.stripe.get_plan_id(product=None, plan=None)

```
##### get_product_id_by_plan_id:
``` python

# call website.stripe.get_product_id_by_plan_id.
response = website.stripe.get_product_id_by_plan_id(plan_id)

```
##### get_product_name:
``` python

# call website.stripe.get_product_name.
response = website.stripe.get_product_name(id=None)

```
##### get_plan_name:
``` python

# call website.stripe.get_plan_name.
response = website.stripe.get_plan_name(id=None)

```

## Subscriptions:
The website.stripe.subscriptions object class.
``` python 

# import the website.stripe.subscriptions object class.
from classes.config import website

```

#### Functions:

##### create:
``` python

# call website.stripe.subscriptions.create.
response = website.stripe.subscriptions.create(
    # the email of the user that will be charged.
    email=None,
    customer_id=None, # instead of email for effienciency.
    # the plan ids (list).
    plans=[], )

```
##### get:
``` python

# call website.stripe.subscriptions.get.
response = website.stripe.subscriptions.get(
    # a specfic user email (optional).
    email=None,
    # active subscription plans only.
    active_only=True,
    # by customer id (custumer id as keys values in return).
    by_customer_id=False, )

```
##### cancel:
``` python

# call website.stripe.subscriptions.cancel.
response = website.stripe.subscriptions.cancel(
    # option 1:
    #     the stripe subscription id.
    subscription_id=None,
    # option 2:
    #     select a user identification option.
    email=None,
    #     the stripe plan id.
    plan=None, )

```

## Users:
The website.firebase.users object class.
``` python 

# import the website.firebase.users object class.
from classes.config import website

```

#### Functions:

##### get:
``` python

# call website.firebase.users.get.
response = website.firebase.users.get(
    # define one of the following parameters.
    uid=None,
    email=None,
    phone_number=None, )

```
##### create:
``` python

# call website.firebase.users.create.
response = website.firebase.users.create(
    # required:
    email=None,
    password=None,
    verify_password=None,
    # optionals:
    name=None,
    phone_number=None,
    photo_url=None,
    email_verified=False, )

```
##### update:
``` python

# call website.firebase.users.update.
response = website.firebase.users.update(
    # required:
    email=None,
    # optionals:
    name=None,
    password=None,
    verify_password=None,
    phone_number=None,
    photo_url=None,
    email_verified=None, )

```
##### delete:
``` python

# call website.firebase.users.delete.
response = website.firebase.users.delete(
    # option 1:
    # the user's uid (much faster).
    uid=None,
    # option 2:
    # the users email / username.
    email=None, )

```
##### verify_id_token:
``` python

# call website.firebase.users.verify_id_token.
response = website.firebase.users.verify_id_token(id_token)

```

## VPS:
The website.vps object class.
``` python 

# import the website.vps object class.
from classes.config import website

```

#### Functions:

##### configure:
``` python

# call website.vps.configure.
response = website.vps.configure(reinstall=False, log_level=0)

```
##### deploy:
``` python

# call website.vps.deploy.
response = website.vps.deploy(code_update=False, reinstall=False, log_level=0)

```

## Website:
The website object class.
``` python 

# initialize the website object class.
website = Website(
    #
    # General.
    #     the root path.
    root=None, # example: FilePath(__file__).base(back=1).replace("./","")
    #     the root domain.
    domain=None,
    #     the website name.
    name=None,
    #     the database path (optional).
    database=None,
    #     the library path (optional).
    library=None,
    #a
    # Deployment.
    #     remote depoyment, options: [local, vps, heroku].
    remote="local",
    #
    # Developers.
    #    the developer users (emails).
    developers=[],
    #
    # Django.
    #    maintenance boolean.
    maintenance=False,
    #     the template data (only required when running the website) (overwrites the w3bsite template data keys).
    template_data={},
    #    2fa required for login.
    _2fa=False,
    #
    # Organization.
    #     the author's / comitters name.
    author=None,
    #     the admin's email.
    email=None,
    #     the organization name.
    organization=None,
    #     the organization unit.
    organization_unit="Information Technology",
    #     the organization country code.
    country_code="NL",
    #     the organization localization's city name.
    city=None,
    #     the organization localization's province / state.
    province=None,
    #
    # AES.
    #    the passphrase of the aes master-key (defaults is no passphrase).
    aes_passphrase=None,
    #
    # Namecheap.
    #    namecheap enabled.
    namecheap_enabled=True,
    #     your namecheap username.
    namecheap_username=None,
    #     your namecheap api key.
    namecheap_api_key=None,
    #
    # Firebase.
    #    firebase enabled.
    firebase_enabled=True,
    #     your firebase admin service account key, (dict) [https://console.firebase.google.com > Service Accounts > Firebase admin].
    firebase_admin={},
    #     your firebase sdk javascript configuration, (dict) [https://console.firebase.google.com > Settings > General > Web JS SDK].
    firebase_js={},
    #
    # Stripe.
    # enable strip.e
    stripe_enabled=True,
    #     your stripe secret key (str) [https://stripe.com > Dashboard > Developer > API Keys > Secret Key].
    stripe_secret_key=None,
    #     your stripe publishable key (str) [https://stripe.com > Dashboard > Developer > API Keys > Secret Key].
    stripe_publishable_key=None,
    #    the stripe subscriptions.
    #        do not edit the plan & product names after creation.
    #        price changes are not supported yet, will be in the future.
    stripe_subscriptions={
        #"vserver": {
        #    "basic": {
        #        "rank":1,
        #        "price":50,
        #        "currency":"eur",
        #        "favicon":"https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vserver/icon/icon.png"
        #    },
        #    "premium": {
        #        "rank":2,
        #        "price":100,
        #        "currency":"eur",
        #    },
        #    "pro": {
        #        "rank":3,
        #        "price":250,
        #        "currency":"eur",
        #    },
        #}
    },
    #     the stripe products.
    stripe_products={
        #"vserver": {
        #    "basic": {
        #        "rank":1,
        #        "price":50,
        #        "currency":"eur",
        #        "favicon":"https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vserver/icon/icon.png"
        #    },
        #    "premium": {
        #        "rank":2,
        #        "price":100,
        #        "currency":"eur",
        #    },
        #    "pro": {
        #        "rank":3,
        #        "price":250,
        #        "currency":"eur",
        #    },
        #}
    },
    #
    #
    # Smtp Email
    #     sending emails [https://gmail.com > Security > Enable Unsafe 3th party applications].
    email_enabled=True,
    email_address=None,
    email_password=None,
    email_smtp_host="smtp.gmail.com",
    email_smtp_port=587,
    #
    # VPS.
    #     the public ip of the vps.
    vps_ip=None,
    #    the vps ssh port.
    vps_port=22,
    #    the executing username on the vps.
    vps_username=None,
    #
    # Additional Options.
    #     prevent heroku deployment.
    prevent_heroku_deployment=False,
    #     purchase tls/ssl certificate from namecheap.
    purchase_tls_certificate=False,
    #     interactive mode.
    interactive=False,
    #    production mode.
    production=True,
    #     the users sub path.
    users_subpath="users/",
    #     id users by username.
    id_by_username=True,
    #
    # the logs.
    log_level=Defaults.options.log_level,
    # styling options.
    styling={},
    #
    #
    # optionally initizialize from a serialized dict (for config.py) (still requires parameters: root).
    serialized=None, )

```

#### Functions:

##### initialize:
``` python

# call website.initialize.
response = website.initialize()

```
##### cli:
``` python

# call website.cli.
_ = website.cli()

```
##### deploy:
``` python

# call website.deploy.
response = website.deploy(code_update=False, reinstall=False, log_level=0)

```
##### check_dns:
``` python

# call website.check_dns.
response = website.check_dns(log_level=0)

```
##### create:
``` python

# call website.create.
response = website.create()

```
##### serialize:
``` python

# call website.serialize.
_ = website.serialize(save=False)

```
##### init_from_serialized:
``` python

# call website.init_from_serialized.
_ = website.init_from_serialized(serialized=None)

```
##### template:
``` python

# call website.template.
_ = website.template(dictionary={}, update=False)

```

#### build_urls:
The build_urls function.
``` python

# call build_urls.
_ = build_urls(views=[])

```
#### include_apps:
The include_apps function.
``` python

# call include_apps.
_ = include_apps(apps=[], auto_include=False)

```
#### main:
The main function.
``` python

# call main.
_ = main()

```
