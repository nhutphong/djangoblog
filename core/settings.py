

import os

from django.contrib.messages import constants as messages

# At the top of the settings
import cloudinary
import cloudinary_storage


# global variable messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

import dj_database_url
import os
from django.test.runner import DiscoverRunner
from pathlib import Path


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


IS_HEROKU = "DYNO" in os.environ

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]


# Generally avoid wildcards(*). However since Heroku router provides hostname validation it is ok
if IS_HEROKU:
    ALLOWED_HOSTS = ["*"]

    # Cloudinary stuff
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': 'dkoiew4qz',
        'API_KEY': '518792273977517',
        'API_SECRET': '5fLFA1OueUqBfgUkkbfTJJqH1yo',
    }

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


else:
    ALLOWED_HOSTS = []



# SECURITY WARNING: don't run with debug turned on in production!
if not IS_HEROKU:
    DEBUG = True
else:
    DEBUG = False


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # library ben thu 3
    'bootstrap5',
    'django_bootstrap5',

    'crispy_forms',
    "crispy_bootstrap5", # new

    'bootstrap_pagination',
    # 'django_pagination_bootstrap',

    # Media Cloudinary
    'cloudinary',
    'cloudinary_storage',

    #whitenoise static file
    "whitenoise.runserver_nostatic",

    # app tu tao
    'pages',
    'products',
    'blog',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # heroku
    'django.middleware.security.SecurityMiddleware',
    # whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # folder /app-name/templates/app-name/*.html
        'DIRS': [ BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

MAX_CONN_AGE = 600
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trydjango',
        'USER': 'phong',
        'PASSWORD': '12341234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
} 


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#url on browser /static/app-name/static/{js,css,img}/{.js,.css,.jpg}
# folders, files duoc admin dua vao folder /static/
#access use syntax {% url 'img/files.jpg' %}
STATIC_URL = 'static/'

# add subfolder, for django scan, copy all folders, files to STATIC_ROOT='staticfiles'
#phai manual create folder top-lever static/
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

#django scan copy all folders,files, in app-name/static/...  to STATIC_ROOT
# STATIC_ROOT auto create folder 'staticfiles'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE ="django.contrib.staticfiles.storage.StaticFilesStorage" # new
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

#lưu media upload, con config urlpatterns in core.urls.py
# files duoc use or admin via form upload
#access use syntax {{ obj.field_name.url }}
MEDIA_URL = "/media/"  # url trên browser
# local name trong project, tên 'media' có thể đổi tùy ý
MEDIA_ROOT = BASE_DIR / 'media'

# required
LOGIN_URL = '/accounts/login/'
#LoginView, LogoutView
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5" # new
CRISPY_TEMPLATE_PACK = "uni_form"


# Test Runner Config
class HerokuDiscoverRunner(DiscoverRunner):
    """Test Runner for Heroku CI, which provides a database for you.
    This requires you to set the TEST database (done for you by settings().)"""

    def setup_databases(self, **kwargs):
        self.keepdb = True
        return super(HerokuDiscoverRunner, self).setup_databases(**kwargs)


# Use HerokuDiscoverRunner on Heroku CI
if "CI" in os.environ:
    TEST_RUNNER = "gettingstarted.settings.HerokuDiscoverRunner"


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#future deployment settings
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
# DATABASES['default']['CONN_MAX_AGE'] = 500