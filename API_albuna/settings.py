from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# PENTING: Tambahkan default untuk mencegah kegagalan saat build/collectstatic
SECRET_KEY=config('SECRET_KEY', default='django-insecure-dummy-key-for-build-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# --- HOSTS & CORS (CLEANED FOR RAILWAY/VERCEL) ---
if DEBUG:
    # Development: Izinkan semua host lokal
    ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
else:
    # Production: Hapus Ngrok dan hanya izinkan domain production
    ALLOWED_HOSTS = [
        '.up.railway.app',
        '.albuna-hijab.vercel.app',
        'healthcheck.railway.app'
    ]
    # Wajib untuk Nginx/Proxy SSL di Railway
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Izinkan React dan Railway sebagai Origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://albuna-hijab.vercel.app",
    "https://*.up.railway.app", # Wildcard untuk Railway
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

# --- DATABASE (DYNAMIC CONFIG - BLOK TERKONSOLIDASI) ---
# Logika ini memastikan DATABASES hanya didefinisikan SATU KALI.
if os.environ.get('DATABASE_URL'):
    # Opsi 1: PRODUCTION (Gunakan variabel tunggal DATABASE_URL dari Railway)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_check=True,
        )
    }
else:
    # Opsi 2: DEVELOPMENT/LOCAL FALLBACK (Gunakan variabel individual DENGAN SAFE DEFAULTS)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            # Tambahkan default untuk mencegah UndefinedValueError
            'NAME': config('DB_NAME', default='postgres_local_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432')
        }
    }
# --- END DATABASE ---
# --- dddd ---

# --- DRF PERMISSIONS FIX ---
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
}
CSRF_TRUSTED_ORIGINS = [
    'https://albuna-hijab.vercel.app',
    'https://*.up.railway.app',
]
# --- END DRF FIX ---
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
CORS_ALLOW_ALL_ORIGINS = True # Opsional, dipertahankan untuk kompatibilitas yang lebih luas
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'