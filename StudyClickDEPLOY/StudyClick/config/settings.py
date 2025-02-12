
from pathlib import Path

from datetime import timedelta
import os
from re import A
# from telnetlib import AUTHENTICATION
import environ
from pathlib import Path

env = environ.Env()
# Set the project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join('.env'))


# BASE_DIR = Path('.env/')

# просто для правильной работы
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://localhost',
    'http://localhost:3000',
    'http://45.89.189.58',
    'http://127.0.0.1:8000',
    'http://django:8000',  # Если используется контейнеризация, например, Docker
    # HTTPS версии, если они будут задействованы
    'https://45.89.189.58',
]
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = [
    '127.0.0.1',      
    'localhost',      
    'localhost:3000', 
    '45.89.189.58',   
    'django',         # Имя контейнера в Docker
]

BASE_DIR = Path(__file__).resolve().parent.parent.parent



# BASE
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# PACKAGES
INSTALLED_APPS += [
    'corsheaders',
    'rest_framework',
    # 'djoser',
    # 'phonenumber_field',
    'drf_spectacular',
]

# APPS
INSTALLED_APPS += [
    'api',
    'common',
    'chatbot',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
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
#################################
# REST
#################################
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
   'rest_framework.permissions.AllowAny',
],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.BasePagination',
}
###################################
# CORS
###################################
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ['http://localhost:3000']
CORS_COOKIE_SECURE = False

###################################
# static & media
###################################
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_TEST_ROOT = os.path.join(BASE_DIR, 'media/test/')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
###################################
# spectakular
###################################
SPECTACULAR_SETTINGS = {
    'TITLE': 'StudyClick',
    'DESCRIPTION': 'API обучающей платформы с AI',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.AllowAny',
    ],

    # 'SERVE_AUTHENTICATION': [
    #     'rest_framework.authentication.BasicAuthentication'
    # ],

    'SWAGGER_UI_SETTINGS': {
        'DeepLinking': True,
        'Display0perationId': True,
        'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}
