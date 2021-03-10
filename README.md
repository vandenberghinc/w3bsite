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
  * [Code Examples](#code-examples)

# Description:
Website library.

# Installation:
Install the package.

	pip3 install w3bsite --upgrade

## Troubleshooting:

#### Apple Silicon M1:

##### Failed to install grpcio
	arch -arch x86_64 /usr/bin/python3 -m pip install firebase-admin

## Setup.

#### Namecheap.
1: Go to https://namecheap.com and sign up / sign in.  <br>
2: Link a credit card to your account. <br>
3: $50 balance is required to activate the developer api, so add balance if you did not reach this limit yet. <br>
4: Enable the developer API. <br>
5: Whitelist your public ip (https://aruljohn.com). <br>
6: Note / copy the api key which will be required later. <br>

#### /.website.py
Create a file named "website.py" in your websites root directory.
	
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
- [__Defaults__](#defaults)
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
- [__FirebaseCLI__](#firebasecli)
  * [install](#install)
  * [installed](#installed)
  * [login](#login-1)
  * [projects](#projects)
- [__Git__](#git)
  * [installed](#installed-1)
  * [install](#install-1)
  * [pull](#pull)
- [__HelloWorld__](#helloworld)
  * [view](#view)
- [__HelloWorldSmall__](#helloworldsmall)
  * [view](#view-1)
- [__Heroku__](#heroku)
  * [check](#check-1)
  * [tail](#tail-1)
  * [add_environment_variables](#add_environment_variables)
  * [remove_environment_variables](#remove_environment_variables)
  * [get_environment_variables](#get_environment_variables)
  * [push](#push)
  * [get_deploy_app](#get_deploy_app)
  * [get_deploy_domain](#get_deploy_domain)
  * [get_domains](#get_domains)
  * [check_domain](#check_domain)
  * [add_domain](#add_domain)
  * [check_logged_in](#check_logged_in)
  * [install_tls](#install_tls)
  * [check_dns](#check_dns-1)
  * [deploy](#deploy-1)
- [__Home__](#home)
  * [view](#view-2)
- [__Logging__](#logging)
  * [log](#log)
- [__Namecheap__](#namecheap)
  * [check_domain](#check_domain-1)
  * [get_domains](#get_domains-1)
  * [get_info](#get_info)
  * [get_dns](#get_dns)
  * [check_dns](#check_dns-2)
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
- [__Products__](#products)
  * [get](#get-2)
  * [create](#create-3)
- [__RateLimit__](#ratelimit)
  * [increment](#increment)
  * [verify](#verify)
- [__Request__](#request)
  * [view](#view-3)
  * [success](#success)
  * [error](#error)
  * [response](#response)
  * [maintenance](#maintenance)
  * [permission_denied](#permission_denied)
- [__Security__](#security)
  * [generate_tls](#generate_tls-1)
  * [set_secret_env](#set_secret_env)
  * [get_secret_env](#get_secret_env)
- [__Stripe__](#stripe)
  * [check](#check-2)
  * [get_product_id](#get_product_id)
  * [get_plan_id](#get_plan_id)
  * [get_product_id_by_plan_id](#get_product_id_by_plan_id)
  * [get_product_name](#get_product_name)
  * [get_plan_name](#get_plan_name)
- [__Subscriptions__](#subscriptions)
  * [create](#create-4)
  * [get](#get-3)
  * [cancel](#cancel)
- [__TemplateData__](#templatedata)
  * [raw](#raw)
- [__Users__](#users)
  * [get](#get-4)
  * [create](#create-5)
  * [update](#update)
  * [delete](#delete-3)
  * [verify_id_token](#verify_id_token)
- [__VPS__](#vps)
  * [configure](#configure-1)
  * [deploy](#deploy-2)
- [__View__](#view)
  * [view](#view-4)
  * [render](#render)
  * [error](#error-1)
  * [maintenance](#maintenance-1)
  * [permission_denied](#permission_denied-1)
- [__Website__](#website)
  * [initialize](#initialize)
  * [cli](#cli)
  * [deploy](#deploy-3)
  * [check_dns](#check_dns-3)
  * [create](#create-6)
  * [serialize](#serialize)
  * [init_from_serialized](#init_from_serialized)
  * [template](#template)

## Customers:
The customers object class.
``` python 

# initialize the customers object class.
customers = Customers(defaults=None)

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

## Database:
The database object class.
``` python 

# initialize the database object class.
database = Database(firestore=None, path=None, live=False)

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
response = database.delete(path=None, data=None)

```
##### join:
``` python

# call database.join.
_ = database.join(path)

```
##### names:
``` python

# call database.names.
_ = database.names(
    # the sub path (leave None to use the root path)
    path=None, )

```

## Defaults:
The defaults object class.
``` python 

# initialize the defaults object class.
defaults = Defaults(
    # info.
    root=None,
    library=None,
    database=None,
    name=None,
    domain=None,
    https_domain=None,
    author=None,
    email=None,
    country_code=None,
    province=None,
    city=None,
    organization=None,
    organization_unit=None,
    developers=None,
    remote=None,
    live=True,
    interactive=False,
    _2fa=False,
    maintenance=False,
    users_subpath="users/",
    id_by_username=True,
    template_data={},
    # objects.
    aes=None,
    logging=None,
    # defaults.
    traceback="w3bsite.Website.defaults", )

```
## Deployment:
The deployment object class.
``` python 

# initialize the deployment object class.
deployment = Deployment(
    # the root path.
    root=None,
    # the library path.
    library=None,
    # the website name.
    name=None,
    # the domain.
    domain=None,
    # the database path.
    database=None,
    # the remote.
    remote=None,
    # the vps ip (if remote is vps else leave default).
    vps_ip=None,
    vps_username=None,
    # the organization's email.
    email=None,
    country_code="NL",
    province="Amsterdam",
    city="Amsterdam",
    organization=None,
    organization_unit="IT",
    # the organization info.
    # objects.
    namecheap=None, )

```

#### Functions:

##### start:
``` python

# call deployment.start.
response = deployment.start()

```
##### stop:
``` python

# call deployment.stop.
response = deployment.stop()

```
##### restart:
``` python

# call deployment.restart.
response = deployment.restart()

```
##### status:
``` python

# call deployment.status.
response = deployment.status()

```
##### reset_logs:
``` python

# call deployment.reset_logs.
response = deployment.reset_logs()

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

## Django:
The django object class.
``` python 

# initialize the django object class.
django = Django(
    # the security object.
    security=None,
    # defaults.
    defaults=None, )

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
response = django.migrations(forced=False, log_level=Defaults.options.log_level)

```
##### collect_static:
``` python

# call django.collect_static.
response = django.collect_static(log_level=Defaults.options.log_level)

```

## Email:
The email object class.
``` python 

# initialize the email object class.
email = Email(
    email=None, # must be first parameter.
    password=None, # must be second parameter.
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    use_tls=True,
    visible_email=None, )

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

## FireStore:
The fire_store object class.
``` python 

# initialize the fire_store object class.
fire_store = FireStore()

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

## Firebase:
The firebase object class.
``` python 

# initialize the firebase object class.
firebase = Firebase(
    # the firebase key.
    key=None,
    # the firebase js config.
    firebase_js={},
    # defaults.
    defaults=None, )

```
## FirebaseCLI:
The firebasecli object class.
``` python 

# initialize the firebasecli object class.
firebasecli = FirebaseCLI()

```

#### Functions:

##### install:
``` python

# call firebasecli.install.
_ = firebasecli.install()

```
##### installed:
``` python

# call firebasecli.installed.
_ = firebasecli.installed()

```
##### login:
``` python

# call firebasecli.login.
_ = firebasecli.login()

```
##### projects:
``` python

# call firebasecli.projects.
_ = firebasecli.projects()

```

## Git:
The git object class.
``` python 

# initialize the git object class.
git = Git(
    # defaults.
    defaults=None, )

```

#### Functions:

##### installed:
``` python

# call git.installed.
response = git.installed()

```
##### install:
``` python

# call git.install.
response = git.install()

```
##### pull:
``` python

# call git.pull.
response = git.pull(title="Updates", message="updates.")

```

## HelloWorld:
The hello_world object class.
``` python 

# initialize the hello_world object class.
hello_world = HelloWorld()

```

#### Functions:

##### view:
``` python

# call hello_world.view.
_ = hello_world.view(request)

```

## HelloWorldSmall:
The hello_world_small object class.
``` python 

# initialize the hello_world_small object class.
hello_world_small = HelloWorldSmall()

```

#### Functions:

##### view:
``` python

# call hello_world_small.view.
_ = hello_world_small.view(request)

```

## Heroku:
The heroku object class.
``` python 

# initialize the heroku object class.
heroku = Heroku(
    # the root path.
    root=None,
    # the domain.
    doman=None,
    # the website name.
    name=None,
    # passed objects.
    namecheap=None,
    logging=None, )

```

#### Functions:

##### check:
``` python

# call heroku.check.
_ = heroku.check()

```
##### tail:
``` python

# call heroku.tail.
_ = heroku.tail()

```
##### add_environment_variables:
``` python

# call heroku.add_environment_variables.
response = heroku.add_environment_variables(variables={}, silent=True)

```
##### remove_environment_variables:
``` python

# call heroku.remove_environment_variables.
_ = heroku.remove_environment_variables(variables={})

```
##### get_environment_variables:
``` python

# call heroku.get_environment_variables.
_ = heroku.get_environment_variables(variables={})

```
##### push:
``` python

# call heroku.push.
response = heroku.push(log_level=0)

```
##### get_deploy_app:
``` python

# call heroku.get_deploy_app.
response = heroku.get_deploy_app()

```
##### get_deploy_domain:
``` python

# call heroku.get_deploy_domain.
response = heroku.get_deploy_domain(
    # the heroku app name (optional to increase speed).
    app=None, )

```
##### get_domains:
``` python

# call heroku.get_domains.
response = heroku.get_domains()

```
##### check_domain:
``` python

# call heroku.check_domain.
response = heroku.check_domain(domain=None)

```
##### add_domain:
``` python

# call heroku.add_domain.
response = heroku.add_domain(domain=None)

```
##### check_logged_in:
``` python

# call heroku.check_logged_in.
response = heroku.check_logged_in()

```
##### install_tls:
``` python

# call heroku.install_tls.
response = heroku.install_tls(
    # the heroku app name (optional to increase speed).
    app=None, )

```
##### check_dns:
``` python

# call heroku.check_dns.
response = heroku.check_dns(log_level=0)

```
##### deploy:
``` python

# call heroku.deploy.
response = heroku.deploy(log_level=0)

```

## Home:
The home object class.
``` python 

# initialize the home object class.
home = Home()

```

#### Functions:

##### view:
``` python

# call home.view.
_ = home.view(request)

```

## Logging:
The logging object class.
``` python 

# initialize the logging object class.
logging = Logging(name=None, root=None, database=None)

```

#### Functions:

##### log:
``` python

# call logging.log.
_ = logging.log(
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
The namecheap object class.
``` python 

# initialize the namecheap object class.
namecheap = Namecheap(
    # your namecheap username.
    username=None,
    # your namecheap api key.
    api_key=None,
    # the root path.
    root=None,
    # the domain.
    domain=None,
    # the organization's email.
    email=None,
    # sandbox boolean (does not seem to work namecheap end).
    sandbox=False, )

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

## Plans:
The plans object class.
``` python 

# initialize the plans object class.
plans = Plans(defaults=None, subscriptions=None)

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

## Products:
The products object class.
``` python 

# initialize the products object class.
products = Products(defaults=None, plans=None)

```

#### Functions:

##### get:
``` python

# call products.get.
response = products.get(
    # the product id (prod_***) (optional).
    id=None,
    # get the plans of each products.
    get_plans=False,
    # get the subscription of each plan (requires get_plans=True).
    get_subscriptions=False,
    # get active subscriptions only (required get_subscriptions=True).
    active_only=True, )

```
##### create:
``` python

# call products.create.
response = products.create(
    # the product id.
    id=None,
    # the product desciption.
    description=None, )

```

## RateLimit:
The rate_limit object class.
``` python 

# initialize the rate_limit object class.
rate_limit = RateLimit(
    # objects.
    db=None,
    # defaults.
    defaults=None, )

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

## Request:
The request object class.
``` python 

# initialize the request object class.
request = Request(
    # the base path (required; if url path is null) [#1 argument].
    base=None,
    # the requests id (required) [#2 argument].
    id=None,
    # the url path (optional).
    url=None,
    # template data (optional).
    template_data={}, )

```

#### Functions:

##### view:
``` python

# call request.view.
_ = request.view(request)

```
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
_ = request.response(response)

```
##### maintenance:
``` python

# call request.maintenance.
response = request.maintenance(request=None)

```
##### permission_denied:
``` python

# call request.permission_denied.
_ = request.permission_denied(request=None)

```

## Security:
The security object class.
``` python 

# initialize the security object class.
security = Security(
    # optional if defaults not initialized.
    root=None,
    # defaults (optional).
    defaults=None, )

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

## Stripe:
The stripe object class.
``` python 

# initialize the stripe object class.
stripe = Stripe(
    # the stripe secret key.
    secret_key=None,
    #     the stripe publishable key.
    publishable_key=None,
    # the default subscription plans.
    subscriptions=None,
    # the default products.
    products=None,
    # defaults.
    defaults=None, )

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

## Subscriptions:
The subscriptions object class.
``` python 

# initialize the subscriptions object class.
subscriptions = Subscriptions(defaults=None, customers=None)

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

## TemplateData:
The template_data object class.
``` python 

# initialize the template_data object class.
template_data = TemplateData(data={})

```

#### Functions:

##### raw:
``` python

# call template_data.raw.
_ = template_data.raw()

```

## Users:
The users object class.
``` python 

# initialize the users object class.
users = Users(defaults=None, firestore=None)

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

## VPS:
The vps object class.
``` python 

# initialize the vps object class.
vps = VPS(
    # the remote ip address.
    ip=None,
    # the remote ssh port.
    port=22,
    # the remote username.
    username=None,
    # passed objects.
    namecheap=None,
    deployment=None,
    # defaults.
    defaults=None, )

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

## View:
The view object class.
``` python 

# initialize the view object class.
view = View(
    # the base path (required; if url path is null) [#1 argument].
    base=None,
    # the views id (required) [#2 argument].
    id=None,
    # the url path (optional).
    url=None,
    # the html path (optional).
    html=None,
    # enable if this view is the [/] landing page.
    landing_page=False,
    # the template data (required).
    template_data={},
    # the object type (do not edit).
    type="View", )

```

#### Functions:

##### view:
``` python

# call view.view.
_ = view.view(request)

```
##### render:
``` python

# call view.render.
_ = view.render(request,
    # overwrite default template data. #2
    template_data=None,
    # overwrite default html #3.
    html=None, )

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
    template_data=None)

```
##### maintenance:
``` python

# call view.maintenance.
_ = view.maintenance(request, template_data=None)

```
##### permission_denied:
``` python

# call view.permission_denied.
_ = view.permission_denied(request, template_data=None)

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
        #"nas-server": {
        #    "basic": {
        #        "rank":1,
        #        "price":50,
        #        "currency":"eur",
        #        "favicon":"https://raw.githubusercontent.com/vandenberghinc/public-storage/master/nas-server/icon/icon.png"
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
        #"nas-server": {
        #    "basic": {
        #        "rank":1,
        #        "price":50,
        #        "currency":"eur",
        #        "favicon":"https://raw.githubusercontent.com/vandenberghinc/public-storage/master/nas-server/icon/icon.png"
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
