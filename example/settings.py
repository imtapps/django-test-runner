import sys
from os.path import abspath, dirname, join
ROOT_DIR = abspath(dirname(__file__))
grandparent = abspath(join(ROOT_DIR, '..'))
for p in (grandparent, ROOT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'sample',
)

TEST_RUNNER = "djtest_runner.DjangoPyCharmRunner"