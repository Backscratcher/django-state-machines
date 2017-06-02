INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_state_machines',
    'test_app',
)

DATABASE_ENGINE = 'sqlite3'

SECRET_KEY = '-'

MIDDLEWARE_CLASSES = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
