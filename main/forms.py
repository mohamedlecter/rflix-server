from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from main.models import Rating

class RatingForm(forms.ModelForm):
    stars = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'required': 'required'})
    )

    class Meta:
        model = Rating
        fields = ['stars']


class DeleteRatingForm(forms.Form):
    confirm = forms.BooleanField(required=True)

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password",
        min_length=6,  # You can adjust the minimum length
        help_text="Enter a password with at least 6 characters."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Password Confirmation",
        help_text="Re-enter the password for verification."
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': None,  # Remove default help text
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm
