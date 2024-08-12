import pytest

from apps.frontend.forms import ContactForm

@pytest.mark.django_db
def test_contact_form_initial_state():
    form = ContactForm()
    assert not form.is_bound

@pytest.mark.django_db
def test_contact_form_with_valid_data():
    form_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "message": "This is a test message.",
    }
    form = ContactForm(data=form_data)
    assert form.is_bound
    assert form.is_valid()
    assert form.cleaned_data["name"] == "John Doe"
    assert form.cleaned_data["email"] == "johndoe@example.com"
    assert form.cleaned_data["message"] == "This is a test message."

@pytest.mark.django_db
def test_contact_form_with_empty_data():
    form_data = {}
    form = ContactForm(data=form_data)
    assert form.is_bound
    assert not form.is_valid()
    assert "name" in form.errors
    assert "email" in form.errors
    assert "message" in form.errors
    assert form.errors["name"] == ["This field is required."]
    assert form.errors["email"] == ["This field is required."]
    assert form.errors["message"] == ["This field is required."]

@pytest.mark.django_db
def test_contact_form_with_invalid_email():
    form_data = {
        "name": "John Doe",
        "email": "john.doe@example",
        "message": "This is a test message.",
    }
    form = ContactForm(data=form_data)
    assert form.is_bound
    assert not form.is_valid()
    assert "email" in form.errors
    assert form.errors["email"] == ["Enter a valid email address."]
