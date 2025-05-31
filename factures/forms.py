from django import forms
from .models import Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['client', 'projet', 'montant', 'date_echeance', 'statut_paiement', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'projet': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_echeance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut_paiement': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les projets en fonction du client sélectionné
        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                self.fields['projet'].queryset = self.fields['projet'].queryset.filter(client_id=client_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.client:
            self.fields['projet'].queryset = self.fields['projet'].queryset.filter(client=self.instance.client) 