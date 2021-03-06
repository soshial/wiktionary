import os
from os.path import join


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

STORAGE_PATH = join(ROOT_PATH, 'storage')
LOGS_PATH = join(ROOT_PATH, 'logs')

DEBUGGING = False

try:
    from .local_conf import *
except ImportError:
    pass

MAIN_STORAGE_PATH = join(STORAGE_PATH, 'main')
AUTHORS_STORAGE_PATH = join(STORAGE_PATH, 'authors')
HTMLS_STORAGE_PATH = join(STORAGE_PATH, 'htmls')
REPORTS_PATH = join(STORAGE_PATH, 'reports')
SYNC_PATH = join(STORAGE_PATH, 'sync')

try:
    from .local_paths import *  # we can change storage sub-paths here
except ImportError:
    pass
