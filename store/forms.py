from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        errors = []

        # Validações personalizadas para a senha
        if password:
            if len(password) < 8:
                errors.append("A senha deve ter pelo menos 8 caracteres.")
            if not re.search(r'\d', password):
                errors.append("A senha deve conter pelo menos um número.")
            if not re.search(r'[A-Z]', password):
                errors.append("A senha deve conter pelo menos uma letra maiúscula.")
            if password.isnumeric():
                errors.append("A senha não pode ser apenas numérica.")
            if password.lower() == password:  # Evita senhas comuns (ex: "senha123")
                errors.append("A senha não pode ser muito comum.")
        
        if errors:
            raise ValidationError(errors[0])  # Mostra apenas o primeiro erro

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Verifica se as senhas coincidem
        if password1 != password2:
            raise ValidationError("As senhas não coincidem.")
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['first_name'].lower()  # Usa o primeiro nome como username
        if commit:
            user.save()
        return user

from django import forms

class CustomUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
