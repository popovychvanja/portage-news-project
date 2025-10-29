"""
Django settings for portage_news_project project.
"""

from pathlib import Path
import os
import dj_database_url
from whitenoise.storage import CompressedManifestStaticFilesStorage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# 1. SECURITY AND DEBUG
# =========================

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variables for the secret key in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-local-insecure-key')

# Set DEBUG to False in production
DEBUG = 'RENDER' not in os.environ

# Set ALLOWED_HOSTS for security
ALLOWED_HOSTS = ['portage-news-web.onrender.com', 'localhost', '127.0.0.1'] 
# You must replace 'portage-news-web.onrender.com' with your actual Render URL

# Ensure secure settings are on in production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# =========================
# 2. APPLICATION DEFINITION
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your Apps Here
    'news', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be listed directly after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portage_news_project.urls' # **UPDATE THIS**

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'portage_news_project.wsgi.application' # **UPDATE THIS**


# =========================
# 3. DATABASE CONFIGURATION
# =========================

# Database configuration logic to switch between local (SQLite) and production (PostgreSQL)

if 'RENDER' in os.environ:
    # Production: Use PostgreSQL via the DATABASE_URL environment variable
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600  # Persistent connections for performance
        )
    }
else:
    # Local Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# =========================
# 4. STATIC FILES (CSS, JS, Images)
# =========================

# URL prefix for static files
STATIC_URL = '/static/'

# Absolute path to the directory where collectstatic will gather files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use WhiteNoise storage for static files in production
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
# MEDIA FILES (for user uploads)
# You should configure an external storage like AWS S3 or a separate Render service for production
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================
# 5. GENERAL & AUTH
# =========================

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True