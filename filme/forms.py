from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


# Formulário de criação de conta do usuário. 
# Ele herda da classe UserCreationForm do Django, que já possui os campos de senha e confirmação de senha.
class CriarContaForm(UserCreationForm):
    # Adiciona o campo de e-mail ao formulário
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = Usuario # Tabela que é utilizada como base para a criação do formulário. Nesse caso, o modelo Usuario que foi criado no arquivo models.py da aplicação filme
        fields = ('username', 'email', 'password1', 'password2') # Campos que serão exibidos no formulário de criação de conta (password1 e password2 são os nomes obrigatórios dos campos de senha e confirmação de senha do Django)


# Formulário utilizado na página inicial do site
class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)  # Campo de e-mail sem rótulo
