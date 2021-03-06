"""
Django settings for knowvi_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

# E-mail connectivity
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Absolute path to templates folder
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

# Absolute path to static folder
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')

# Absolute path to media folder
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# Absolute path to database
DATABASE_PATH = os.path.join(PROJECT_PATH, 'knowvi.db')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=1@^amtq%b_no*_0#vv-qx2)bx-t&1qt9#^vegmqc&k$3&cwgm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['zguang.pythonanywhere.com']



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'knowvi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'knowvi_project.urls'

WSGI_APPLICATION = 'knowvi_project.wsgi.application'

# Templates
TEMPLATE_DIRS = (
    # Put strings here and don't forget to use absolute paths
    TEMPLATE_PATH,
)

# Active link highlighting
TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

# Media files
MEDIA_URL = '/media/'

# Login
LOGIN_URL = '/knowvi/login/'
