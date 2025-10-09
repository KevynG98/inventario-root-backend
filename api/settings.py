from pathlib import Path
import os
import platform
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

# --- Base paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Load environment (safe in both DEV/PROD) ---
load_dotenv(BASE_DIR / '.env')

# --- Helper: CSV env -> list (skip empties/whitespace) ---
def env_csv(name: str, default: str = ""):
    raw = os.getenv(name, default)
    return [x.strip() for x in raw.split(",") if x.strip()]

# --- Toggle environment ---
DEV = True  # <<< set True for development, False for production

if DEV:
    print("🌍 DEV MODE: Using SQL Server (hospitalpruebas)\n")
else:
    print("☢️ PROD MODE: Using SQL Server (hospitalproduccion)\n")

# --- ODBC driver & params (unified for DEV/PROD) ---
ODBC_DRIVER = os.getenv("SQL_ODBC_DRIVER", "ODBC Driver 18 for SQL Server")
ODBC_EXTRA = os.getenv("DB_ODBC_EXTRA", "Encrypt=yes;TrustServerCertificate=yes;")

# --- Secrets / Security ---
if DEV:
    SECRET_KEY = 'django-insecure-dev-key'
    DEBUG = True

    ALLOWED_HOSTS = [
        '192.168.1.18',
        '10.10.20.16',
        'localhost',
        '127.0.0.1',
        '172.25.146.246',
    ]

    # CORS / CSRF (DEV)
    CORS_ALLOW_CREDENTIALS = True
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://192.168.1.18:3000",
        "http://10.10.20.16:3000",
        "http://10.10.20.16:3077",
        "http://172.25.146.246:3000",
        "http://172.25.146.246:3077",
    ]
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.18:3000",
        "http://10.10.20.16:3000",
        "http://10.10.20.16:3077",
        "http://172.25.146.246:3000",
        "http://172.25.146.246:3077",
    ]
    CORS_ALLOW_HEADERS = list(default_headers) + ['x-user']

    # --- Base de datos (DEV con detección de entorno) ---
    DB_HOST = os.getenv('DB_PRUEBAS_HOST', '172.25.146.246')
    if platform.system() == 'Windows':
        DB_HOST = '127.0.0.1'  # si lo corres directamente en Windows

    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.getenv('DB_PRUEBAS_NAME', 'hospitalpruebas'),
            'USER': os.getenv('DB_PRUEBAS_USER', 'hospital_user'),
            'PASSWORD': os.getenv('DB_PRUEBAS_PASSWORD', 'ContraseñaSegura123!'),
            'HOST': DB_HOST,
            'PORT': os.getenv('DB_PRUEBAS_PORT', '1433'),
            'OPTIONS': {
                'driver': ODBC_DRIVER,
                'extra_params': ODBC_EXTRA,
            },
        }
    }

else:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False

    # --- CORS / CSRF / Hosts (PROD via .env) ---
    ALLOWED_HOSTS = env_csv('ALLOWED_HOSTS')
    CSRF_TRUSTED_ORIGINS = env_csv('CSRF_TRUSTED_ORIGINS')
    CORS_ALLOWED_ORIGINS = env_csv('CORS_ALLOWED_ORIGINS')
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_HEADERS = list(default_headers) + ['x-user']

    # --- Base de datos (PROD) ---
    DB_HOST = os.getenv('DB_PROD_HOST', '172.25.146.246')
    if platform.system() == 'Windows':
        DB_HOST = '127.0.0.1'

    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.getenv('DB_PROD_NAME'),
            'USER': os.getenv('DB_PROD_USER'),
            'PASSWORD': os.getenv('DB_PROD_PASSWORD'),
            'HOST': DB_HOST,
            'PORT': os.getenv('DB_PROD_PORT', '1433'),
            'OPTIONS': {
                'driver': ODBC_DRIVER,
                'extra_params': ODBC_EXTRA,
            },
        }
    }

# --- Installed apps ---
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'api.apps.ApiConfig',
]

# --- DRF config ---
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.utils.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# --- Middleware ---
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

# --- URLs / WSGI ---
ROOT_URLCONF = 'api.urls'
WSGI_APPLICATION = 'api.wsgi.application'

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

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- i18n / tz ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'api' / 'static']

# --- Default PK ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
