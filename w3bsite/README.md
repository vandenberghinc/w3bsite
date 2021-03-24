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

##### Failed to install grpcio on MacOS Apple Silicon M1.
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
- [__Database__](#database)
  - [__Database__](#database)
    * [load](#load)
    * [save](#save)
    * [delete](#delete)
    * [names](#names)
    * [subpath](#subpath)
    * [fullpath](#fullpath)
    * [join](#join)
- [__Deployment__](#deployment)
  - [__VPS__](#vps)
    * [configure](#configure)
    * [deploy](#deploy)
  - [__Deployment__](#deployment)
    * [start](#start)
    * [stop](#stop)
    * [restart](#restart)
    * [status](#status)
    * [reset_logs](#reset_logs)
    * [tail](#tail)
    * [configure](#configure-1)
    * [deploy](#deploy-1)
    * [generate_tls](#generate_tls)
    * [activate_tls](#activate_tls)
    * [bundle_tls](#bundle_tls)
    * [check_dns](#check_dns)
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
- [__Django__](#django)
  - [__Django__](#django)
    * [start](#start-1)
    * [create](#create)
    * [create_app](#create_app)
    * [migrations](#migrations)
    * [collect_static](#collect_static)
  - [__Users__](#users)
    * [create](#create-1)
    * [update](#update)
    * [authenticate](#authenticate)
    * [delete](#delete-1)
    * [get](#get)
    * [exists](#exists)
- [__Firebase__](#firebase)
  - [__Firebase__](#firebase)
  - [__FireStore__](#firestore)
    * [list](#list)
    * [load](#load-1)
    * [load_collection](#load_collection)
    * [save](#save-1)
    * [delete](#delete-2)
  - [__Users-1__](#users)
    * [get](#get-1)
    * [create](#create-2)
    * [update](#update-1)
    * [delete](#delete-3)
    * [verify_id_token](#verify_id_token)
- [__Logging__](#logging)
  - [__Logging__](#logging)
    * [log](#log)
    * [load_logs](#load_logs)
    * [reset_logs](#reset_logs-1)
    * [log_to_file](#log_to_file)
  - [__Alerts__](#alerts)
    * [save](#save-2)
    * [check](#check)
    * [mark](#mark)
- [__Payments__](#payments)
  - [__Stripe__](#stripe)
    * [check](#check-1)
    * [get_product_id](#get_product_id)
    * [get_plan_id](#get_plan_id)
    * [get_product_id_by_plan_id](#get_product_id_by_plan_id)
    * [get_product_name](#get_product_name)
    * [get_plan_name](#get_plan_name)
  - [__Customers__](#customers)
    * [check](#check-2)
    * [create](#create-3)
    * [delete](#delete-4)
    * [get_id](#get_id)
    * [get](#get-2)
    * [get_cards](#get_cards)
    * [create_card](#create_card)
    * [delete_card](#delete_card)
  - [__Subscriptions__](#subscriptions)
    * [create](#create-4)
    * [get](#get-3)
    * [cancel](#cancel)
  - [__Plans__](#plans)
    * [get](#get-4)
    * [create](#create-5)
- [__Users__](#users)
  - [__Users-2__](#users)
    * [get](#get-5)
    * [create](#create-6)
    * [update](#update-2)
    * [delete](#delete-5)
    * [exists](#exists-1)
    * [authenticate](#authenticate-1)
    * [signout](#signout)
    * [authenticated](#authenticated)
    * [root_permission](#root_permission)
    * [load_data](#load_data)
    * [save_data](#save_data)
    * [send_email](#send_email)
    * [send_code](#send_code)
    * [verify_code](#verify_code)
    * [verify_api_key](#verify_api_key)
    * [verify_subscription](#verify_subscription)
    * [create_subscription](#create_subscription)
    * [get_api_key](#get_api_key)
    * [set_permission](#set_permission)
    * [check_password](#check_password)
    * [load_password](#load_password)
    * [save_password](#save_password)
    * [iterate](#iterate)
    * [synchronize](#synchronize)
- [__Views__](#views)
  - [__Request__](#request)
    * [success](#success)
    * [error](#error)
    * [response](#response)
    * [_403](#_403)
    * [_404](#_404)
    * [_500](#_500)
    * [_503](#_503)
    * [permission_denied](#permission_denied)
    * [maintenance](#maintenance)
  - [__View__](#view)
    * [render](#render)
    * [error](#error-1)
    * [_403](#_403-1)
    * [_404](#_404-1)
    * [_500](#_500-1)
    * [_503](#_503-1)
    * [permission_denied](#permission_denied-1)
    * [maintenance](#maintenance-1)
    * [template](#template)
- [__Website__](#website)
  - [__Security__](#security)
    * [generate_tls](#generate_tls-1)
    * [set_secret_env](#set_secret_env)
    * [get_secret_env](#get_secret_env)
  - [__Website__](#website)
    * [initialize](#initialize)
    * [cli](#cli)
    * [deploy](#deploy-2)
    * [check_dns](#check_dns-2)
    * [create](#create-7)
    * [serialize](#serialize)
    * [init_from_serialized](#init_from_serialized)
  - [__RateLimit__](#ratelimit)
    * [increment](#increment)
    * [verify](#verify)
  - [__Metrics__](#metrics)
    * [clean](#clean)
    * [requests](#requests)
    * [auth_requests](#auth_requests)
    * [disk_space](#disk_space)
    * [create_pie_graph](#create_pie_graph)
    * [create_line_graph](#create_line_graph)
    * [count_api_request](#count_api_request)
    * [count_web_request](#count_web_request)
    * [count_auth_request](#count_auth_request)
    * [count_request](#count_request)
  - [__Email__](#email)
    * [login](#login)
    * [send](#send)

## Database:
The database object class.
``` python 

# import the website.db object class.
import w3bsite

```

#### Functions:

##### load:
``` python

# call database.load.
response = database.load(path=None)

```
##### save:
``` python

# call database.save.
response = database.save(path=None, data=None, overwrite=False)

```
##### delete:
``` python

# call database.delete.
response = database.delete(path=None)

```
##### names:
``` python

# call database.names.
response = database.names(
    # the sub path (leave None to use the root path)
    path=None, )

```
##### subpath:
``` python

# call database.subpath.
_ = database.subpath(fullpath)

```
##### fullpath:
``` python

# call database.fullpath.
_ = database.fullpath(subpath)

```
##### join:
``` python

# call database.join.
_ = database.join(name=None, type="")

```

## VPS:
The vps object class.
``` python 

# import the website.vps object class.
import w3bsite

```

#### Functions:

##### configure:
``` python

# call vps.configure.
response = vps.configure(reinstall=False, log_level=0)

```
##### deploy:
``` python

# call vps.deploy.
response = vps.deploy(code_update=False, reinstall=False, log_level=0)

```

## Deployment:
The deployment object class.
``` python 

# import the website.deployment object class.
import w3bsite

```

#### Functions:

##### start:
``` python

# call deployment.start.
response = deployment.start(log_level=dev0s.defaults.options.log_level)

```
##### stop:
``` python

# call deployment.stop.
response = deployment.stop(log_level=dev0s.defaults.options.log_level)

```
##### restart:
``` python

# call deployment.restart.
response = deployment.restart(log_level=dev0s.defaults.options.log_level)

```
##### status:
``` python

# call deployment.status.
response = deployment.status(log_level=dev0s.defaults.options.log_level)

```
##### reset_logs:
``` python

# call deployment.reset_logs.
response = deployment.reset_logs(log_level=dev0s.defaults.options.log_level)

```
##### tail:
``` python

# call deployment.tail.
response = deployment.tail(nginx=False, debug=False)

```
##### configure:
``` python

# call deployment.configure.
response = deployment.configure(reinstall=False, log_level=0, loader=None)

```
##### deploy:
``` python

# call deployment.deploy.
response = deployment.deploy(code_update=False, reinstall=False, log_level=0)

```
##### generate_tls:
``` python

# call deployment.generate_tls.
response = deployment.generate_tls(log_level=0)

```
##### activate_tls:
``` python

# call deployment.activate_tls.
response = deployment.activate_tls(log_level=0)

```
##### bundle_tls:
``` python

# call deployment.bundle_tls.
response = deployment.bundle_tls(directory, log_level=0)

```
##### check_dns:
``` python

# call deployment.check_dns.
response = deployment.check_dns(log_level=0)

```

## Namecheap:
The namecheap object class.
``` python 

# import the website.namecheap object class.
import w3bsite

```

#### Functions:

##### check_domain:
``` python

# call namecheap.check_domain.
response = namecheap.check_domain(domain=None)

```
##### get_domains:
``` python

# call namecheap.get_domains.
response = namecheap.get_domains()

```
##### get_info:
``` python

# call namecheap.get_info.
response = namecheap.get_info(domain=None)

```
##### get_dns:
``` python

# call namecheap.get_dns.
response = namecheap.get_dns(domain=None)

```
##### check_dns:
``` python

# call namecheap.check_dns.
response = namecheap.check_dns(
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

# call namecheap.set_dns.
response = namecheap.set_dns(
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

# call namecheap.add_dns.
response = namecheap.add_dns(
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

# call namecheap.tag_dns.
response = namecheap.tag_dns(
    # the dns record type,
    type=None,
    # the dns record host,
    host=None,
    # the dns record value/address,
    value=None, )

```
##### get_sld_and_tld:
``` python

# call namecheap.get_sld_and_tld.
response = namecheap.get_sld_and_tld(domain=None)

```
##### get_tls:
``` python

# call namecheap.get_tls.
response = namecheap.get_tls()

```
##### create_tls:
``` python

# call namecheap.create_tls.
response = namecheap.create_tls(
    # the expiration years.
    years=2,
    # the tls type.
    type="PositiveSSL", )

```
##### activate_tls:
``` python

# call namecheap.activate_tls.
response = namecheap.activate_tls(
    # the certificate's id.
    certificate_id=None, )

```

## Django:
The django object class.
``` python 

# import the website.django object class.
import w3bsite

```

#### Functions:

##### start:
``` python

# call django.start.
response = django.start(host="127.0.0.1", port="8000", production=False)

```
##### create:
``` python

# call django.create.
response = django.create()

```
##### create_app:
``` python

# call django.create_app.
response = django.create_app(name="home")

```
##### migrations:
``` python

# call django.migrations.
response = django.migrations(forced=False, log_level=dev0s.defaults.options.log_level)

```
##### collect_static:
``` python

# call django.collect_static.
response = django.collect_static(log_level=dev0s.defaults.options.log_level)

```

## Users:
The users object class.
``` python 

# import the website.django.users object class.
import w3bsite

```

#### Functions:

##### create:
``` python

# call users.create.
response = users.create(
    username=None,
    email=None,
    password=None,
    name=None,
    superuser=False, )

```
##### update:
``` python

# call users.update.
response = users.update(
    # required.
    username=None,
    # optionals.
    email=None,
    password=None,
    name=None,
    superuser=None, )

```
##### authenticate:
``` python

# call users.authenticate.
response = users.authenticate(
    # the login credentials.
    username=None,
    password=None,
    # the request.
    request=None,
    # login the user.
    login=True, )

```
##### delete:
``` python

# call users.delete.
response = users.delete(username=None)

```
##### get:
``` python

# call users.get.
response = users.get(
    # select one of the following user id options:
    username=None,
    email=None, )

```
##### exists:
``` python

# call users.exists.
response = users.exists(
    # option 1:
    # by username (much faster).
    username=None,
    # option 2:
    # by email.
    email=None, )

```

## Firebase:
The firebase object class.
``` python 

# import the website.firebase object class.
import w3bsite

```
## FireStore:
The fire_store object class.
``` python 

# import the website.firebase.firestore object class.
import w3bsite

```

#### Functions:

##### list:
``` python

# call fire_store.list.
response = fire_store.list(reference)

```
##### load:
``` python

# call fire_store.load.
response = fire_store.load(reference)

```
##### load_collection:
``` python

# call fire_store.load_collection.
response = fire_store.load_collection(reference)

```
##### save:
``` python

# call fire_store.save.
response = fire_store.save(reference, data)

```
##### delete:
``` python

# call fire_store.delete.
response = fire_store.delete(reference)

```

## Users:
The users object class.
``` python 

# import the website.firebase.users object class.
import w3bsite

```

#### Functions:

##### get:
``` python

# call users.get.
response = users.get(
    # define one of the following parameters.
    uid=None,
    email=None,
    phone_number=None, )

```
##### create:
``` python

# call users.create.
response = users.create(
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

# call users.update.
response = users.update(
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

# call users.delete.
response = users.delete(
    # option 1:
    # the user's uid (much faster).
    uid=None,
    # option 2:
    # the users email / username.
    email=None, )

```
##### verify_id_token:
``` python

# call users.verify_id_token.
response = users.verify_id_token(id_token)

```

#### include_apps:
The w3bsite.classes.views.defaults.include_apps function.
``` python

# call w3bsite.classes.views.defaults.include_apps.
_ = w3bsite.classes.views.defaults.include_apps(apps=[], auto_include=False)

```
#### build_urls:
The w3bsite.classes.views.defaults.build_urls function.
``` python

# call w3bsite.classes.views.defaults.build_urls.
_ = w3bsite.classes.views.defaults.build_urls(views=[])

```
#### main:
The w3bsite.example.manage.main function.
``` python

# call w3bsite.example.manage.main.
_ = w3bsite.example.manage.main()

```
## Logging:
The logging object class.
``` python 

# import the website.logging object class.
import w3bsite

```

#### Functions:

##### log:
``` python

# call logging.log.
response = logging.log(
    # option 1:
    # the message (#1 param).
    message=None,
    # option 2:
    # the error.
    error=None,
    # option 3:
    # the response dict (leave message None to use).
    response={},
    # print the response as json.
    json=False,
    # optionals:
    # the active log level.
    log_level=0,
    # the required log level for when printed to console (leave None to use logging.log_level).
    required_log_level=None,
    # save to log file.
    save=False,
    # save errors always (for options 2 & 3 only).
    save_errors=None,
    # the log mode (leave None for default).
    mode=None, )

```
##### load_logs:
``` python

# call logging.load_logs.
response = logging.load_logs(format="webserver", options=["webserver", "cli", "array", "string"])

```
##### reset_logs:
``` python

# call logging.reset_logs.
response = logging.reset_logs(format="webserver", options=["webserver", "cli", "array", "string"])

```
##### log_to_file:
``` python

# call logging.log_to_file.
response = logging.log_to_file(message, raw=False)

```

## Alerts:
The alerts object class.
``` python 

# import the website.logging.alerts object class.
import w3bsite

```

#### Functions:

##### save:
``` python

# call alerts.save.
_ = alerts.save(
    # the alert's id (str).
    id="testalert",
    # the alert's title (str).
    title="Warning!",
    # the alert's message (str).
    message="Some message.",
    # the alert's right button redirect url (str).
    redirect="/dashboard/home/",
    # the alert's right button redirect text (str).
    redirect_button="Ok",
    # the alert's icon path.
    icon="/media/icons/warning.png",
    # the urls on which the alert will be shown (list) (use [*] for all urls).
    urls=["*"],
    # the users to which the alert will be shown (list) (use [*] for all users).
    users=["*"], )

```
##### check:
``` python

# call alerts.check.
response = alerts.check(
    # specific alert id's (str, list) (optional).
    id=None,
    # the active user (str) (optional).
    username=None,
    # the active url (str) (optional).
    url=None, )

```
##### mark:
``` python

# call alerts.mark.
_ = alerts.mark(
    # the alert's id.
    id=None,
    # the alert's timestamp.
    timestamp=None, )

```

## Stripe:
The stripe object class.
``` python 

# import the website.stripe object class.
import w3bsite

```

#### Functions:

##### check:
``` python

# call stripe.check.
response = stripe.check()

```
##### get_product_id:
``` python

# call stripe.get_product_id.
response = stripe.get_product_id(product=None)

```
##### get_plan_id:
``` python

# call stripe.get_plan_id.
response = stripe.get_plan_id(product=None, plan=None)

```
##### get_product_id_by_plan_id:
``` python

# call stripe.get_product_id_by_plan_id.
response = stripe.get_product_id_by_plan_id(plan_id)

```
##### get_product_name:
``` python

# call stripe.get_product_name.
response = stripe.get_product_name(id=None)

```
##### get_plan_name:
``` python

# call stripe.get_plan_name.
response = stripe.get_plan_name(id=None)

```

## Customers:
The customers object class.
``` python 

# import the website.stripe.customers object class.
import w3bsite

```

#### Functions:

##### check:
``` python

# call customers.check.
response = customers.check(
    # the users email.
    email=None, )

```
##### create:
``` python

# call customers.create.
response = customers.create(
    # the users email.
    email=None, )

```
##### delete:
``` python

# call customers.delete.
response = customers.delete(
    # the stripe customer id.
    id=None, )

```
##### get_id:
``` python

# call customers.get_id.
response = customers.get_id(
    # the users email.
    email=None, )

```
##### get:
``` python

# call customers.get.
response = customers.get(
    # the stripe customer id (optional).
    id=None, )

```
##### get_cards:
``` python

# call customers.get_cards.
response = customers.get_cards(
    # the stripe customer id.
    id=None, )

```
##### create_card:
``` python

# call customers.create_card.
response = customers.create_card(
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

# call customers.delete_card.
response = customers.delete_card(
    # the stripe customer id.
    id=None, )

```

## Subscriptions:
The subscriptions object class.
``` python 

# import the website.stripe.subscriptions object class.
import w3bsite

```

#### Functions:

##### create:
``` python

# call subscriptions.create.
response = subscriptions.create(
    # the email of the user that will be charged.
    email=None,
    customer_id=None, # instead of email for effienciency.
    # the plan ids (list).
    plans=[], )

```
##### get:
``` python

# call subscriptions.get.
response = subscriptions.get(
    # a specfic user email (optional).
    email=None,
    # active subscription plans only.
    active_only=True,
    # by customer id (custumer id as keys values in return).
    by_customer_id=False, )

```
##### cancel:
``` python

# call subscriptions.cancel.
response = subscriptions.cancel(
    # option 1:
    #     the stripe subscription id.
    subscription_id=None,
    # option 2:
    #     select a user identification option.
    email=None,
    #     the stripe plan id.
    plan=None, )

```

## Plans:
The plans object class.
``` python 

# import the website.stripe.plans object class.
import w3bsite

```

#### Functions:

##### get:
``` python

# call plans.get.
response = plans.get(
    # the plan id (plan_***) (optional).
    id=None,
    # get the subscriptions of the plan.
    get_subscriptions=False,
    # get active subscriptions only (required get_subscriptions=True).
    active_only=True, )

```
##### create:
``` python

# call plans.create.
response = plans.create(
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

## Users:
The users object class.
``` python 

# import the website.users object class.
import w3bsite

```

#### Functions:

##### get:
``` python

# call users.get.
_ = users.get(
    # define one of the following user id parameters.
    username=None,
    email=None, )

```
##### create:
``` python

# call users.create.
response = users.create(
    # required:
    username=None,
    email=None,
    password=None,
    # optionals:
    verify_password=None,
    name=None,
    superuser=False, )

```
##### update:
``` python

# call users.update.
response = users.update(
    # required:
    email=None,
    # optionals:
    name=None,
    password=None,
    verify_password=None,
    superuser=None,
    #phone_number=None,
    #photo_url=None,
    #email_verified=None, )

```
##### delete:
``` python

# call users.delete.
response = users.delete(
    # the user's email.
    email=None,
    # the user's username.
    username=None, )

```
##### exists:
``` python

# call users.exists.
_ = users.exists(
    # one of the user id options is required.
    username=None,
    email=None,
    # the filter (django).
    filter="django", )

```
##### authenticate:
``` python

# call users.authenticate.
response = users.authenticate(
    # the users username.
    username=None,
    # the users password.
    password=None,
    # the 2fa code.
    _2fa_code=None,
    # the 2fa enabled boolean.
    # leave None to use the users._2fa settings and specify to overwrite.
    _2fa=None,
    # the html for the verification code email (str).
    html="",
    # the request object.
    request=None, )

```
##### signout:
``` python

# call users.signout.
response = users.signout(
    # the request object (obj) (#1).
    request=None, )

```
##### authenticated:
``` python

# call users.authenticated.
response = users.authenticated(
    # the request (#1).
    request=None, )

```
##### root_permission:
``` python

# call users.root_permission.
response = users.root_permission(
    # the request (#1).
    request=None, )

```
##### load_data:
``` python

# call users.load_data.
response = users.load_data(
    # the user's email.
    email=None,
    # the user's username.
    username=None,
    # the create boolean (do not use).
    create=False, )

```
##### save_data:
``` python

# call users.save_data.
response = users.save_data(
    # the user's email.
    email=None,
    # the user's username.
    username=None,
    # the user's data.
    data={},
    # the overwrite boolean.
    overwrite=False, )

```
##### send_email:
``` python

# call users.send_email.
response = users.send_email(
    # define email to retrieve user.
    email=None,
    username=None,
    # the email title.
    title="Account Activation",
    # the html (str).
    html="", )

```
##### send_code:
``` python

# call users.send_code.
response = users.send_code(
    # define username / email to retrieve user.
    username=None,
    email=None,
    # the clients ip.
    ip="unknown",
    # the mode id.
    mode="verification",
    # the mode title.
    title="Account Activation",
    # the html (str).
    html="",
    # optionally specify the code (leave None to generate).
    code=None, )

```
##### verify_code:
``` python

# call users.verify_code.
response = users.verify_code(
    # define email to retrieve user.
    username=None,
    email=None,
    # the user entered code.
    code=000000,
    # the message mode.
    mode="verification", )

```
##### verify_api_key:
``` python

# call users.verify_api_key.
response = users.verify_api_key(api_key=None, request=None)

```
##### verify_subscription:
``` python

# call users.verify_subscription.
response = users.verify_subscription(
    # select one of the following user id options:
    email=None,
    username=None,
    api_key=None,
    # the subscription product.
    product=None,
    # the subscription plans that will return a success verification (["*"] for all plans within the product).
    plans=[], )

```
##### create_subscription:
``` python

# call users.create_subscription.
response = users.create_subscription(
    # select one of the following user id options:
    email=None,
    username=None,
    api_key=None,
    # the subscription product.
    product=None,
    # the subscription plan.
    plan=None,
    # the card holders name.
    card_name=None,
    # the card number.
    card_number=None,
    # the card expiration month.
    card_expiration_month=None,
    # the card expiration year.
    card_expiration_year=None,
    # the card cvc.
    card_cvc=None, )

```
##### get_api_key:
``` python

# call users.get_api_key.
response = users.get_api_key(email=None, username=None)

```
##### set_permission:
``` python

# call users.set_permission.
response = users.set_permission(email=None, username=None, permission_id=None, permission=True)

```
##### check_password:
``` python

# call users.check_password.
response = users.check_password(
    # password (#1).
    password=None,
    # verify password (#2).
    verify_password=None,
    # the strong password boolean.
    strong=False, )

```
##### load_password:
``` python

# call users.load_password.
response = users.load_password(email=None, username=None)

```
##### save_password:
``` python

# call users.save_password.
response = users.save_password(email=None, username=None, password=None)

```
##### iterate:
``` python

# call users.iterate.
_ = users.iterate(
    # the filter of what to iterate.
    filter="user",
    # from which database to iterate (django / database).
    database="database", )

```
##### synchronize:
``` python

# call users.synchronize.
response = users.synchronize(
    # leave ids=None default to synchronize all users.
    # optionally pass emails=[newuser@email.com] to synchronize new users.
    emails=["*"],
    usernames=["*"], )

```

## Request:
The request object class.
``` python 

# initialize the website.views.Request object class.
request = website.views.Request(
    # the base path (required; if url path is null) [#1 argument].
    base=None,
    # the requests id (required) [#2 argument].
    id=None,
    # the url path (optional).
    url=None,
    # the w3bsite.Website object (required).
    website=None,
    # authentication required.
    auth_required=False,
    # root permission required.
    root_required=False, )

```

#### Functions:

##### success:
``` python

# call request.success.
response = request.success(message, arguments={})

```
##### error:
``` python

# call request.error.
response = request.error(error)

```
##### response:
``` python

# call request.response.
response = request.response(response)

```
##### _403:
``` python

# call request._403.
_ = request._403(request=None)

```
##### _404:
``` python

# call request._404.
_ = request._404(request=None, error=None)

```
##### _500:
``` python

# call request._500.
_ = request._500(request=None, error=None)

```
##### _503:
``` python

# call request._503.
_ = request._503(request=None)

```
##### permission_denied:
``` python

# call request.permission_denied.
_ = request.permission_denied(request=None)

```
##### maintenance:
``` python

# call request.maintenance.
_ = request.maintenance(request=None)

```

## View:
The view object class.
``` python 

# initialize the website.views.View object class.
view = website.views.View(
    # the base path (required; if url path is null) [#1 argument].
    base=None,
    # the views id (required) [#2 argument].
    id=None,
    # the url path (optional).
    url=None,
    # the html path (optional).
    html=None,
    # the w3bsite.Website object (required).
    website=None,
    # enable if this view is the [/] landing page.
    landing_page=False,
    # authentication required.
    auth_required=False,
    # root permission required.
    root_required=False,
    # the object type (do not edit).
    type="View", )

```

#### Functions:

##### render:
``` python

# call view.render.
_ = view.render(
    # the request (obj) (#1)
    request,
    # overwrite default template data. #2
    template_data=None,
    # overwrite default html #3.
    html=None,
    # the response's status code.
    status=200, )

```
##### error:
``` python

# call view.error.
_ = view.error(
    # the django request parameter.
    request,
    # the error title.
    title="Warning!",
    # the error title.
    message="Some error occured.",
    # the error icon (the static directory is root).
    icon="media/icons/warning.png",
    # the redirect button text (right button).
    redirect_button="Ok",
    # the redirect url.
    redirect="/dashboard/home/",
    # overwrite default template data.
    template_data=None,
    # pass arguments by dict.
    serialized={}, )

```
##### _403:
``` python

# call view._403.
_ = view._403(request, template_data=None)

```
##### _404:
``` python

# call view._404.
_ = view._404(request, template_data=None)

```
##### _500:
``` python

# call view._500.
_ = view._500(request, template_data=None, error=None)

```
##### _503:
``` python

# call view._503.
_ = view._503(request, template_data=None)

```
##### permission_denied:
``` python

# call view.permission_denied.
_ = view.permission_denied(request, template_data=None)

```
##### maintenance:
``` python

# call view.maintenance.
_ = view.maintenance(request, template_data=None)

```
##### template:
``` python

# call view.template.
_ = view.template(new={}, old=None, safe=False)

```

## Security:
The security object class.
``` python 

# import the website.security object class.
import w3bsite

```

#### Functions:

##### generate_tls:
``` python

# call security.generate_tls.
response = security.generate_tls()

```
##### set_secret_env:
``` python

# call security.set_secret_env.
response = security.set_secret_env(key, value)

```
##### get_secret_env:
``` python

# call security.get_secret_env.
_ = security.get_secret_env(key, default=None, required=True)

```

## Website:
The website object class.
``` python 

# initialize the w3bsite.Website object class.
website = w3bsite.Website(
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
    #     sending emails [https://gmail.com > Security > Enable Unsafe 3th party applications / generate an app password (advised)].
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
    #     debug mode.
    debug=False,
    #     the users sub path.
    users_subpath="users/",
    #     id users by username.
    id_by_username=True,
    #
    # the logs.
    log_level=dev0s.defaults.options.log_level,
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

## RateLimit:
The rate_limit object class.
``` python 

# import the website.ratelimit object class.
import w3bsite

```

#### Functions:

##### increment:
``` python

# call rate_limit.increment.
response = rate_limit.increment(
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

# call rate_limit.verify.
response = rate_limit.verify(
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

## Metrics:
The metrics object class.
``` python 

# import the website.metrics object class.
import w3bsite

```

#### Functions:

##### clean:
``` python

# call metrics.clean.
response = metrics.clean()

```
##### requests:
``` python

# call metrics.requests.
response = metrics.requests()

```
##### auth_requests:
``` python

# call metrics.auth_requests.
response = metrics.auth_requests()

```
##### disk_space:
``` python

# call metrics.disk_space.
response = metrics.disk_space(mode="GB")

```
##### create_pie_graph:
``` python

# call metrics.create_pie_graph.
_ = metrics.create_pie_graph(
    # the data.
    data={
        "Used (GB)":15,
        "Free (GB)":3,
    },
    # the key's colors.
    colors={
        "Used (GB)": "#FD304E",
        "Free (GB)": "#323B8390",
    },
    # the keys to keep.
    keep=["*"],
    # fill background color.
    fill=False, )

```
##### create_line_graph:
``` python

# call metrics.create_line_graph.
_ = metrics.create_line_graph(
    # the data.
    data={
        "$timestamp":{
            "active":10,
            "non_active":3,
        },
    },
    # the key's colors.
    colors={
        "active":"#323B83",
        "non_active":"#FD304E",
    },
    # the keys to keep.
    keep=["*"],
    # fill background color.
    fill=False, )

```
##### count_api_request:
``` python

# call metrics.count_api_request.
_ = metrics.count_api_request(request, data={})

```
##### count_web_request:
``` python

# call metrics.count_web_request.
_ = metrics.count_web_request(request, data={})

```
##### count_auth_request:
``` python

# call metrics.count_auth_request.
_ = metrics.count_auth_request(request, data={})

```
##### count_request:
``` python

# call metrics.count_request.
response = metrics.count_request(request, id=None, data={"url":None}, save=False)

```

## Email:
The email object class.
``` python 

# import the website.users.email object class.
import w3bsite

```

#### Functions:

##### login:
``` python

# call email.login.
response = email.login(timeout=3)

```
##### send:
``` python

# call email.send.
response = email.send(
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

