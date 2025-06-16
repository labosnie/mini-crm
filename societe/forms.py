from django import forms
from .models import Societe


class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = "__all__"
