import os
from django.core.management.utils import get_random_secret_key

# === SECURITY SETTINGS ===

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
AUTH_USER_MODEL = 'users.User'

# === DATABASE SETTINGS ===

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'ramesh_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_HOST_USER = ' '

# === DJANGO APPS ===

INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'app.core',
    'app.users',
    'app.users.super_user',
    'app.users.doctor',
    'app.users.patient',
    # 'app.medical_services.counseling',
#     'app.medical_services.group_therapy',
#     'app.medical_services.knowledge_cafe',
#     'app.medical_services.nutritionist',
#     'app.medical_services.social_worker',
#     'app.medical_services.spiritual_therapy_specialist',
#     'app.medical_services.sports_physiology_specialist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'app.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "app", "core", "templates")],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.core.wsgi.application'

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

# === INTERNATIONALIZATION ===

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === STATIC FILES SETTINGS ===

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "app", "core", "static")]

# Default model auto field.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allow all origins to access your site (not recommended for production!)
CORS_ORIGIN_ALLOW_ALL = True
