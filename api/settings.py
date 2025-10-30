from pathlib import Path
import os
import socket
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Load environment ---
load_dotenv(BASE_DIR / ".env")

# ======================================================
# 🌍 ENTORNO Y RED DETECTADOS AUTOMÁTICAMENTE
# ======================================================
DEV = os.getenv("DEV", "True").lower() == "true"  # True = base de pruebas

hostname_ip = socket.gethostbyname(socket.gethostname())
if hostname_ip.startswith("10."):
    NETWORK = "lan"
elif hostname_ip.startswith("172."):
    NETWORK = "zerotier"
else:
    NETWORK = "local"

print(f"🌐 Network: {NETWORK.upper()} | Host IP: {hostname_ip}")
print("💾 Base activa:", "hospitalpruebas" if DEV else "hospitalproduccion")

# ======================================================
# 🔐 SECRET / DEBUG
# ======================================================
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-key")
DEBUG = True  # puedes dejarlo activo para ver errores

# ======================================================
# ⚙️ CORS / CSRF / HOSTS
# ======================================================
if NETWORK == "lan":
    ALLOWED_HOSTS = ["10.10.20.16", "localhost"]
    CORS_ALLOWED_ORIGINS = [
        "http://10.10.20.16:3000",
        "http://10.10.20.16:3077",
    ]
elif NETWORK == "zerotier":
    ALLOWED_HOSTS = ["172.25.146.246", "localhost"]
    CORS_ALLOWED_ORIGINS = [
        "http://172.25.146.246:3000",
        "http://172.25.146.246:3077",
    ]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ["x-user"]

# ======================================================
# 🧾 BASE DE DATOS
# ======================================================
ODBC_DRIVER = os.getenv("SQL_ODBC_DRIVER", "ODBC Driver 17 for SQL Server")

if DEV:
    DB_NAME = os.getenv("DB_PRUEBAS_NAME")
    DB_USER = os.getenv("DB_PRUEBAS_USER")
    DB_PASS = os.getenv("DB_PRUEBAS_PASSWORD")
    DB_HOST = os.getenv("DB_PRUEBAS_HOST")
    DB_PORT = os.getenv("DB_PRUEBAS_PORT")
else:
    DB_NAME = os.getenv("DB_PROD_NAME")
    DB_USER = os.getenv("DB_PROD_USER")
    DB_PASS = os.getenv("DB_PROD_PASSWORD")
    DB_HOST = os.getenv("DB_PROD_HOST")
    DB_PORT = os.getenv("DB_PROD_PORT")

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "OPTIONS": {
            "driver": ODBC_DRIVER,
            "extra_params": "Encrypt=yes;TrustServerCertificate=yes;"
        },
    }
}

# ======================================================
# 🔧 REST / APPS / MIDDLEWARE
# ======================================================
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'api.apps.ApiConfig',
    'django_extensions',
    'operaciones.apps.OperacionesConfig',
    'solicitudes.apps.SolicitudesConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.utils.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

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

ROOT_URLCONF = 'api.urls'
WSGI_APPLICATION = 'api.wsgi.application'

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

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'api' / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
