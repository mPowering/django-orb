"""
App-specific settings go here.

This ensures that defaults can be provided for settings that may
not be explicitly available.
"""
from __future__ import unicode_literals

from django.conf import settings

DOWNLOAD_LOGIN_REQUIRED = getattr(settings, 'DOWNLOAD_LOGIN_REQUIRED ', True)
DOWNLOAD_EXTRA_INFO = getattr(settings, 'DOWNLOAD_EXTRA_INFO ', True)

EMBEDDABLE_FILE_TYPES = getattr(
    settings,
    'EMBEDDABLE_FILE_TYPES ',
    ['pdf', 'mp4', 'pptx', 'jpg', 'png', 'ppt', 'docx', 'mov', 'm4v'],
)
