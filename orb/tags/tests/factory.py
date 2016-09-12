import uuid

from orb.categories.tests.factory import category_factory
from orb.models import Tag


def tag_factory(**kwargs):
    user = kwargs.pop("user", None)
    if user:
        kwargs.update({
            "create_user": user,
            "update_user": user,
        })

    defaults = {
        "category": category_factory(),
        "name": str(uuid.uuid4()),
    }
    defaults.update(kwargs)
    return Tag.objects.create(**defaults)
