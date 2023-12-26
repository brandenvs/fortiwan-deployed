from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'django-insecure-swr011w^(j!6%7-(9wouxt6r&5fpw(*63!2l193i1628#l@v85'

DEBUG = False

CONFIG_PATH = os.path.join(BASE_DIR.parent, '.env')
config._find_file(CONFIG_PATH)

API_KEY = config('API_KEY')
PASSWORD = config('PASSWORD')
CLIENT_ID = config('CLIENT_ID')

ALLOWED_HOST = config('ALLOWED_HOST')

PSQL_NAME = config('PSQL_NAME')
PSQL_USERNAME = config('PSQL_USERNAME')
PSQL_PASSWORD = config('PSQL_PASSWORD')
PSQL_HOST = config('PSQL_HOST')
PSQL_PORT = config('PSQL_PORT')

allowed_base = ALLOWED_HOST
allowed_https = f'https://{ALLOWED_HOST}'

ALLOWED_HOSTS = [
    allowed_https,
    allowed_base,
    '51.68.220.41', 
    'localhost', 
    '127.0.0.1'
]

INSTALLED_APPS = [
    'corsheaders',
    'authentication',
    'services',   
    'ipsec_dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Cookies
SESSION_COOKIE_SECURE = True

'''APPLICATION SECURITY SETTINGS'''
# CORS Policy
CORS_ALLOW_ALL_ORIGINS = True

# CSRF Tokenization
CSRF_TRUSTED_ORIGINS = ['https://fortiapi.bcfa.co.za/']
CSRF_COOKIE_SECURE = True

# SSL Redirect
SECURE_SSL_REDIRECT = False

ROOT_URLCONF = 'myfortiwan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR.parent, 'shared/layouts')],
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

WSGI_APPLICATION = 'myfortiwan.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PSQL_NAME,
        'USER': PSQL_USERNAME,
        'PASSWORD': PSQL_PASSWORD,
        'HOST': PSQL_HOST,
        'PORT': PSQL_PORT,
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL =  'static/'

# STATIC_ROOT = '/home/fortiwan/fortiwanroot/site/Fortiwan-Deployed/static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent.relative_to(BASE_DIR.parent), 'static/') 

STATICFILES_DIRS = [
    os.path.join(STATIC_ROOT, 'css/'),
    os.path.join(STATIC_ROOT, 'js/'),
    os.path.join(STATIC_ROOT, 'res/') 
]