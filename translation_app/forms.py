from django import forms

class TranslationForm(forms.Form):
    target_language = forms.CharField(max_length=2)
    file = forms.FileField()

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
