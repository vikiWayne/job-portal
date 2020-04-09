from job_portal.settings.common import *

try:
    from job_portal.settings.local import *
except ImportError:
    pass
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y*&an+$_@(y+_6q-645=sv=9(1zoru&8mot9mx8zh=630a5)m9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
