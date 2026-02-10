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
isProd = not DEV

hostname_ip = socket.gethostbyname(socket.gethostname()) 
if hostname_ip.startswith("10."):
    NETWORK = "lan"
elif hostname_ip.startswith("172."):
    NETWORK = "zerotier"
else:
    NETWORK = "local"

print(f"🌐 Network: {NETWORK.upper()} | Host IP: {hostname_ip}")
print("💾 Base activa:", "inventariopruebas" if DEV else "inventarioproduccion")

# ======================================================
# 🔐 SECRET / DEBUG
# ======================================================
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-key")
DEBUG = DEV  # True si estamos en desarrollo

# ======================================================
# ⚙️ CORS / CSRF / HOSTS
# ======================================================
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if isProd:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "inventario-root-backend.onrender.com",
        "gamatec.org",
        "www.gamatec.org",
    ]
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        "https://gamatec.org",
        "https://www.gamatec.org",
        "https://inventario-root-backend.onrender.com",
        "http://localhost",
        "http://127.0.0.1",
    ]
elif NETWORK == "lan":
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
    CORS_ALLOWED_ORIGINS = ["http://localhost:3000", 
                            "http://127.0.0.1:3000",
                            "http://localhost:5173",
                            "http://localhost:4173"]

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
    
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASS,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
else:
    DB_NAME = os.getenv("DB_PROD_NAME")
    DB_USER = os.getenv("DB_PROD_USER")
    DB_PASS = os.getenv("DB_PROD_PASSWORD")
    DB_HOST = os.getenv("DB_PROD_HOST")
    DB_PORT = os.getenv("DB_PROD_PORT")

    # Si falta el host de producción, asumimos que se quiere usar la configuración de MySQL de respaldo
    if not DB_HOST:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.getenv("DB_PRUEBAS_NAME"),
                "USER": os.getenv("DB_PRUEBAS_USER"),
                "PASSWORD": os.getenv("DB_PRUEBAS_PASSWORD"),
                "HOST": os.getenv("DB_PRUEBAS_HOST"),
                "PORT": os.getenv("DB_PRUEBAS_PORT"),
            }
        }
    else:
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
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'api.apps.ApiConfig',
    'django_extensions',
    'anymail',
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

# ======================================================
# ☁️ CLOUDINARY STORAGE
# ======================================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ======================================================
# 📧 Email (Resend via Anymail)
# ======================================================
# Usamos Anymail con el driver de Resend (API) en lugar de SMTP.
EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
ANYMAIL = {
    "RESEND_API_KEY": os.getenv("RESEND_API_KEY"),
}

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@resend.dev")
# El EMAIL_HOST_USER se mantiene si se usa en lógica de negocio como destinatario por defecto
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", DEFAULT_FROM_EMAIL)

# Configuración anterior (SMTP) deshabilitada/comentada por referencia:
# EMAIL_BACKEND = 'api.utils.custom_email_backend.ConfiguredEmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT') or 465)
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False') == 'True'
# EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'True') == 'True'
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")