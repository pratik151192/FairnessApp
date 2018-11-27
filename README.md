# FairnessApp

Created a web-based social network between humans and bots where the users are asked to 
provide preferences whether they want to tag or be tagged in a specific post. The model in the background uses Game Theory 
techniques to evaluate the fairness of the system, and to observe whether users compromise towards a neutral privacy setting
after rounds of repeated negotiations in their network.

Want to play?

https://floating-bastion-32116.herokuapp.com/

## 1. Prerequisites

This project requires Python 3.6 with pip3

```
$ sudo pip3 install --ignore-installed  asn1crypto==0.23.0 boto3==1.5.0 botocore==1.8.14 certifi==2017.7.27.1 cfe==0.0.15 cffi==1.11.2 chardet==3.0.4   Click==6.6 cmake==0.8.0 colorama==0.3.9 confusable-homoglyphs==2.0.2 cryptography==2.1.1 cycler==0.10.0 decorator==4.1.2 dj-database-url==0.4.2 dj-static==0.0.6 Django==1.11.6 django-bootstrap-form==3.3 django-registration==2.3 django-storages==1.6.5 django-toolbelt==0.0.1  docutils==0.14 fdb==1.8 Flask==0.12.2 Flask-MySQL==1.4.0 gunicorn==19.7.1 idna==2.6 instagram-scraper==1.5.3 ipython==6.1.0  ipython-genutils==0.2.0 itsdangerous==0.24 jedi==0.10.2 Jinja2==2.9.6 jmespath==0.9.3 jsonschema==2.6.0 jupyter-core==4.3.0 MarkupSafe==1.0 matplotlib==2.0.2 mongo==0.2.0 nbformat==4.4.0 networkx==1.11 numpy==1.13.1 oauthlib==2.0.4 olefile==0.44 optional-django==0.1.0 pickleshare==0.7.4 Pillow==4.3.0 plotly==2.0.15 prompt-toolkit==1.0.15 psycopg2==2.7.3.2 pycares==2.3.0 pycparser==2.18 pygame==1.9.3 Pygments==2.2.0 pymongo==3.5.1 PyMySQL==0.7.11 pyOpenSSL==17.3.0 pyparsing==2.2.0 pysolr==3.6.0 pytagcloud==0.3.5 python-dateutil==2.6.1 pytz==2017.2 requests==2.18.4 requests-oauthlib==0.8.0 s3transfer==0.1.12 simplegeneric==0.8.1 simplejson==3.11.1  six==1.10.0 static3==0.7.0 tqdm==4.15.0 traitlets==4.3.2 tweepy==3.5.0 twitter==1.17.1 twython==3.6.0 urllib3==1.22 virtualenv==15.1.0 watson-developer-cloud==0.26.1 wcwidth==0.1.7 Werkzeug==0.12.2 whitenoise==3.3.1 wordcloud==1.3sudo pip install --ignore-installed  asn1crypto==0.23.0 boto3==1.5.0 botocore==1.8.14 certifi==2017.7.27.1 cfe==0.0.15 cffi==1.11.2 chardet==3.0.4   Click==6.6 cmake==0.8.0 colorama==0.3.9 confusable-homoglyphs==2.0.2 cryptography==2.1.1 cycler==0.10.0 decorator==4.1.2 dj-database-url==0.4.2 dj-static==0.0.6 Django==1.11.6 django-bootstrap-form==3.3 django-registration==2.3 django-storages==1.6.5 django-toolbelt==0.0.1  docutils==0.14 fdb==1.8 Flask==0.12.2 Flask-MySQL==1.4.0 gunicorn==19.7.1 idna==2.6 instagram-scraper==1.5.3 ipython==6.1.0  ipython-genutils==0.2.0 itsdangerous==0.24 jedi==0.10.2 Jinja2==2.9.6 jmespath==0.9.3 jsonschema==2.6.0 jupyter-core==4.3.0 MarkupSafe==1.0 matplotlib==2.0.2 mongo==0.2.0 nbformat==4.4.0 networkx==1.11 numpy==1.13.1 oauthlib==2.0.4 olefile==0.44 optional-django==0.1.0 pickleshare==0.7.4 Pillow==4.3.0 plotly==2.0.15 prompt-toolkit==1.0.15 psycopg2==2.7.3.2 pycares==2.3.0 pycparser==2.18 pygame==1.9.3 Pygments==2.2.0 pymongo==3.5.1 PyMySQL==0.7.11 pyOpenSSL==17.3.0 pyparsing==2.2.0 pysolr==3.6.0 pytagcloud==0.3.5 python-dateutil==2.6.1 pytz==2017.2 requests==2.18.4 requests-oauthlib==0.8.0 s3transfer==0.1.12 simplegeneric==0.8.1 simplejson==3.11.1  six==1.10.0 static3==0.7.0 tqdm==4.15.0 traitlets==4.3.2 tweepy==3.5.0 twitter==1.17.1 twython==3.6.0 urllib3==1.22 virtualenv==15.1.0 watson-developer-cloud==0.26.1 wcwidth==0.1.7 Werkzeug==0.12.2 whitenoise==3.3.1 wordcloud==1.3.1.1
```

## 2. Execution

Please execute it with:

```
$ python3 manage.py runserver
```

Note: The logic behind the users compromising or negotiating in the network is published here:

