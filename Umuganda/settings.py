from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-secret")  # Must be set in Render
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'umuganda',
        'USER': 'umuganda_user',
        'PASSWORD': 'liTxrFhyok4vD7UVIqooA2Vja3wBS57Y',
        'HOST': 'dpg-d21rrrumcj7s73et6vk0-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}


# PUBLIC API URL (used in verification/reset/email links)
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
]

ROOT_URLCONF = "Umuganda.urls"
WSGI_APPLICATION = "Umuganda.wsgi.application"

# CUSTOM USER MODEL & AUTH BACKEND
AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = [
    "users.auth_backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# TEMPLATES
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
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_TIMEZONE = "Africa/Kigali"
CELERY_ENABLE_UTC = False

# EMAIL (console for dev, set SMTP in production)
DEFAULT_FROM_EMAIL = "no-reply@umuganda.com"
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)

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
USE_TZ = True
LANGUAGE_CODE = "en-us"

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}
