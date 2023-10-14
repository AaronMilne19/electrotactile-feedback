"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _ 


#TODO: edit the name of this/potentially change structure.
class MainForm(forms.Form):
    options = ( 
        ("1", "One"), 
        ("2", "Two"), 
        ("3", "Three"), 
        ("4", "Four"), 
        ("5", "Five"), 
    )
    radio_options = forms.ChoiceField(choices=options, widget=forms.RadioSelect, label="Try selecting an option")
    test = forms.CharField(label="Enter your text", max_length=100)


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
