""" Test settings
"""

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Extra apps
    "defender",
    "django_celery_beat",
    "drf_spectacular",
    "menu",
    # Local apps
    "xml_utils",
    "core_main_app",
    "core_explore_common_app",
    "core_explore_oaipmh_app",
    "core_federated_search_app",
    "core_oaipmh_common_app",
    "core_oaipmh_harvester_app",
    "core_linked_records_app",
    "tests",
]

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core_main_app.utils.custom_context_processors.domain_context_processor",  # Needed by any curator app
                "django.template.context_processors.i18n",
            ],
        },
    },
]

CUSTOM_NAME = "mock_custom_name"

ROOT_URLCONF = "tests.test_urls"

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
SERVER_URI = "http://mock-cdcs.com"

PID_PATH = "mock.pid"

ID_PROVIDER_PREFIXES = ["mock_cdcs"]

MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False

ENABLE_SAML2_SSO_AUTH = False

CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
