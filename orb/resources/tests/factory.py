from orb.models import Resource


def resource_factory(**kwargs):
    user = kwargs.pop("user", None)
    if user:
        kwargs.update({
            "create_user": user,
            "update_user": user,
        })

    defaults = {
        "title": "Test resource",
        "description": "Test resource",
    }
    defaults.update(kwargs)
    return Resource.objects.create(**defaults)