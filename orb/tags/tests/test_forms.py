# -*- coding: utf-8 -*-

"""
Tests for ORB tag forms
"""

from hypothesis import strategies as st, given, example, settings
import  pytest

from orb.tags.forms import TagPageForm


@given(st.characters())
@example(u'-create_date')
@example(u'title')
@example(u'-update_date')
@example(u'-rating')
def test_tag_order_validation(order_by):
    form = TagPageForm(data={'order': order_by, 'page': 1})

    if order_by in {option[0] for option in TagPageForm.ORDER_OPTIONS}:
        assert form.is_valid()
        assert form.cleaned_data['order'] == order_by

    else:
        assert not form.is_valid()


@given(st.characters())
def test_tag_page_number_validation(page):
    form = TagPageForm(data={'page': page})
    try:
        page_num = int(page)
    except (TypeError, ValueError):
        assert not form.is_valid()
    else:
        if page_num > 0:
            assert form.is_valid()
        else:
            assert not form.is_valid()


@pytest.mark.parametrize("page,expected", [
    ("1",1),
    ("3",3),
])
def test_valid_page_numbers(page, expected):
    form = TagPageForm(data={'page': page})
    form.is_valid()
    assert form.cleaned_data['page'] == expected


@given(st.integers())
def test_tag_page_validation(page):
    form = TagPageForm(data={'order': TagPageForm.CREATED, 'page': page})

    if page > 0:
        assert form.is_valid()
    else:
        assert not form.is_valid()
