from orb.models import Tag
from orb.categories.tests.factory import category_factory


def tag_factory(**kwargs):
    user = kwargs.pop("user", None)
    if user:
        kwargs.update({
            "create_user": user,
            "update_user": user,
        })

    defaults = {
        "category": category_fixture(),
        "name": "Test tag",
    }
    defaults.update(kwargs)
    return Tag.objects.create(**defaults)