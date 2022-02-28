from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterForm(forms.ModelForm):
    password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    retype_password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
    def clean(self):
        super().clean()
        p1=self.cleaned_data.get('password')
        p2=self.cleaned_data.get('retype_password')
        if p1!=p2:
            raise forms.ValidationError('Password must be same')

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20,widget=forms.PasswordInput)
    def clean(self):
        u=self.cleaned_data.get('username')
        p=self.cleaned_data.get('password')
        x=authenticate(username=u,password=p)
        if x is False:
            raise forms.ValidationError('Username or password is incorrect')
    




