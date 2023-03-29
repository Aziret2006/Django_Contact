from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Contact, PhoneNumber, User

# class HelloForm(forms.Form):

#     first_name = forms.CharField(max_length='20', label='First name')
#     last_name = forms.CharField(max_length='20', label='Last name')
#     age = forms.IntegerField(max_value=100, min_value=0, label='Age')
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name']
        

class PhoneNumberForm(forms.ModelForm):
    
    class Meta:
        model = PhoneNumber
        fields = ['number']
        

class UserCreationForm(UserCreationForm):
    
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='Password confirm'
    )
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        help_texts = {
            'username': None,
        } 
        