from django import forms
from .models import Produit, Categorie


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
        }


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'nom',
            'description',
            'image',
            'prix',
            'stock',
            'categorie',
        ]

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du produit'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description du produit',
                'rows': 4
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prix du produit'
            }),

            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantité en stock'
            }),

            'categorie': forms.Select(attrs={
                'class': 'form-select'
            }),
        }