import pytest
from django.template import Context, Template

from apps.common.templatetags.text_tags import addstr


@pytest.mark.parametrize(
    "value, arg, expected",
    [
        ("Hello", "World", "HelloWorld"),
        ("123", "456", "123456"),
        ("foo", "", "foo"),
        ("", "bar", "bar"),
        (123, 456, "123456"),
        (None, "bar", "Nonebar"),
    ],
)
def test_addstr_filter(value, arg, expected):
    result = addstr(value, arg)
    assert result == expected
