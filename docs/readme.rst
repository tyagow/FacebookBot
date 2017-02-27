=============================
Django Base
=============================


.. image:: https://travis-ci.org/tyagow/django-base.svg?branch=master
    :target: https://travis-ci.org/tyagow/django-base

Documentation
-------------

The full documentation is at http://django-base.readthedocs.io.

Live demo @ http://django-base.104.236.104.21.xip.io

Quickstart
----------

1. Clone o repositório.
2. Crie um virutalenv com o Python 3.5
3. Ative o Virtualenv.
4. Instale as dependencias.
5. Configure a instancia com o .env
6. Migre seus modelos para o Banco de Dados
7. Roda o collectstatic para configurar arquivos staticos
8. Execute os testes.

Digite no terminal::

    git clone https://github.com/tyagow/django-base.git Nome-Do-Projeto
    cd Nome-Do-Projeto
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp contrib/env-sample .env
    python manage.py collectstatic
    python manage.py migrate
    python manage.py test
    python manage.py runserver


Como fazer o Deploy?
---------------------------

1. Install Digital Ocean Dokku image
2. Send your ssh-key to dokku
3. Connect via ssh to your server
4. Create app in dokku
5. Install postgres plugin in dokku
6. Create database for your app in dokku
7. Link database and app in dokku
8. Set DEBUG in dokku
9. Generate new SECRET_KEY
10. Set SECRET_KEY in dokku
11. Set ALLOWED_HOSTS in dokku
12. Set Global Domain dor dokku
13. Push your code to dokku
14. Run the migrations
15. Collect static data with DEBUG=False

Digite no terminal ::

    (local) cat ~/.ssh/id_rsa.pub | ssh root@<your.ip.address> "sudo sshcommand acl-add dokku [description]"
    (local) ssh root@<your.ip.address>
    (server) dokku apps:create <app-name>
    (server) sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
    (server) dokku postgres:create <database-name>
    (server) dokku postgres:link <databse-name> <app-name>
    (local) git remote add dokku dokku@dokku.me:<app-name>
    (local) ssh dokku@<your.ip.address> config:set <app-name> DEBUG=False
    (local) python contrib/secret_gen.py
    (local) ssh dokku@<your.ip.address> config:set <app-name> SECRET_KEY='<new-generated-key>'
    (local) ssh dokku@<your.ip.address> config:set <app-name> ALLOWED_HOSTS=<app-name>.<your.ip.address>.xip.io
    (local) ssh dokku@<your.ip.address> config:set <app-name> AWS_STORAGE_BUCKET_NAME=XXXXXXXXXXX AWS_ACCESS_KEY_ID=XXXXXXXXXXX AWS_SECRET_ACCESS_KEY=XXXXXXXXXXX
    (local) ssh dokku@<your.ip.address> domains:add-global <your.ip.address>.xip.io
    (local) ssh dokku@<your.ip.address> domains:enable <app-name>
    (local) git push dokku master
    (local) ssh dokku@<your.ip.address> run <app-name> python manage.py migrate
    (local) DEBUG=False python manage.py collectstatic


**NOTES**

* Depois do primeiro deploy feito basta um comando para o deploy:

`git push dokku master`

* Não esquecer de migrar/atualizar o banco de dados sempre que alterar um modelo:

`ssh dokku@<your.ip.address> run <app-name> python manage.py migrate`

* http://dokku.viewdocs.io/dokku/deployment/application-deployment/

**Dokku**
* Change PORT
`
(não recomendado, se configurar na porta 80 só poderei ter 1 serviço (app) )
" you can only bind a single service to port 80 if you do not use a vhost
but i highly suggest using a vhost for your server
so then you get urls like
app.vhost.com " @ savant`

`
dokku config:set APP DOKKU_NGINX_PORT=80 DOKKU_PROXY_PORT_MAP=http:80:5000
`

* Configurar um vhost
`dokku domains:add-global domain_here`

* Re-enable vhosts for your app
( http://dokku.viewdocs.io/dokku/configuration/domains/ )
`dokku domains:enable APP`

**Configurar AmazonS3**

* https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/


Features
--------

* Django 1.10.5
* Bootstrap 3.3.7
* JQuery 3.1.1
* Python Decouple
* DJ Static (serving static files locally)
* Dj Database URL
* Django test without migrations
* Django Crispy Forms
* Django bootstrap3
* Social User Login App* (facebook e twitter)
* Django Extensions
* Dokku pre configured
* Multi languange i18n

**Need additional configuration**

Social Auth
------------

* **Adicionar ao INSTALLED_APPS**
::

  'social_django',

* **Adicionar ao settings.py**
::

  AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
  )

* **Adicionar ao requirements.txt**

::

 social-auth-app-django

* **Adicionar ao urls.py**
::

  url('', include('social_django.urls', namespace='social'))

* **Adicionar ao MIDDLEWARE_CLASSES**
::

    'social_django.middleware.SocialAuthExceptionMiddleware',

* **Adicionar ao TEMPLATES**
::

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

* **Configurar variaveis no .env e no servidor**
::

    SOCIAL_AUTH_TWITTER_KEY=
    SOCIAL_AUTH_TWITTER_SECRET=
    SOCIAL_AUTH_FACEBOOK_KEY=
    SOCIAL_AUTH_FACEBOOK_SECRET=

* **Configurar o HOST no App do Facebook**

* **Uncomment buttons to social login in registration/login.html**

* Tutorial: https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html

Running Tests
--------------

Does the code actually work?

::

    source .venv/bin/activate
    (myenv) $ python manage.py test


