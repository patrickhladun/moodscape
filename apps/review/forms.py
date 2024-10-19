from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.RadioSelect(
                choices=[
                    (5, "5 Stars"),
                    (4, "4 Stars"),
                    (3, "3 Stars"),
                    (2, "2 Stars"),
                    (1, "1 Star"),
                ]
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter your review...",
                }
            ),
        }
        error_messages = {
            "rating": {
                "required": "Please select a rating.",
            },
            "text": {
                "required": "Please enter your review text.",
            },
        }


class ReviewStatusForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["status"]
