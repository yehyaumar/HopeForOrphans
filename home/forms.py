from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CheckboxSelectMultiple, SelectDateWidget

from home.models import Orphanage, Contact, Address, BankDetail, Orphan, AdoptionRequest


class OrphanageSignUpForm(forms.ModelForm):
    class Meta:
        model = Orphanage
        fields = ('name', 'display_pic', 'reg_num','brief_desc', 'income_source',
                  'facilities', 'date_estd')

        this_year = datetime.now().year

        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'Name'}),
            'reg_num': forms.TextInput(attrs={'placeholder':'Registration Number'}),
            'brief_desc': forms.Textarea(attrs={'placeholder': 'Brief Description'}),
            'display_pic': forms.FileInput(attrs={'class':'dp_upload', 'id':'file_upload'}),
            'date_estd': SelectDateWidget(years=range(1900,this_year+1), attrs={'class': 'date-time'}),
            'income_source': CheckboxSelectMultiple(),
            'facilities': CheckboxSelectMultiple,
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('locality', 'city', 'state', 'zip_pin_code', 'country')
        widgets = {
            'locality': forms.TextInput(attrs={'placeholder': 'Locality'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'zip_pin_code': forms.TextInput(attrs={'placeholder': 'Zip/Pin Code'}),
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
        fields = ('merchant_key', 'merchant_salt')
        widgets = {
            'merchant_key': forms.TextInput(attrs={'placeholder': 'Merchant Key'}),
            'merchant_salt': forms.TextInput(attrs={'placeholder': 'Merchant Salt'}),
        }


class OrphanForm(forms.ModelForm):
    class Meta:
        model = Orphan
        fields = ('first_name', 'last_name', 'dob', 'gender', 'status')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'gender': forms.Select(),
            'dob': forms.SelectDateWidget(years=range(1990, 2019), attrs={'class': 'date-time'}),
            'status': forms.Select(),
        }


class MyAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(
            attrs={'placeholder': 'Email'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder':'Password'})


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ('first_name', 'last_name', 'dob', 'phone_number', 'email',
                  'occupation', 'income', 'married', 'family_members', 'mobile_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'dob': forms.SelectDateWidget(years=range(1990, 2019), attrs={'class': 'date-time'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Occupation'}),
            'income': forms.NumberInput(attrs={'placeholder': 'Annual Income'}),
            'family_members': forms.NumberInput(attrs={'placeholder': 'Family Members'}),

        }


class AdoptionApprovalForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ('approved',)

        widgets = {
            'approved': forms.Select(),
        }
