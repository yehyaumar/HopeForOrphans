from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'password':forms.PasswordInput(attrs={'placeholder':'Password'})
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder':'Password'})

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password'})


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)