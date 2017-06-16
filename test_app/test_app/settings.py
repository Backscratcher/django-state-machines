DEBUG = True

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_state_machines',
    'fields_tests',
    'test_app',
)

DATABASE_ENGINE = 'sqlite3'

SECRET_KEY = '-'

MIDDLEWARE_CLASSES = ()

DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_database',
    }
}
