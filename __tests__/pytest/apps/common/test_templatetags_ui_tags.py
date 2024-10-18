import pytest
from django.utils.safestring import SafeString

from apps.common.templatetags.ui_tags import icon

icons_data = [
    {
        "icon": "icon-envelope",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M30.84,6.87c-.21-.56-.6-1.01-1.11-1.31-.37-.21-.79-.35-1.25-.35H3.53c-.46,0-.88.13-1.25.35-.51.29-.9.75-1.11,1.31-.1.27-.17.57-.17.87v16.51c0,.35.07.68.2.99.23.54.65.98,1.17,1.25.35.18.74.29,1.16.29h24.95c.42,0,.81-.11,1.16-.29.52-.27.94-.71,1.17-1.25.13-.3.2-.64.2-.99V7.75c0-.31-.06-.6-.16-.87ZM28.36,6.93l-7.94,7.94-1.21,1.21-2.72,2.72c-.27.27-.73.26-1,0l-2.72-2.72-1.21-1.21L3.64,6.93h24.72ZM2.71,8.42l7.66,7.66-7.66,7.66v-15.32ZM3.79,25.07l7.79-7.79,2.72,2.72c.47.47,1.09.71,1.71.71s1.24-.24,1.71-.71l2.72-2.72,7.79,7.79H3.79ZM29.29,23.73l-7.66-7.66,7.66-7.66v15.32Z"/></svg></span></span>',
    },
    {
        "icon": "icon-facebook",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M12.82,31v-13.68h-4.61v-5.33h4.61v-3.93c0-4.56,2.79-7.05,6.86-7.05,1.95,0,3.63.15,4.12.21v4.77h-2.82c-2.21,0-2.64,1.05-2.64,2.6v3.4h5.28l-.69,5.33h-4.59v13.68h-5.51Z"/></svg></span></span>',
    },
    {
        "icon": "icon-hamburger",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 32 32"><path d="M28.9,28.3H3.1c-1.4,0-2.6-1.2-2.6-2.6s1.2-2.6,2.6-2.6h25.9c1.4,0,2.6,1.2,2.6,2.6s-1.2,2.6-2.6,2.6ZM31.6,16c0-1.4-1.2-2.6-2.6-2.6H3.1c-1.4,0-2.6,1.2-2.6,2.6s1.2,2.6,2.6,2.6h25.9c1.4,0,2.6-1.2,2.6-2.6ZM31.6,6.3c0-1.4-1.2-2.6-2.6-2.6H3.1C1.6,3.7.4,4.9.4,6.3s1.2,2.6,2.6,2.6h25.9c1.4,0,2.6-1.2,2.6-2.6Z"/></svg></span></span>',
    },
    {
        "icon": "icon-instagram",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M9.33,1C4.74,1,1,4.74,1,9.33v13.33c0,4.59,3.74,8.33,8.33,8.33h13.33c4.59,0,8.33-3.74,8.33-8.33v-13.33c0-4.59-3.74-8.33-8.33-8.33h-13.33ZM9.33,4.33h13.33c2.76,0,5,2.24,5,5v13.33c0,2.76-2.24,5-5,5h-13.33c-2.76,0-5-2.24-5-5v-13.33c0-2.76,2.24-5,5-5ZM24.33,6c-.92,0-1.67.75-1.67,1.67s.75,1.67,1.67,1.67,1.67-.75,1.67-1.67-.75-1.67-1.67-1.67ZM16,7.67c-4.59,0-8.33,3.74-8.33,8.33s3.74,8.33,8.33,8.33,8.33-3.74,8.33-8.33-3.74-8.33-8.33-8.33ZM16,11c2.76,0,5,2.24,5,5s-2.24,5-5,5-5-2.24-5-5,2.24-5,5-5Z"/></svg></span></span>',
    },
    {
        "icon": "icon-linkedin",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M1,11h7v20H1V11ZM4.5,1c-1.93,0-3.5,1.57-3.5,3.5s1.57,3.5,3.5,3.5,3.5-1.57,3.5-3.5-1.57-3.5-3.5-3.5ZM23.54,11c-3.02,0-5.05,1.12-5.88,2.7h-.09v-2.7h-5.58v20h5.83v-9.91c0-2.61.49-5.15,3.73-5.15s3.44,2.99,3.44,5.31v9.74h6v-10.99c0-5.4-1.16-9.01-7.46-9.01Z"/></svg></span></span>',
    },
    {
        "icon": "icon-location",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M7.42,21.62h4.69c.27,0,.54,0,.67.27s.27.4.27.67,0,.54-.27.67-.4.27-.67.27h-4.16l-4.16,5.63h24.26l-4.16-5.63h-4.16c-.27,0-.54,0-.67-.27s-.27-.4-.27-.67,0-.54.27-.67.4-.27.67-.27h5.09s.27.13.27.27l5.63,7.51c0,.13.13.27.13.54v.54c0,.13-.13.27-.4.4-.13,0-.27.13-.54.13H2.06c-.13,0-.4,0-.54-.13-.13,0-.27-.27-.4-.4v-.54c0-.13,0-.4.13-.54l5.63-7.51s.4-.27.54-.27ZM15.87,2.98c-.67,0-1.47.13-2.14.4-.67.27-1.34.67-1.88,1.21s-.94,1.07-1.21,1.88c-.27.67-.4,1.34-.4,2.14s.13,1.47.4,2.14c.27.67.67,1.34,1.21,1.88s1.07.94,1.88,1.21c.67.27,1.34.4,2.14.4,1.47,0,2.95-.54,3.89-1.61,1.07-1.07,1.61-2.41,1.61-3.89s-.53-3.26-1.6-4.19c-1.5-1.73-3.9-1.57-3.9-1.57ZM8.36,8.48c0-1.47.4-2.82,1.21-4.02.8-1.21,1.88-2.14,3.22-2.82,1.34-.54,2.82-.8,4.16-.54,1.47.27,2.68.8,3.75,1.74,1.07.94,1.88,2.14,2.28,3.62.4,1.34.4,2.82,0,4.16s-1.21,2.55-2.28,3.49c-1.07.94-2.41,1.47-3.89,1.74v10.32c0,.27,0,.54-.27.67s-.4.27-.67.27-.54,0-.67-.27-.27-.4-.27-.67v-10.32c-1.74-.27-3.49-1.07-4.69-2.41s-1.88-3.08-1.88-4.96Z"/></svg></span></span>',
    },
    {
        "icon": "icon-phone",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M23.44,31c-.99,0-1.98-.13-2.95-.38C13.36,28.82,3.18,18.64,1.38,11.5c-.74-2.82-.39-5.8.99-8.38,1-1.92,3.39-2.67,5.32-1.67.36.19.68.42.97.71l2.92,2.92c1.14,1.13,1.48,2.89.83,4.36-.3.71-.74,1.37-1.28,1.93-.37.37-.44.96-.23,1.77.79,2.94,5.03,7.18,7.97,7.97.81.22,1.4.14,1.76-.21.58-.56,1.23-1,1.96-1.31,1.47-.65,3.23-.31,4.36.84l2.91,2.92c1.54,1.54,1.53,4.05-.01,5.58-.29.29-.61.52-.97.71-1.69.9-3.55,1.36-5.43,1.36ZM5.87,2.99c-.2,0-.4.03-.59.09-.5.16-.9.5-1.14.96-1.15,2.15-1.44,4.61-.82,6.95,1.63,6.48,11.21,16.06,17.68,17.68,2.35.62,4.82.33,6.95-.81.19-.1.35-.21.49-.36.37-.37.57-.86.57-1.38s-.2-1.01-.57-1.38l-2.92-2.92c-.56-.57-1.43-.73-2.15-.41-.51.22-.96.52-1.35.9-.61.61-1.74,1.24-3.67.72-3.66-.98-8.4-5.71-9.38-9.38-.52-1.93.11-3.07.73-3.68.36-.38.66-.83.88-1.33.32-.74.16-1.6-.41-2.16l-2.92-2.92c-.14-.14-.3-.26-.48-.35-.28-.15-.59-.22-.9-.22Z"/></svg></span></span>',
    },
    {
        "icon": "icon-search",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M30.2,27.49l-7.19-7.19c1.67-2.3,2.56-5.19,2.27-8.3-.52-5.59-4.96-10.2-10.54-10.9C6.79.1.08,6.82,1.1,14.77c.71,5.51,5.24,9.91,10.77,10.49,3.03.31,5.87-.49,8.15-2.06l7.23,7.23c.31.31.82.31,1.13,0l1.82-1.82c.31-.31.31-.82,0-1.13ZM4.69,14.62c-.97-5.87,4.06-10.9,9.93-9.93,3.56.59,6.43,3.46,7.02,7.02.97,5.87-4.06,10.9-9.93,9.93-3.56-.59-6.43-3.46-7.02-7.02Z"/></svg></span></span>',
    },
    {
        "icon": "icon-twitter",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M28.55,27.94l-9.82-14.27L29.62,1h-2.49l-2.13,2.47-7.38,8.59L10.59,1.85l-.58-.85H1.38l2.11,3.06,9.34,13.58L1.34,31h2.49l10.1-11.75,7.51,10.91.58.85h8.63l-2.11-3.06ZM23.05,29.05l-7.8-11.33-1.11-1.61L5.09,2.95h3.89l7.32,10.63,1.11,1.61,9.53,13.85h-3.89Z"/></svg></span></span>',
    },
    {
        "icon": "icon-web",
        "size": "sm",
        "expected": '<span class="flex transition-all"><span class="inline-block w-4 h-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 29.66 29.8"><path d="M2.27,6.9C4.92,2.76,9.55,0,14.83,0c.05,0,.09,0,.14,0,.02,0,.04,0,.06,0,.06,0,.11.02.17.02,5.12.13,9.6,2.84,12.18,6.88h-3.77c-1.08-1.18-2.38-2.14-3.85-2.81.41.84.76,1.79,1.07,2.81h-3.14c-.89-2.49-2.02-3.81-2.61-3.89-.03,0-.06,0-.09,0-.58.05-1.73,1.37-2.63,3.89h-3.14c.33-1.12.73-2.15,1.18-3.04-1.68.68-3.17,1.72-4.37,3.04h-3.77ZM23.61,22.9c-1.08,1.18-2.38,2.14-3.85,2.81.41-.84.76-1.79,1.07-2.81h-3.14c-.89,2.49-2.02,3.81-2.61,3.89-.03,0-.06,0-.09,0-.58-.05-1.73-1.37-2.63-3.89h-3.14c.33,1.12.73,2.15,1.18,3.04-1.68-.68-3.17-1.72-4.37-3.04h-3.77c2.65,4.14,7.27,6.9,12.56,6.9.05,0,.09,0,.14,0,.02,0,.04,0,.06,0,.06,0,.11-.02.17-.02,5.12-.13,9.6-2.84,12.18-6.88h-3.77ZM1.31,18.62h3.08l.61-4.93h.13l.58,4.93h2.94l1.24-7.56h-2.38l-.26,4.56h-.17l-.35-3.33c-.17-1.14-.46-1.27-1.68-1.27-.47,0-1.01.05-1.46.12l-.41,4.49h-.17l-.26-3.31c-.1-1.16-.36-1.31-1.27-1.31-.49,0-1.1.08-1.48.18l1.31,7.44ZM11.2,18.62h3.08l.61-4.93h.13l.58,4.93h2.94l1.24-7.56h-2.38l-.26,4.56h-.17l-.35-3.33c-.17-1.14-.46-1.27-1.68-1.27-.47,0-1.01.05-1.46.12l-.41,4.49h-.17l-.26-3.31c-.1-1.16-.36-1.31-1.27-1.31-.49,0-1.1.08-1.48.18l1.31,7.44ZM21.08,18.62h3.08l.61-4.93h.13l.58,4.93h2.94l1.24-7.56h-2.38l-.26,4.56h-.17l-.35-3.33c-.17-1.14-.46-1.27-1.68-1.27-.47,0-1.01.05-1.46.12l-.41,4.49h-.17l-.26-3.31c-.1-1.16-.36-1.31-1.27-1.31-.49,0-1.1.08-1.48.18l1.31,7.44Z"/></svg></span></span>',
    },
]

sizes = {
    "sm": "w-4 h-4",
    "md": "w-6 h-6",
    "lg": "w-9 h-9",
}


@pytest.mark.parametrize("icon_data", icons_data)
def test_icon(icon_data):
    result = icon(icon_data["icon"], icon_data["size"])
    assert isinstance(result, SafeString)
    assert icon_data["expected"] in str(result)


@pytest.mark.parametrize("size, expected_class", sizes.items())
def test_icon_with_size(size, expected_class):
    result = icon("icon-facebook", size=size)
    assert expected_class in result


def test_icon_with_class_name():
    result = icon("icon-facebook", class_name="custom-class")
    assert "custom-class" in result


def test_icon_not_found():
    result = icon("icon-non-existent")
    assert "Icon not found" in result
