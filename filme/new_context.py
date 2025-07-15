# Gerenciador de contexto - onde definimos todas aas variáveis que poderão ser acessadas em qualquer página HTML do nosso aplicativo
# Para se tornarem ativos no aplicativo, essas fuhnções precisam ser registradas no settings.py do projeto (em TEMPLATES, OPTIONS, CONTEXT_PROCESSORS)

from .models import Filme # Importa o modelo Filme do arquivo models.py da aplicação filme


# Função que vai retornar a lista de filmes vistos recentemente pelo usuário para a página HTML
# Retorna também o filme em destaque, que n o caso é o filme mais novo na plataforma
def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8] # Lista todos os filmes do banco, ordenados de forma decrescente pela datra de criação (-data_criacao) e limitando a 8 filmes
    if lista_filmes:
        filme_destaque = Filme.objects.all().order_by('-data_criacao')[0] # Mesmo filtro utilizado para trazer os filmes mais recentes, porem pegando apenas o primeiro
    else:
        filme_destaque = None
    return {'lista_filmes_recentes': lista_filmes, 'filme_destaque': filme_destaque} # Sempre será retornad um dicionário, nesse caso com dois itens


# Função que retorna a lista de filmes mais vistos 
def lista_filmes_emalta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:8] # Lista todos os filmes do banco, ordenados de forma decrescente pela quantidade de visualizações (-visualizacoes) e limitando a 8 filmes
    return {'lista_filmes_emalta': lista_filmes}