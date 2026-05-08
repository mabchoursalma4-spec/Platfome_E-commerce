from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Utilisateur


class InscriptionForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'numero_tel',
            'adresse',
            'password1',
            'password2',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom d'utilisateur"
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse email'
            }),

            'numero_tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de téléphone'
            }),

            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse'
            }),
        }


class ProfilUtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = [
            'first_name',
            'last_name',
            'email',
            'numero_tel',
            'adresse',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),

            'numero_tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone'
            }),

            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse'
            }),
        }


class AdminUtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'numero_tel',
            'adresse',
            'is_staff',
            'is_active',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'numero_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),

            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }