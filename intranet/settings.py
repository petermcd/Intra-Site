"""Settings for the Django project."""
import mimetypes
import os
import socket
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(
    os.getenv(
        "SECURITY_KEY",
        "django-insecure-w6d881036p!78s)**g^=9b%h0ujlgg(0ldpkt6jwz&r#s=6y!6",
    )
)

mimetypes.add_type("application/javascript", ".js", True)

DEBUG = True

allowed_host_env = os.getenv(
    "DJANGO_ALLOWED_HOST",
    "intra.petermcdonald.co.uk",
)

ALLOWED_HOSTS: list[str] = [
    allowed_host_env,
]

CSRF_TRUSTED_ORIGINS: list[str] = [
    f"https://{allowed_host_env}",
]

INTERNAL_IPS: list[str] = []

if int(os.getenv("DJANGO_DEBUG", 0)) == 1:
    DEBUG = True
    ALLOWED_HOSTS = [
        "*",
    ]
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
    ]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": str(os.getenv("DATABASE_HOST")),
            "PORT": str(os.getenv("DATABASE_PORT")),
            "NAME": str(os.getenv("DATABASE_NAME")),
            "USER": str(os.getenv("DATABASE_USERNAME")),
            "PASSWORD": str(os.getenv("DATABASE_PASSWORD")),
        },
    }

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mathfilters",
    "oauth2_provider",
    "rest_framework",
    "api.apps.ApiConfig",
    "books.apps.BooksConfig",
    "documents.apps.DocumentsConfig",
    "events.apps.EventsConfig",
    "finance.apps.FinanceConfig",
    "network.apps.NetworkConfig",
    "settings.apps.SettingsConfig",
    "tasks.apps.TasksConfig",
    "wishlist.apps.WishlistConfig",
    "debug_toolbar",
    "django_cleanup.apps.CleanupConfig",  # Must be placed last
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "intranet.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "intranet.wsgi.application"

OAUTH2_PROVIDER = {
    "ALLOWED_REDIRECT_URI_SCHEMES": ["https", "intra"],
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
        "groups": "Access to your groups",
    },
}

REST_FRAMEWORK: dict[str, Union[set[str], list[str]]] = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
