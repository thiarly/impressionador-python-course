from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

LISTA_CATEGORIAS = (
    ("ANALISE", "Análise"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTAÇÃO", "Apresentação"),
    ("OUTROS", "Outros"),

)

# criar o filme
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=1500)
    categoria = models.CharField(max_length=100, choices=LISTA_CATEGORIAS)
    quantidade_views = models.IntegerField(default=0)
    classificacao = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)
   
    def __str__(self):
        return self.titulo
    

# criar o episódio
class Episodio(models.Model):
    filme = models.ForeignKey(Filme, related_name="episodios", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    video = models.URLField()
    
    def __str__(self):
        return self.filme.titulo + " - " + self.titulo


class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")


    # - Filmes/Séries
    # - thumb
    # - titulo
    # - descrição
    # - categoria
    # - quantidade de views
    # - data da criação
    # - Episodio
    #     - videos
    #     - titulo
# criar os episódios

# criar o usuário