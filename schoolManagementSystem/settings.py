from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-tho$pm1pz8&o*a3st$%dgfct%f%m@g1)kfa7)8*y)&9yjy()ze"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', '172.16.6.91', 'ibaschat.celloscope.net']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "home.apps.HomeConfig",
    "authenticationApp.apps.AuthenticationappConfig",
    "staffApp.apps.StaffappConfig",
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "schoolManagementSystem.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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

CORS_ALLOWED_ORIGINS = [
    'http://172.16.6.91',
    'http://172.16.6.91:8001',
    'http://ibaschat.celloscope.net',
    #"https://ibaschat.celloscope.net",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:5502",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501"
]



#CSRF_TRUSTED_ORIGINS = [
#    'http://172.16.6.91',
#    'http://ibaschat.celloscope.net',
#],

WSGI_APPLICATION = "schoolManagementSystem.wsgi.application"  # [use WSGI to run vannila-dj-app]
ASGI_APPLICATION = "schoolManagementSystem.asgi.application"

# Assign the Custom User Model Configuration
AUTH_USER_MODEL = "authenticationApp.User"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Integrate MongoDB
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'drmc_db',
#         'CLIENT': {
#             'host': 'mongodb://mongo:mongo@localhost:27017/?authSource=admin',
#             'port': 27017,
#             'username': 'mongo',
#             'password': 'mongo',
#             'authSource': 'admin',
#             'authMechanism': 'SCRAM-SHA-1'
#         },
#     }
# }

# Integrate PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ibas_db',
        'USER': 'ibas_admin',
        'PASSWORD': 'L10w$ShRU021',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Channel-Redis Server Setup
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                ("127.0.0.1", 6379),
            ],
        },
    },
}


CHANNELS = {
    'DEFAULT_CHANNEL_LAYER': 'default',
    'ALLOWED_HOSTS': ['172.16.6.91', 'ibaschat.celloscope.net'],
    'MIDDLEWARE': [
        'channels.middleware.CorsMiddleware',
    ],
    'CORS_ORIGIN_ALLOW_ALL': True,
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static'),
#]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media Configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email service configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'python4dia@gmail.com'
EMAIL_HOST_PASSWORD = 'wyyyryzlymjicrhw'
EMAIL_PORT = 587


#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
