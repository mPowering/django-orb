
from django.utils.translation import ugettext as _

ERROR_CODE_RESOURCE_EXISTS = 2000
ERROR_CODE_RESOURCE_NO_TITLE = 4000
ERROR_CODE_RESOURCE_NO_DESCRIPTION = 4001

ERROR_CODE_TAG_EXISTS = 5000
ERROR_CODE_TAG_EMPTY = 5001

ERROR_CODES = {
               ERROR_CODE_RESOURCE_EXISTS : _(u"You have already uploaded a resource with this title"),
               ERROR_CODE_RESOURCE_NO_TITLE : _(u"No title provided"),
               ERROR_CODE_RESOURCE_NO_DESCRIPTION : _(u"No description provided"),
               ERROR_CODE_TAG_EXISTS : _(u'This tag already exists'),
               ERROR_CODE_TAG_EMPTY : _(u'Cannot add empty tag'),
               }