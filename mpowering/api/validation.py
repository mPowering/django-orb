# oppia/quiz/api/validation.py
from django.utils.translation import ugettext_lazy as _

from mpowering.models import Resource

from tastypie import bundle
from tastypie.validation import Validation

class ResourceOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        resource = bundle.obj.resource
        if resource.create_user.id != bundle.request.user.id:
                errors['error_message'] = _(u"You are not the owner of this resource")
        return errors
    