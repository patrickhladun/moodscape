import pytest

from apps.review.forms import ReviewForm, ReviewStatusForm
from apps.review.models import Review


def test_review_form_initialization():
    form = ReviewForm()
    assert "rating" in form.fields
    assert "text" in form.fields


def test_review_form_valid_data():
    form_data = {
        "rating": 5,
        "text": "Great product!",
    }
    form = ReviewForm(data=form_data)
    assert form.is_valid()


def test_review_form_invalid_data():
    form_data = {
        "rating": 6,
        "text": "",
    }
    form = ReviewForm(data=form_data)
    assert not form.is_valid()


def test_review_form_rendering():
    form = ReviewForm()
    form_html = form.as_p()
    assert '<textarea name="text"' in form_html


def test_review_status_form_initialization():
    form = ReviewStatusForm()
    assert "status" in form.fields


def test_review_status_form_valid_data():
    form_data = {
        "status": "approved",
    }
    form = ReviewStatusForm(data=form_data)
    assert form.is_valid()


def test_review_status_form_invalid_data():
    form_data = {
        "status": "invalid_status",
    }
    form = ReviewStatusForm(data=form_data)
    assert not form.is_valid()
    assert "status" in form.errors
