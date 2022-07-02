"""
Django settings for geodjango project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import django_heroku
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
#from RAJVEL plain english
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ID = 1
#added from stack https://stackoverflow.com/questions/1926049/django-templatedoesnotexist 
# SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#os.path.join(BASE_DIR, 'staticfiles'
with open(BASE_DIR + '/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# with open('../secret_key.txt') as f:
#     SECRET_KEY = f.read().strip()
    
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = [
    '80','localhost',
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8080/',
    '127.0.0.1:8080/',
    '127.0.0.1:8000/',
  '127.0.0.1',
  '111.222.333.444',
  'http://str-airbnb-policy-florence.herokuapp.com/',
  'www.str-airbnb-policy-florence.herokuapp.com',
  '.str-airbnb-policy-florence.herokuapp.com',
  'https://str-airbnb-policy-florence.herokuapp.com/'
  '*'
]



# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    # 'world',
    'world.apps.WorldConfig',
    'csvimport.app.CSVImportConf',
    'coverage',
    'django_nose',
    'freeze' #couldn't do this in the end because needed django version 1.6.5 but when we deprecated all sorts of issues happened and couldn't run the script from freeze

]

# DJANGO_SETTINGS_MODULE = geodjango.settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'geodjango_tut.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        ## Find templates in the same folder as settings.py.
        #https://stackoverflow.com/questions/1926049/django-templatedoesnotexist
        # 'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
        'DIRS': [SETTINGS_PATH + 'templates'], #BASE_DIR + '/templates/' from RAJVEL example
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'geodjango_tut.wsgi.application'

# SECURE_HSTS_SECONDS = True #If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems. 
SECURE_SSL_REDIRECT = False #True when in production or if want to allow non ssl 
#For deployment no cookie 
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
#should add these to gitignore
# /Users/stateofplace/new_codes/geodjango_tut/
with open(BASE_DIR +'/db_pass.txt') as f:
    PASSWORD = f.read().strip()

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'taylor',
        'PASSWORD': PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432'
     }
}




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#maybe change DISABLE_COLLECTSTATIC to not be set?

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=foo,bar',
]

django_heroku.settings(locals())