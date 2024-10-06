import pytest
from django import forms
from django_countries.fields import LazyTypedChoiceField

from __tests__.pytest.factories import (
    CategoryFactory,
    OrderFactory,
    OrderLineItemFactory,
    ProductFactory,
)
from apps.order.forms import (
    AddOrderItemForm,
    CreateOrderForm,
    OrderItemForm,
    OrderStatusForm,
    UpdateOrderForm,
    UpdateOrderStatusForm,
)


@pytest.mark.django_db
def test_create_order_form_has_correct_fields():
    """
    Test that the CreateOrderForm contains the expected fields and each field is of the correct type.
    Each assertion verifies that the field exists in the form and is of the correct Django field type.
    """
    form = CreateOrderForm()

    assert "email" in form.fields
    assert isinstance(form.fields["email"], forms.EmailField)
    assert "first_name" in form.fields
    assert isinstance(form.fields["first_name"], forms.CharField)
    assert "last_name" in form.fields
    assert isinstance(form.fields["last_name"], forms.CharField)
    assert "phone_number" in form.fields
    assert isinstance(form.fields["phone_number"], forms.CharField)
    assert "address_line_1" in form.fields
    assert isinstance(form.fields["address_line_1"], forms.CharField)
    assert "address_line_2" in form.fields
    assert isinstance(form.fields["address_line_2"], forms.CharField)
    assert "town_city" in form.fields
    assert isinstance(form.fields["town_city"], forms.CharField)
    assert "postcode" in form.fields
    assert isinstance(form.fields["postcode"], forms.CharField)
    assert "country" in form.fields
    assert isinstance(form.fields["country"], LazyTypedChoiceField)
    assert "county" in form.fields
    assert isinstance(form.fields["county"], forms.CharField)


@pytest.mark.django_db
def test_create_order_form_has_correct_placeholders():
    """
    Test that the placeholders for the CreateOrderForm fields are correctly set.

    This test checks that the form fields have the appropriate placeholder text, including
    the dynamic addition of an asterisk (*) for required fields.
    """
    form = CreateOrderForm()

    assert form.fields["email"].widget.attrs["placeholder"] == "Email *"
    assert (
        form.fields["first_name"].widget.attrs["placeholder"]
        == "First Name *"
    )
    assert (
        form.fields["last_name"].widget.attrs["placeholder"] == "Last Name *"
    )
    assert (
        form.fields["phone_number"].widget.attrs["placeholder"]
        == "Phone Number *"
    )
    assert (
        form.fields["address_line_1"].widget.attrs["placeholder"]
        == "Address Line 1 *"
    )
    assert (
        form.fields["address_line_2"].widget.attrs["placeholder"]
        == "Address Line 2"
    )
    assert (
        form.fields["town_city"].widget.attrs["placeholder"]
        == "Town or City *"
    )
    assert form.fields["postcode"].widget.attrs["placeholder"] == "Postcode"
    assert form.fields["country"].widget.attrs["placeholder"] == "Country *"
    assert form.fields["county"].widget.attrs["placeholder"] == "County"


@pytest.mark.django_db
def test_create_order_form_first_name_autofocus():
    """
    Test that the 'first_name' field in the CreateOrderForm has the autofocus attribute set to True.
    """
    form = CreateOrderForm()

    assert form.fields["first_name"].widget.attrs.get("autofocus") == True


