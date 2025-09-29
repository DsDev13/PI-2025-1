
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
    endereco_exibicao = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Opcional. Informe um endereço comercial se desejar exibir no anúncio. Não informe endereço residencial."
    )

    def __str__(self):
        return f"{self.titulo} ({self.usuario.username})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)



    def __str__(self):
        return self.user.username


# Chat entre interessados e criador do anúncio
class Mensagem(models.Model):
    anuncio = models.ForeignKey('Anuncio', on_delete=models.CASCADE, related_name='mensagens')
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username} ({self.anuncio.titulo})"

    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username} ({self.anuncio.titulo})"
