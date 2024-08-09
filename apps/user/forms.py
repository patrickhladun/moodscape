from django import forms
from .models import User

class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']

