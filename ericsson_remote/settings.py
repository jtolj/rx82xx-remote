# Django settings for ericsson_remote project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ericsson_remote.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'C:/Documents and Settings/jtolj/Dropbox/Work/django/ericsson_remote/static'


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    'C:/Users/Jesse/Dropbox/Work/django/ericsson_remote/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's(iim4wydfbc&amp;#))+k@mln98j6qi%87c!+b6*+9$&amp;ut*l*kr7^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ericsson_remote.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ericsson_remote.wsgi.application'

TEMPLATE_DIRS = (
   'C:/Users/Jesse/Dropbox/Work/django/ericsson_remote/templates',
   'C:/Documents and Settings/jtolj/Dropbox/Work/django/ericsson_remote/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'schedule_events',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

###### Receiver Configuration ######

#Configure receiver name as key, ip address as value.
RECEIVERS = {}
RECEIVERS['PBS1'] = '192.168.80.221'
RECEIVERS['PBS2'] = '192.168.80.222'
RECEIVERS['PBS3'] = '192.168.80.223'
RECEIVERS['PBS4'] = '192.168.80.224'
RECEIVERS['PBS6'] = '192.168.80.226'
RECEIVERS['PBS7'] = '192.168.80.227'
RECEIVERS['PBS8'] = '192.168.80.228'

#Horizonal is on Input 1, Vertical on Input 2
POLARITY_HORIZONTAL = 0
POLARITY_VERTICAL = 1

#Define schedules that can be tuned here. Key channel name, value is a tuple consisting of
#Polarity, Frequency, Symbol Rate, MPEG Service Number
SCHEDULES = {}
SCHEDULES['HD01'] = (POLARITY_VERTICAL, 1430000, 30000000, 3)
SCHEDULES['HD02'] = (POLARITY_VERTICAL, 1430000, 30000000, 4)
SCHEDULES['HD03'] = (POLARITY_VERTICAL, 1430000, 30000000, 5)
SCHEDULES['HD04'] = (POLARITY_HORIZONTAL, 1395500, 6250000, 3)
SCHEDULES['HD05'] = (POLARITY_HORIZONTAL, 1405000, 6250000, 3)
SCHEDULES['SD01'] = (POLARITY_VERTICAL, 1430000, 30000000, 11)
SCHEDULES['SD05'] = (POLARITY_HORIZONTAL, 1413000, 4440000, 11)
SCHEDULES['SD06'] = (POLARITY_HORIZONTAL, 1419000, 4440000, 11)
SCHEDULES['SD07'] = (POLARITY_HORIZONTAL, 1425000, 4440000, 11)
