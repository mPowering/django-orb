# -*- coding: utf-8 -*-
#import ctypes
import os

import dj_database_url  # NOTE: This is not in the project requirements!


DATABASES = {'default': dj_database_url.config(default='mysql://root@localhost/orb')}
DATABASES['default']['TEST'] = {'NAME': os.environ.get('TEST_DB_NAME', 'test_orb')}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'

#GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH', '/usr/local/lib/libgdal.dylib')
#ctypes.CDLL(GDAL_LIBRARY_PATH)

