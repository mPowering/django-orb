# coding: utf-8

"""
Model field definitions for Django ORB
"""

from autoslug import AutoSlugField as BaseSlugField


class AutoSlugField(BaseSlugField):
    """
    Redefined AutoSlugField with defaults selected

    - unique: True
    """
    def __init__(self, *args, **kwargs):
        if "unique" not in kwargs and "unique_with" not in kwargs:
            kwargs["unique"] = True
        super(AutoSlugField, self).__init__(*args, **kwargs)
