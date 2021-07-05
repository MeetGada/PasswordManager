from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import credentials
from django import forms

class customUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'autocomplete':"off"}),
            'last_name': forms.TextInput(attrs={'autocomplete':"off"}),
            'email': forms.EmailInput(attrs={'autocomplete':"off"}),
            'username': forms.TextInput(attrs={'autocomplete':"off"}),
        }

class credentialsForm(forms.ModelForm):
    class Meta:
        model = credentials
        fields = '__all__'
        exclude = ['name','key']

        widgets = {
            'description': forms.TextInput(attrs={'autocomplete':"off"}),
            'user_id': forms.TextInput(attrs={'maxlength':20, 'autocomplete':"off"}),
            'password': forms.TextInput(attrs={'maxlength':50, 'autocomplete':"off"}),
        }
    
    def clean_user_id(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')

        if len(user_id) > 21:
            raise forms.ValidationError('User Id should less 20 characters')
        else:
            return user_id
     
    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        if len(password) > 51:
            raise forms.ValidationError('Password should be less than 50 characters')
        else:
            return password