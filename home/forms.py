from django import forms
from django.contrib.auth.forms import AuthenticationForm

from home.models import Orphanage, Contact, Address, BankDetail, Orphan


class OrphanageSignUpForm(forms.ModelForm):
    class Meta:
        model = Orphanage
        fields = ('name', 'display_pic', 'reg_num','brief_desc')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'Name'}),
            'reg_num': forms.TextInput(attrs={'placeholder':'Registration Number'}),
            'brief_desc': forms.Textarea(attrs={'placeholder': 'Brief Description'}),
            'display_pic': forms.FileInput(attrs={'class':'dp_upload', 'id':'file_upload'})
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('locality', 'city', 'state', 'zip_pin_code', 'country')
        widgets = {
            'locality': forms.TextInput(attrs={'placeholder': 'Locality'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'zip_pin_code': forms.NumberInput(attrs={'placeholder': 'Zip/Pin Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('phone_number', 'mobile_number', 'website')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'website': forms.URLInput(attrs={'placeholder': 'Website'}),
        }


class BankDetailForm(forms.ModelForm):
    class Meta:
        model = BankDetail
        fields = ('MERCHANT_KEY', 'MERCHANT_SALT')


class OrphanForm(forms.ModelForm):
    class Meta:
        model = Orphan
        fields = ('first_name', 'last_name', 'dob', 'gender', 'status', 'hobbies',
                  'education', 'date_joined', 'avatar')


class MyAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(
            attrs={'placeholder': 'Email'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder':'Password'})
