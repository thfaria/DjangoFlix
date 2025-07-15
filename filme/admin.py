from django.contrib import admin
from .models import Filme, Episodio, Usuario # Importa do arquivo models.py as classes  que representam as tabelas no banco de dados
from django.contrib.auth.admin import UserAdmin # Biblioteca responsável pela administração de usuários no Django


# O novo campo incluido ao usuário precisa ser adcionado a lista de campos apresentados pelo UserAdmin para que ele apareça na área de admin do sistema 
campos = list(UserAdmin.fieldsets) #Pega a tupla de campos do UserAdmin e transforma em uma lista
# A nova sessão e campos precisam ser adicionados conforme a estrutura abaixo
campos.append(
    ('Histórico de visualizações', {'fields': ('filmes_vistos',)}) #Tupla onde o primeiro item é o nome da sessão e o segundo item é outra tupla com os nomes dos campos
)
UserAdmin.fieldsets = tuple(campos) # Ao final altera-se os campos apresntados pelo UserAdmin

# Todas essas alterações acima se fazem necessárias apenas para que o campo criado esteja vísivel na área de Admin do site.
# Se nada disso for feito o campo seguirá existindo no banco de dados (já que foi criado no models.py), mas não estará visível ou editável no Admin.


# Register your models here.
# Registra a classe Filme no admin do Django, permitindo que ela seja gerenciada através da interface administrativa
admin.site.register(Filme) 
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin) # Além de registrar a tabela de usuários no aplicativo é necessário informar que essa tabela continua realizando toda a aprte de administração de usuários do sistema