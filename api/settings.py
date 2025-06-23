from pathlib import Path
import os

# --- Rutas básicas ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Controlar ambiente ---
DEV = True  # <<< SOLO cambia esto a False en producción

if DEV:
    print("🌍 MODO DESARROLLO: Estás usando base de datos SQL Server (hospitalpruebas)\n")
else:
    print("☢️ MODO PRODUCCIÓN: Estás usando base de datos SQL Server (hospitalproduccion)\n")

# --- Secretos y configuraciones ---
if DEV:
    SECRET_KEY = 'django-insecure-er(in23ikbn2fkn)ik9@yjj#1io1u+@%^*xnp(2%^0)473)9vy'
    DEBUG = True

    ALLOWED_HOSTS = [
        '192.168.1.18',
        '10.10.20.16',
        'localhost',
        '127.0.0.1'
    ]

    CORS_ALLOW_CREDENTIALS = True

    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://192.168.1.18:3000",
        "http://10.10.20.16:3000"
    ]

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.18:3000",
        "http://10.10.20.16:3000"
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'hospitalpruebas',
            'USER': 'hospital_user',
            'PASSWORD': 'ContraseñaSegura123!',
            'HOST': '172.25.146.246',
            'PORT': '1433',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
                'trust_server_certificate': 'yes',
            },
        }
    }

else:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')

    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False

    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    CORS_ALLOW_CREDENTIALS = True

    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.getenv('DB_PROD_NAME'),
            'USER': os.getenv('DB_PROD_USER'),
            'PASSWORD': os.getenv('DB_PROD_PASSWORD'),
            'HOST': os.getenv('DB_PROD_HOST'),
            'PORT': os.getenv('DB_PROD_PORT', '1433'),
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
                'trust_server_certificate': 'yes',
            },
        }
    }

# --- Apps instaladas ---
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api.apps.ApiConfig',
]

# --- Configuración de DRF ---
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.utils.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# --- Middlewares ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middlewares.middlewares.AuditoriaMiddleware',
    'api.middlewares.MovimientoInventarioMiddleware.MovimientoInventarioMiddleware',
]

# --- Configuración de URLs ---
ROOT_URLCONF = 'api.urls'

# --- Templates ---
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

# --- WSGI ---
WSGI_APPLICATION = 'api.wsgi.application'

# --- Validadores de contraseñas ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalización ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'api' / 'static']

# --- Primary key default ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
