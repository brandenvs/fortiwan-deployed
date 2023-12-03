from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-swr011w^(j!6%7-(9wouxt6r&5fpw(*63!2l193i1628#l@v85'

DEBUG = True

ALLOWED_HOSTS = [
    'https://fortiapi.bcfa.co.za',
    'fortiapi.bcfa.co.za',
    '51.68.220.41', 
    'localhost', 
    '127.0.0.1'
]

INSTALLED_APPS = [
    'corsheaders',
    'fortiwan_services',
    'authentication',
    'fortiwan_dashboard',
    'fortiwan_monitor',
    'fortiwan_config',
    'fortiwan_log',
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
        'DIRS': [os.path.join(BASE_DIR, 'shared/layouts')],
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
        'NAME': 'frankfurt_de',
        'USER': 'brands',
        'PASSWORD': '?yeaB3@BU$72u0&S',
        'HOST': '54.37.74.171',
        'PORT': '5432',
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

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(STATIC_ROOT, 'css/'),
    os.path.join(STATIC_ROOT, 'js/'),
    os.path.join(STATIC_ROOT, 'res/')
]
# Use Whitenoise for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Load environment variables from the .env file
CONFIG_PATH = os.path.join(BASE_DIR, '.env')
config._find_file(CONFIG_PATH)

# Load environment variables
ACCESS_TOKEN = config('ACCESS_TOKEN')
API_KEY = config('API_KEY')
PASSWORD = config('PASSWORD')
CLIENT_ID = config('CLIENT_ID')
INTERFACE_TOKEN = config('INTERFACE_TOKEN')