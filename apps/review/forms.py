from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=[
                (5, '5 Star'),
                (4, '4 Stars'),
                (3, '3 Stars'),
                (2, '2 Stars'),
                (1, '1 Stars'),
            ]),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ReviewStatusForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['status']