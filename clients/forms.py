from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'ville', 'code_postal', 'pays', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        } 