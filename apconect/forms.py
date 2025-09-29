from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Anuncio
from .models import Profile

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    cep = forms.CharField(max_length=9, label='CEP')
    logradouro = forms.CharField(max_length=255, label='Endereço')
    numero = forms.CharField(max_length=20, label='Número')
    bairro = forms.CharField(max_length=100, label='Bairro')
    cidade = forms.CharField(max_length=100, label='Cidade')
    estado = forms.CharField(max_length=2, label='Estado (UF)')

    class Meta:
        model = User
        fields = ['username', 'email']

    @transaction.atomic # Garante que ou tudo salva, ou nada salva
    def save(self, commit=True):
        # Primeiro, salva o User
        user = super().save(commit=False)
        # O UserCreationForm lida com a senha, não precisamos nos preocupar
        
        if commit:
            user.save() # Salva o usuário no banco
            
            # Agora, cria e salva o Profile
            profile = Profile.objects.create(
                user=user,
                cep=self.cleaned_data.get('cep'),
                logradouro=self.cleaned_data.get('logradouro'),
                numero=self.cleaned_data.get('numero'),
                bairro=self.cleaned_data.get('bairro'),
                cidade=self.cleaned_data.get('cidade'),
                estado=self.cleaned_data.get('estado'),
            )
        return user


class AnuncioForm(forms.ModelForm):
    cep = forms.CharField(max_length=9, label='CEP', required=False)
    endereco_exibicao = forms.CharField(
        required=False,
        label='Endereço para exibição',
        help_text='Preencha o CEP e o endereço será preenchido automaticamente. Complete com o número.'
    )

    class Meta:
        model = Anuncio
        fields = ['titulo', 'descricao', 'categoria', 'imagem', 'cep', 'endereco_exibicao']