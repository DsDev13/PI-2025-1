from django.db import models
from django.contrib.auth.models import User

CATEGORIAS = [
    ('infra', 'Infraestrutura'),
    ('alimentos', 'Alimentos'),
    ('servicos', 'Serviços'),
    ('vendas', 'Vendas'),
]

class Anuncio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    imagem = models.ImageField(upload_to='anuncios/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.usuario.username})"