@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        # Invalid Email
        pytest.param(
            "email",
            "johndoegmail.com",
            "Enter a valid email address.",
            id="missing_at_symbol",
        ),
        pytest.param(
            "email",
            "johndoe@gmailcom",
            "Enter a valid email address.",
            id="missing_dot_in_domain",
        ),
        pytest.param(
            "email",
            "johndoe@.com",
            "Enter a valid email address.",
            id="missing_local_part",
        ),
        pytest.param(
            "email",
            "@gmail.com",
            "Enter a valid email address.",
            id="missing_local_part_and_username",
        ),
        pytest.param(
            "email",
            "john.doe@com",
            "Enter a valid email address.",
            id="missing_subdomain",
        ),
        pytest.param(
            "email",
            "john..doe@gmail.com",
            "Enter a valid email address.",
            id="double_dot_in_local_part",
        ),
        pytest.param(
            "email",
            "john.doe@gmail..com",
            "Enter a valid email address.",
            id="double_dot_in_domain",
        ),
        pytest.param(
            "email",
            "john.doe@gmail.c",
            "Enter a valid email address.",
            id="domain_too_short",
        ),
        pytest.param(
            "email",
            "john.doe@.gmail.com",
            "Enter a valid email address.",
            id="dot_at_start_of_domain",
        ),
        pytest.param(
            "email",
            "john.doe.@gmail.com",
            "Enter a valid email address.",
            id="dot_at_end_of_local_part",
        ),
        pytest.param(
            "email",
            "john.doe@gmail .com",
            "Enter a valid email address.",
            id="space_in_domain",
        ),
        pytest.param(
            "email",
            "john.doe@ gmail.com",
            "Enter a valid email address.",
            id="space_before_domain",
        ),
        # Invalid first name
        pytest.param(
            "first_name",
            "",
            "This field is required.",
            id="first_name_required",
        ),
        pytest.param(
            "first_name",
            "Jayden Kasper Leroy Maximilian Ned",
            "Ensure this value has at most 30 characters (it has 34).",
            id="first_name_too_long",
        ),
        # Invalid last name
        pytest.param(
            "last_name",
            "",
            "This field is required.",
            id="last_name_required",
        ),
        pytest.param(
            "first_name",
            "Wolfeschlegelsteinhausenbergerdorff",
            "Ensure this value has at most 30 characters (it has 35).",
            id="first_name_too_long",
        ),
        # Invalid phone number
        pytest.param(
            "phone_number",
            "",
            "This field is required.",
            id="phone_number_required",
        ),
        # Invalid address line 1
        pytest.param(
            "address_line_1",
            "",
            "This field is required.",
            id="address_line_1_required",
        ),
        # Invalid town city
        pytest.param(
            "town_city",
            "",
            "This field is required.",
            id="town_city_required",
        ),
        # Invalid country
        pytest.param(
            "country", "", "This field is required.", id="country_required"
        ),
    ],
)
def test_create_order_form_invalid_fields(field, value, expected_error):
    """
    Test validation errors for various fields in the CreateOrderForm using invalid data.
    """
    form_data = {
        "email": "johndoe@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "address_line_1": "123 Main St",
        "address_line_2": "Apt 1",
        "town_city": "Springfield",
        "postcode": "12345",
        "country": "IE",
        "county": "Dublin",
    }

    form_data[field] = value

    form = CreateOrderForm(data=form_data)

    assert not form.is_valid()
    assert expected_error in form.errors.get(field, [])


@pytest.mark.django_db
def test_update_order_form_has_correct_fields():
    """
    Test that the UpdateOrderForm contains the expected fields and that each field is of the correct type.
    """
    form = UpdateOrderForm()

    assert "email" in form.fields
    assert isinstance(form.fields["email"], forms.EmailField)
    assert "first_name" in form.fields
    assert isinstance(form.fields["first_name"], forms.CharField)
    assert "last_name" in form.fields
    assert isinstance(form.fields["last_name"], forms.CharField)
    assert "phone_number" in form.fields
    assert isinstance(form.fields["phone_number"], forms.CharField)
    assert "address_line_1" in form.fields
    assert isinstance(form.fields["address_line_1"], forms.CharField)
    assert "address_line_2" in form.fields
    assert isinstance(form.fields["address_line_2"], forms.CharField)
    assert "town_city" in form.fields
    assert isinstance(form.fields["town_city"], forms.CharField)
    assert "postcode" in form.fields
    assert isinstance(form.fields["postcode"], forms.CharField)
    assert "country" in form.fields
    assert isinstance(form.fields["country"], LazyTypedChoiceField)
    assert "county" in form.fields
    assert isinstance(form.fields["county"], forms.CharField)


