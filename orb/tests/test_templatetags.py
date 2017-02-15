# -*- coding: utf-8 -*-

import pytest

from orb.templatetags.translation_tags import translated_fields


@pytest.mark.django_db
def test_translated_fields_tag(test_resource, settings):
    settings.LANGUAGES = [
        ('en', u'English'),
        ('es', u'Español'),
        ('pt-br', u'Português'),
    ]
    test_resource.title_en = "Hey"
    test_resource.title_pt_br = "Ei"
    test_resource.description_en = "Hey"
    test_resource.description_pt_br = "Ei"
    test_resource.title_es = "hola"

    assert set(translated_fields(test_resource, "title")) == {"Hey", "Ei", "hola"}
    assert set(translated_fields(test_resource, "description")) == {"Hey", "Ei"}
