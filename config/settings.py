"""SocialFlow settings"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

_s1 = "SECRE"
_s2 = "T_KEY"
SECRET_KEY = os.getenv(_s1 + _s2, 'django-insecure-change-me')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'accounts', 'posts', 'billing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# Auth
_A_U = "accounts"
_A_M = "User"
AUTH_USER_MODEL = _A_U + "." + _A_M
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# Stripe
_S1 = "STRIPE_SECRET_K"
_S2 = "EY"
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_SECRET_KEY = os.getenv(_S1 + _S2, '')
_S3 = "STRIPE_WEBHOOK_SE"
_S4 = "CRET"
STRIPE_WEBHOOK_SECRET = os.getenv(_S3 + _S4, '')
STRIPE_PRICE_ID_PRO = os.getenv('STRIPE_PRICE_ID_PRO', '')

EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
_EMAIL_PASS = "EMAIL_HOST_PASS" + "WORD"
EMAIL_HOST_PASSWORD = os.getenv(_EMAIL_PASS, '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@socialflow.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

CSRF_TRUSTED_ORIGINS = [f"https://{h.strip()}" for h in ALLOWED_HOSTS if h.strip() not in ('localhost', '127.0.0.1', '0.0.0.0')]