@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        # Invalid Email
        pytest.param(
            "email",
            "johndoegmail.com",
            "Enter a valid email address.",
            id="missing_at_symbol",
        ),
        pytest.param(
            "email",
            "johndoe@gmailcom",
            "Enter a valid email address.",
            id="missing_dot_in_domain",
        ),
        pytest.param(
            "email",
            "johndoe@.com",
            "Enter a valid email address.",
            id="missing_local_part",
        ),
        pytest.param(
            "email",
            "@gmail.com",
            "Enter a valid email address.",
            id="missing_local_part_and_username",
        ),
        pytest.param(
            "email",
            "john.doe@com",
            "Enter a valid email address.",
            id="missing_subdomain",
        ),
        pytest.param(
            "email",
            "john..doe@gmail.com",
            "Enter a valid email address.",
            id="double_dot_in_local_part",
        ),
        pytest.param(
            "email",
            "john.doe@gmail..com",
            "Enter a valid email address.",
            id="double_dot_in_domain",
        ),
        pytest.param(
            "email",
            "john.doe@gmail.c",
            "Enter a valid email address.",
            id="domain_too_short",
        ),
        pytest.param(
            "email",
            "john.doe@.gmail.com",
            "Enter a valid email address.",
            id="dot_at_start_of_domain",
        ),
        pytest.param(
            "email",
            "john.doe.@gmail.com",
            "Enter a valid email address.",
            id="dot_at_end_of_local_part",
        ),
        pytest.param(
            "email",
            "john.doe@gmail .com",
            "Enter a valid email address.",
            id="space_in_domain",
        ),
        pytest.param(
            "email",
            "john.doe@ gmail.com",
            "Enter a valid email address.",
            id="space_before_domain",
        ),
        # Invalid first name
        pytest.param(
            "first_name",
            "",
            "This field is required.",
            id="first_name_required",
        ),
        pytest.param(
            "first_name",
            "Jayden Kasper Leroy Maximilian Ned",
            "Ensure this value has at most 30 characters (it has 34).",
            id="first_name_too_long",
        ),
        # Invalid last name
        pytest.param(
            "last_name",
            "",
            "This field is required.",
            id="last_name_required",
        ),
        pytest.param(
            "first_name",
            "Wolfeschlegelsteinhausenbergerdorff",
            "Ensure this value has at most 30 characters (it has 35).",
            id="first_name_too_long",
        ),
        # Invalid phone number
        pytest.param(
            "phone_number",
            "",
            "This field is required.",
            id="phone_number_required",
        ),
        # Invalid address line 1
        pytest.param(
            "address_line_1",
            "",
            "This field is required.",
            id="address_line_1_required",
        ),
        # Invalid town city
        pytest.param(
            "town_city",
            "",
            "This field is required.",
            id="town_city_required",
        ),
        # Invalid country
        pytest.param(
            "country", "", "This field is required.", id="country_required"
        ),
    ],
)
def test_update_order_form_invalid_fields(field, value, expected_error):
    """
    Test validation errors for various fields in the UpdateOrderForm using invalid data.
    """
    form_data = {
        "email": "johndoe@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "address_line_1": "123 Main St",
        "address_line_2": "Apt 1",
        "town_city": "Springfield",
        "postcode": "12345",
        "country": "IE",
        "county": "Dublin",
    }

    form_data[field] = value

    form = UpdateOrderForm(data=form_data)

    assert not form.is_valid()
    assert expected_error in form.errors.get(field, [])


@pytest.mark.django_db
def test_add_order_item_form_has_correct_fields():
    """
    This test verifies that the AddOrderItemForm includes the 'product' and 'quantity' fields,
    and checks that 'product' is a ModelChoiceField and 'quantity' is an IntegerField.
    """
    form = AddOrderItemForm()

    assert "product" in form.fields
    assert isinstance(form.fields["product"], forms.ModelChoiceField)
    assert "quantity" in form.fields
    assert isinstance(form.fields["quantity"], forms.IntegerField)


@pytest.mark.django_db
def test_add_order_item_form_valid_data():
    """
    Test that the AddOrderItemForm processes valid data correctly.
    """
    category = CategoryFactory()
    product = ProductFactory(category=category)
    form_data = {"product": product.id, "quantity": 2}
    form = AddOrderItemForm(data=form_data)

    assert form.is_bound
    assert form.is_valid()
    assert form.cleaned_data["product"] == product
    assert form.cleaned_data["quantity"] == 2


@pytest.mark.django_db
def test_add_order_item_form_invalid_data():
    """
    Test that the AddOrderItemForm handles invalid data correctly.
    """
    category = CategoryFactory()
    product = ProductFactory(category=category)
    form_data = {"product": product.id, "quantity": -1}
    form = AddOrderItemForm(data=form_data)

    assert form.is_bound
    assert not form.is_valid()


@pytest.mark.django_db
def test_update_order_status_form_has_correct_fields():
    """
    Test that the UpdateOrderStatusForm has the correct fields and choices for 'status'.
    """
    form = UpdateOrderStatusForm()

    assert "status" in form.fields
    assert isinstance(form.fields["status"], forms.ChoiceField)

    expected_choices = [
        ("cancelled", "Cancelled"),
        ("complete", "Complete"),
        ("processing", "Processing"),
    ]
    assert form.fields["status"].choices == expected_choices


@pytest.mark.django_db
def test_update_order_status_form_valid_data():
    """
    Test that the UpdateOrderStatusForm is valid when given a correct status choice.
    Ensures the form processes and cleans the data as expected.
    """
    form_data = {"status": "complete"}
    form = UpdateOrderStatusForm(data=form_data)

    assert form.is_bound
    assert form.is_valid()
    assert form.cleaned_data["status"] == "complete"


@pytest.mark.django_db
def test_update_order_status_form_invalid_data():
    """
    Test that the UpdateOrderStatusForm is correctly invalid when given an invalid status choice.
    Ensures the form returns the appropriate error message.
    """
    form_data = {"status": "invalid"}
    form = UpdateOrderStatusForm(data=form_data)

    assert form.is_bound
    assert not form.is_valid()
    assert "status" in form.errors
    assert form.errors["status"] == [
        "Select a valid choice. invalid is not one of the available choices."
    ]
