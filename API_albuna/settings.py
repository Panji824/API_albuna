from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# --- HOSTS & CORS (FIXED FOR NGROK/REACT) ---
if DEBUG:
    # IZINKAN HOST APAPUN saat development. Ini mengatasi masalah Ngrok Host Header.
    ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
else:
    # HANYA HOST YANG DIİZINKAN DI PRODUCTION
    ALLOWED_HOSTS = ['.render.com', 'unsolitary-joni-spleenish.ngrok-free.dev']

# Izinkan React dan Ngrok sebagai Origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://albuna-hijab.vercel.app",
    "https://unsolitary-joni-spleenish.ngrok-free.dev",
]
# --- END CORS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # API & CORS
    'rest_framework',
    'corsheaders',
    'product_catalog.apps.ProductCatalogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Untuk Static Files di Production
    'corsheaders.middleware.CorsMiddleware',  # CORS harus di atas Session/Auth
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'API_albuna.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'API_albuna.wsgi.application'

# --- DATABASE (DYNAMIC CONFIG) ---
# 1. Konfigurasi Lokal (Menggunakan .env untuk Supabase Pooler)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}

# 2. Logika Production (Render) - Menimpa konfigurasi di atas jika ditemukan
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_check=True,
        )
    }
# --- END DATABASE ---


# --- DRF PERMISSIONS FIX ---
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # Izinkan siapa saja melihat data (GET), tapi memerlukan autentikasi
        # untuk mengubah data (POST, PUT, DELETE). Ini mengatasi konflik sesi admin.
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ]
}
# --- END DRF FIX ---
AUTH_PASSWORD_VALIDATORS = [
    # ... (password validators)
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
CORS_ALLOW_ALL_ORIGINS = True # Opsional, dipertahankan untuk kompatibilitas yang lebih luas
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'