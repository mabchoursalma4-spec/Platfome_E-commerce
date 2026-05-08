from django import forms
from .models import Commande, LigneCommande, StatutCommande


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['statut']

        widgets = {
            'statut': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class LigneCommandeForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        fields = [
            'produit',
            'quantite',
        ]

        widgets = {
            'produit': forms.Select(attrs={
                'class': 'form-select'
            }),

            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Quantité'
            }),
        }

    def clean_quantite(self):
        quantite = self.cleaned_data.get('quantite')

        if quantite <= 0:
            raise forms.ValidationError("La quantité doit être supérieure à 0.")

        return quantite