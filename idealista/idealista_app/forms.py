from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email de acceso')
    passwd = forms.CharField(widget=forms.PasswordInput)

