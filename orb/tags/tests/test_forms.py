# -*- coding: utf-8 -*-

"""
Tests for ORB tag forms
"""

from hypothesis import strategies as st, given, example

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


@given(st.integers())
def test_tag_page_validation(page):
    form = TagPageForm(data={'order': TagPageForm.CREATED, 'page': page})

    if page > 0:
        assert form.is_valid()
    else:
        assert not form.is_valid()
