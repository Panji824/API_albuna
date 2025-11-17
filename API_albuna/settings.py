from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# --- HOSTS & CORS (FIXED FOR NGROK/REACT) ---
if DEBUG:
    # IZINKAN HOST APAPUN saat development. Ini mengatasi masalah Ngrok Host Header.
    ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
else:
    # HANYA HOST YANG DIİZINKAN DI PRODUCTION
    ALLOWED_HOSTS = ['.render.com', 'unsolitary-joni-spleenish.ngrok-free.dev', ".up.railway.app"]

# Izinkan React dan Ngrok sebagai Origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.up.railway.app",
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
    'cloudinary_storage',
    'cloudinary',

    # API & CORS
    'rest_framework',
    'corsheaders',
    'product_catalog.apps.ProductCatalogConfig',
]
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

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
    # Opsi 1: Menggunakan variabel tunggal DATABASE_URL (Railway Production)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_check=True,
        )
    }
else:
    # Opsi 2: Fallback ke variabel individual (Local Development/Testing)
    # Kita harus memberikan nilai default untuk mencegah error UndefinedValueError
    # jika DB_NAME tidak disetel di .env lokal.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            # Tambahkan default, ini mengatasi UndefinedValueError jika DB_NAME kosong
            'NAME': config('DB_NAME', default='postgres_local_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432')
        }
    }


# --- DRF PERMISSIONS FIX ---
REST_FRAMEWORK = {
    # Keep your existing permission settings
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    # ADD THIS BLOCK: Use token/basic auth and remove session authentication
    # which is what triggers the default CSRF check for API endpoints.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # For testing/stateless API: use token auth
        # 'rest_framework.authentication.TokenAuthentication',

        # OR, keep session only if you need admin UI login, but make sure
        # to exclude it from views called by React.
        # A common strategy is to only use Basic or Token for the API:
        'rest_framework.authentication.BasicAuthentication',
    ],
    # Ensure all views that are NOT meant for the Admin UI do not require CSRF.
    # This is usually done by using the @api_view decorator which defaults to
    # using the settings above.
}
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.dev', # Wildcard for all ngrok tunnels
    'https://unsolitary-joni-spleenish.ngrok-free.dev',
    'https://albuna-hijab.vercel.app',
    # Add your render.com domain if it also posts to the API
]
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