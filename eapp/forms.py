
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from eapp.models import Contact, Profile, Address, Review


class RegisterForm(UserCreationForm):
    username = forms.CharField(label_suffix=' ',widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label_suffix=' ',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password',label_suffix=' ',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'email': 'E-mail'}

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label_suffix=' ',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label_suffix=' ',widget=forms.PasswordInput(attrs={'class': 'form-control'}))        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StateSelectWidget(forms.Select):
    # Define custom choices for the state field
    choices = Address.STATE_CHOICES

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'phone', 'street',
                  'city', 'zipcode', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': StateSelectWidget(attrs={'class': 'form-control'})
            
        }

class ReviewSelectWidget(forms.Select):
    # Define custom choices for the state field
    choices = Review.RATING_CHOICES        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review 
        fields =  ['name','rating','review', ]   
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'review': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': StateSelectWidget(attrs={'class': 'form-control'})

        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact    
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
