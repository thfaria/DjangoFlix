from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario # Importa os modelos necessários do arquivo models.py
from .forms import CriarContaForm, FormHomepage # Importa os formulários criados no arquivo forms.py
# Biblioteca necessária para utilização de Class Based Views (CBV)
from django.views.generic import TemplateView # Classe para renderizar templates HTML
from django.views.generic import ListView # Classe para listar objetos de um modelo
from django.views.generic import DetailView # Classe para listar os detalhes de um objeto específico de um modelo
from django.views.generic import FormView # Classe para renderizar formulários
from django.views.generic import UpdateView # Classe para atualizar objetos de um modelo do banco de dados
from django.contrib.auth.mixins import LoginRequiredMixin # Classe que obriga o usuário a estar logado para acessar as views. Configurações de redirecionamento ficam na settings.py


# View da Home do site

# Comentado abaixo temos uma Funcrtion Based View (FBV) que chama a homeapage.html
# def homepage(request):
#    return render(request, 'homepage.html') # Carrega a página homepage.html

# E agora a mesma chamada utilizando uma Class Based View (CBV)
class Homepage(FormView):
    template_name = 'homepage.html' # Nome do template HTML a ser carregado (é obrigatório o nome da variável ser esse)
    form_class = FormHomepage # Formulário utilizado na página inicial do site

    # Método get editado para retornar ao usuário a página correta, dependendo se ele esta ou não logado no site
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes') # Se o usuário estiver logado, redireciona para a classe de Homefilmes
        else:
            return super().get(request, *args, **kwargs) # Redireciona o usuário para a página padrão da classe (homepage.html)

    # Verifica se o e-mail infomrado existe no banco de dados e redirecionar o usuário conforme essa resposta
    def get_success_url(self):
        email = self.request.POST.get('email') # Pega o e-mail informado no formulário
        usuario = Usuario.objects.filter(email=email) # Busca no banco de dados um usuário com o e-mail informado
        if usuario:
            return reverse('filme:login') # Se o usuário existir, redireciona para a página de login
        else:
            return reverse('filme:criarconta') # Se o usuário não existir, redireciona para a página de criação de conta
    

# view da Home de Filmes
# Essa página irá receber uma lista com todos os filmes cadastrados no banco para presentação

# Chamnada da página na versão FBV
# def homefilmes(request):
#    context = {} # Dicionário por onde as informações são passadas para a página HTML
#    lista_filmes = Filme.objects.all() # Busca todos os filmes cadastrados no banco de dados
#    context['lista_filmes'] = lista_filmes # Adiciona a lista de filmes ao dicionário
#    return render(request, 'homefilmes.html', context) # Carrega a página homefilmes.html passando o dicionário como contexto 

# Chamada da página na versão CBV
# A inclusão da LoginRequiredMixin antes da classe base garante que o acesso a essa view só é permitido para usuários logados no site
class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html' # Nome do template HTML a ser carregado (é obrigatório o nome da variável ser esse)
    model = Filme # Modelo que será utilizado para a listagem dos objetos (é obrigatório o nome da variável ser esse)
    # object_list - É o nome da váriável que contem a lista retornada do banco


# View para apresentar os detalhes de um filme específico
# A inclusão da LoginRequiredMixin antes da classe base garante que o acesso a essa view só é permitido para usuários logados no site
class DetalhesFilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object - diferente da ListView, aqui é retornado para a págna HTML um único objeto (object) e não uma lista (object_list)

    # O método get_context_data é o responsável por pasar as informações para o template HTML
    # Esse método pode ser reenscrito para passar mais infomrações ou até mesmo informações completamente novas
    # Nossa idéia é passar uma lista de filmes relacionados (com a mesma catgegoria) ao filme que foi detalhado
    def get_context_data(self, **kwargs):
        context = super(DetalhesFilme, self).get_context_data(**kwargs) # Com essa linha garantimos que o método siga com seu funcionamento normal, adicionando novas infonmrações ao contexto

        # Após garantir a continuidade do contexto, incluimos as novas informações
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria).exclude(id=self.get_object().id)[0:5] # Filtrar os filmes que possuam a mesma categoria do filme detalhado, excluindo ele mesmo. São pasados apenas 5 filmes 
        context['filmes_relacionados'] = filmes_relacionados # Adiciona a lista de filmes relacionados ao contexto (com a chave 'filmes_relacionados')

        return context # Retorna o contexto atualizado
    
    # Redefinindo o método get da DetalheFilme para contar o acesso do usuário como uma visualização do filme
    # Adicionamos também o filme a lista de Filmes_vistos no banco de dados relativo ao usuário
    # Esse método é chamado sempre que o usuário acessa a página de detalhes do filme
    def get(self, request, *args, **kwargs):
        filme = self.get_object() # Filme que esta sendo detalhado
        filme.visualizacoes += 1 # Aumenta o número de visualizações do mesmo
        filme.save() # Salva a alteração em banco

        usuario = request.user # Pega o usuário que está acessando a página
        usuario.filmes_vistos.add(filme) # Adiciona o filme a lista de filmes vistos do usuário

        return super().get(request, *args, **kwargs) # O retorno desse método não é alterado no final das contas
    

# View que apresenta os filmes resultantes de uma pesquisa
# A inclusão da LoginRequiredMixin antes da classe base garante que o acesso a essa view só é permitido para usuários logados no site
class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html' # Nome do template HTML a ser carregado (é obrigatório o nome da variável ser esse)
    model = Filme # Modelo que será utilizado para a listagem dos objetos (é obrigatório o nome da variável ser esse)
    # object_list - É o nome da váriável que contem a lista retornada do banco

    # Redefinindo o metodo get_queryset que devolve à página HTML o object_list resultante de uma ListView (no caso da ListView utilizada pela classe acima)
    def get_queryset(self):
        # Pega o parametro de pesquisa que foi passado a partir do campó de pesquisa da barra de navegação
        termo_pesquisa = self.request.GET.get('query')

        # Se alguma pesquisa tiver sido realizada...
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains = termo_pesquisa) # Verifica se o termo existe em algum dos titulos dos filmes
            return object_list # E retorna o resultado para a página
        else:
            return None # Se nada foi pesquisado, retorna nada
        

# View que possibilita ao usuário editar seu perfil no site
class EditarPerfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario # Tabela do banco de dados que terá os dados atualizados a partir desse formulário
    fields = ['first_name', 'last_name', 'email'] # Campos que serão atualizados

    # Método que define para onde o formulário redireciona o usuário em caso de sucesso
    def get_success_url(self):
        return reverse('filme:homefilmes')


# View de criação de conta dos usuários
class CriarConta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm # Formulário que será utilizado para a criação da conta

    # Método que verifica se o formulário é válido e, por realizar uma alteração em banco, salva os dados criados
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # Método que define para onde o formulário redireciona o usuário em caso de sucesso
    def get_success_url(self):
        return reverse('filme:login')