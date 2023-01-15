from django import forms
from .models import User


# User Login Form
class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # to hide the password-field-value while typing

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        # NB: use this func in order to make custom-validation of each/certain field(s)
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class UserPasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        # NB: use this func in order to make custom-validation of each/certain field(s)
        # print(self.cleaned_data['password'])
        # print(self.cleaned_data['repeat_password'])
        if self.is_valid():
            password = self.cleaned_data['password']
            repeat_password = self.cleaned_data['repeat_password']
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['repeat_password'].widget.attrs['class'] = 'form-control'
        self.fields['repeat_password'].widget.attrs['placeholder'] = 'Confirm Password'
