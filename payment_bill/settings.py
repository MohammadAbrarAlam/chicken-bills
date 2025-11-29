"""
Django settings for payment_bill project.
Production-ready version.
"""

import os
from pathlib import Path

# ----------------------------
# Base directory
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# Security
# ----------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'replace_this_with_env_secret')

# Turn off debug in production
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Set your domain or IP here
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

# ----------------------------
# Application definition
# ----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payments',  # your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'payment_bill.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # add template dirs if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'payment_bill.wsgi.application'

# ----------------------------
# Database (SQLite for free deploy, e.g., on PythonAnywhere)
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------
# Password validation
# ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------
# Internationalization
# ----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------
# Static and Media files
# ----------------------------
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Optional: extra dirs during development
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# ----------------------------
# Default primary key field type
# ----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
