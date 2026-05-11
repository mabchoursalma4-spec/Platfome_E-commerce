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
    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        
        # Supprimer tous les messages d'aide 
        for field in self.fields:
            self.fields[field].help_text = None
            
            #  Appliquer automatiquement le style 
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-3 bg-white border border-beige-300 rounded-xl text-sm focus:outline-none focus:border-caramel focus:ring-1 focus:ring-caramel transition-all duration-300',
                'placeholder': f'Entrez votre {self.fields[field].label.lower()}'
            })
        


class ConnexionForm(forms.ModelForm):
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