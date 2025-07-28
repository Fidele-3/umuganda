from pathlib import Path
from datetime import timedelta
import os
import dj_database_url
import ssl
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-secret") 
DEBUG = os.environ.get("DEBUG", "False") == "True"


#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

ALLOWED_HOSTS = ['http://10.0.2.2', '10.0.2.2', '127.0.0.1']

# DATABASE

import os

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'umuganda',
        'USER': 'umuganda_user',
        'PASSWORD': '11223344',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

"""

PUBLIC_API_URL = os.environ.get("PUBLIC_API_URL", "http://localhost:8000")

# APPLICATIONS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "umuganda",
    "users",
    "payment.apps.PaymentConfig",
    "admn",
    "sector",
    "corsheaders",
    "rest_framework",
    "django_celery_beat",
]

# MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",

]

ROOT_URLCONF = "Umuganda.urls"
WSGI_APPLICATION = "Umuganda.wsgi.application"


AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = [
    "users.auth_backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

# STATIC FILES
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# MEDIA (optional)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# SIMPLE JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=31),
}

# CELERY
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")

CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_BROKER_USE_SSL = {
    "ssl_cert_reqs": ssl.CERT_NONE  
}

CELERY_RESULT_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "Africa/Kigali"
CELERY_ENABLE_UTC = False

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)


# CORS
CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS", "False") == "True"
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://localhost:8081"
).split(",")

# FRONTEND URL
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# MISC
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1
TIME_ZONE = "Africa/Kigali"
USE_I18N = True
USE_TZ = False
LANGUAGE_CODE = "en-us"

import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },

    'root': {
        'handlers': ['console'],
       'level': 'DEBUG',  # Show everything
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
           'level': 'INFO',  # Change to INFO or WARNING in production
            'propagate': True,
        },
        'django.db.backends': {
           'handlers': ['console'],
            'level': 'DEBUG',  
        },
    },
}
