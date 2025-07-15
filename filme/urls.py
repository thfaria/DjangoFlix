# Para cada novo link no seu site é preciso definir 3 coisas:
# 1. A URL a ser acessada
# 2. A view que é a programação por tras da página
# 3. O tgemplate HTML a ser apresentado

# A forma como esse arquivo de URLs é configurado é amesma do arquivo de URLs presente no projeto (djangoflix/urls.py)


from django.urls import path # Função responsável por definir as URLs do site
from django.urls import reverse_lazy # Função utilizada para redirecionar o usuário para uma URL específica após uma ação bem-sucedida
from .views import Homepage, Homefilmes, DetalhesFilme, PesquisaFilme, EditarPerfil, CriarConta # Importa as views do arquivo views.py da aplicação filme
from django.contrib.auth.views import LoginView, LogoutView # Importa as views de Login e Logout do Django, que serão utilizadas para criar as páginas de login e logout do site
from django.contrib.auth.views import PasswordChangeView # Importa a view de Mudança de Senha do Django, que será utilizada para criar a página de mudança de senha do usuário

app_name = 'filme' # Define o namespace da aplicação filme, para que as URLs sejam únicas e não haja conflito com outras aplicações do projeto

urlpatterns = [
    #path('', homepage), # Chama a view homepage quando o usuário acessa a raiz do site (FBV)
    path('', Homepage.as_view(), name='homepage'), # Chama a view Homepage quando o usuário acessa a raiz do site (CBV)
    path('filmes/', Homefilmes.as_view(), name='homefilmes'), # Chama a view homefilmes quando o usuário acessa o caminho especificado (filmes/)
    path('filmes/<int:pk>/', DetalhesFilme.as_view(), name='detalhesfilme'), # Chama a view DetalhesFilme, passando a chave primaria (pk) do filme 
    path('pesquisa/', PesquisaFilme.as_view(), name='pesquisafilme'), # Chama a view PesquisaFilmes, passando o parametro para pesquisa 
    path('login/', LoginView.as_view(template_name='login.html'), name='login'), # Cahama a view de Login padrão do Django. Passa o parametro template_name com o nome da página HTML a ser chamada
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'), # Cahama a view de Logout padrão do Django. Passa o parametro template_name com o nome da página HTML a ser chamada
    path('editarperfil/<int:pk>/', EditarPerfil.as_view(), name='editarperfil'), # Chama a view EditarPerfil, passando a chave primaria do usuário que esta logado (e que será editado)
    path('criarconta/', CriarConta.as_view(), name='criarconta'), # Chama a view CriarConta, que será responsável por criar um novo usuário no site
    path('mudarsenha/', PasswordChangeView.as_view(template_name='editarperfil.html', success_url=reverse_lazy('filme:homefilmes')), name='mudarsenha'), # A mudança de senha utiliza a mesma página HTML da edição de perfil como base, já que a única alteração entre elas é o formulário apresentado. Na chamada já é passado o parâmetro success_url, que redireciona o usuário após a mudança de senha ser bem-sucedida
]