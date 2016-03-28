from orb.models import Category


def category_factory(**kwargs):
    defaults = {
        "name": "Test category",
    }
    defaults.update(kwargs)
    return Category.objects.create(**defaults)
