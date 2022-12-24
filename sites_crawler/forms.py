from django import forms
from django.forms import TextInput
import re


class GrabForm(forms.Form):
    site_url = forms.URLField(widget=TextInput, label="")
