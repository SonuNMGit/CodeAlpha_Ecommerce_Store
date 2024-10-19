from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):  
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        help_texts = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        
        error_messages = {
            'username': {
                'max_length': ("This username is too long."),
            },
            'password1': {
                'password_too_similar': ("Your password can’t be too similar to your other personal information."),
                'too_common': ("Your password can’t be a commonly used password."),
                'numeric': ("Your password can’t be entirely numeric."),
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data



