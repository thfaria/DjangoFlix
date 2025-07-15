# Sempre que uma alteração for feita aqui é necessário rodar o comando:
# python manage.py makemigrations
# python manage.py migrate
# Garantindo que as alterações sejam aplicadas no banco de dados

# Para criar o superuser e acessar o admin:
# python manage.py createsuperuser

from django.db import models # Biblioteca par a criação dos modelos de tabelas
from django.utils import timezone # Biblioteca para manipulação de data/ hora
from django.contrib.auth.models import AbstractUser # Importação do modelo padrão de usuários do Django

# Lista de categorias que serão utilizadas no sistema e na coluna 'categoria' da tabela de Filmes
# Essa lista é de fato uma Tupla de tuplas, onde cada tupla é uma categrua formada pelo valor armazenado no banco e o texto apresentado no sistema
# Nome da lista em MAIUSCULO mostrando que essa é uma variável imutável
LISTA_CATEGORIAS = (
    ('ACAO', 'Ação'),
    ('COMEDIA', 'Comédia'),
    ('DRAMA', 'Drama'),
    ('TERROR', 'Terror'),
    ('SCIFI', 'Ficção Científica'),
    ('DOCUMENTARIO', 'Documentário'),
    ('AVENTURA', 'Aventura'),
)

# Classe (tabela) de Filmes
class Filme(models.Model):
    # Atributos (colunas) da tabela
    titulo = models.CharField(max_length=100) # Título do Filme
    thumb = models.ImageField(upload_to='thumb_filmes') # Imagem de capa do filme (armazenada na pasta thumb_filmes)
    descricao = models.TextField(max_length=600) # Descrição do Filme
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS) # Categoria do filme (recebe a lista de categorias, definida anteriormente, como opção de valores)
    visualizacoes = models.IntegerField(default=0) # Número de visualizações do filme (inicializado com zero)
    data_criacao = models.DateTimeField(default=timezone.now) # Coluna que armazena a data de criação do filme (inicializado com a data atual)

    # Método que retorna o título do filme quando o objeto é 'printado'
    # Por padrão, ao 'printar' um objeto, o Django retorna o objeto em si (Filme object (id) por exemplo)
    # Para retornar algo mais intuitivo, como o título do filme, precisamos sobrescrever o método __str__
    def __str__(self):
        return self.titulo
    
# Class (tabela) de Episódios
class Episodio(models.Model):
    # Atributos (colunas) da tabela
    filme = models.ForeignKey('Filme', related_name='episodios', on_delete=models.CASCADE) # Chave estrangeira ligando os episódios a um filme. Related_name é o nome que será utilizado para acessar os episódios de um filme (ex: filme.episodios.all()). On_delete=models.CASCADE comanda as ações em cima de um episódio em caso de exclusão de um filme.
    titulo = models.CharField(max_length=100) # Título do Episódio
    video = models.URLField() # URL do vídeo do episódio    
    
    # Método que retorna o título do episódio quando o objeto é 'printado'
    def __str__(self):
        return self.titulo
    
# Class (tabela) de Usuários que é uma subclasse de AbstractUser (usuário padrão do Django)
class Usuario(AbstractUser):
    # Aqui incluímos apenas os novos campos, já que os campos padrões (nomne, e-mail, etc) já existem na tabela pafrão dde usuários
    filmes_vistos = models.ManyToManyField('Filme') # Campo de relacionamento N para N com a tabela de Filmes