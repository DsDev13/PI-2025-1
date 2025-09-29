from .models import Anuncio, Mensagem
from django.contrib.auth.models import User
# Chat de mensagens entre interessados e criador do anúncio
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def chat_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)
    mensagens = Mensagem.objects.filter(anuncio=anuncio).order_by('data_envio')
    if request.method == 'POST':
        texto = request.POST.get('texto')
        destinatario_id = request.POST.get('destinatario_id')
        if texto and destinatario_id:
            destinatario = User.objects.get(id=destinatario_id)
            Mensagem.objects.create(
                anuncio=anuncio,
                remetente=request.user,
                destinatario=destinatario,
                texto=texto
            )
            return redirect('chat_anuncio', anuncio_id=anuncio.id)

    # Se o criador do anúncio está logado, ele pode escolher para quem responder (lista de interessados)
    interessados = None
    destinatario = None
    if request.user == anuncio.usuario:
        # Buscar todos os usuários que já enviaram mensagem para este anúncio, exceto o próprio criador
        interessados = User.objects.filter(mensagens_enviadas__anuncio=anuncio).exclude(id=anuncio.usuario.id).distinct()
    else:
        destinatario = anuncio.usuario

    return render(request, 'apconect/chat_anuncio.html', {
        'anuncio': anuncio,
        'mensagens': mensagens,
        'destinatario': destinatario,
        'interessados': interessados
    })
# Detalhe do anúncio
def anuncio_detalhe(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)
    return render(request, 'apconect/anuncio_detalhe.html', {'anuncio': anuncio})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Anuncio
from .forms import AnuncioForm
from .forms import RegistroUsuarioForm


def home(request):
    anuncios = Anuncio.objects.all().order_by('-data_criacao')  # mostra os mais recentes primeiro
    # Sinalização de mensagens não lidas para o criador do anúncio
    notificacoes = {}
    if request.user.is_authenticated:
        for anuncio in anuncios:
            if anuncio.usuario == request.user:
                # Mensagens recebidas pelo criador do anúncio que ele ainda não respondeu
                novas = Mensagem.objects.filter(anuncio=anuncio, destinatario=request.user).exclude(remetente=request.user).count()
                if novas > 0:
                    notificacoes[anuncio.id] = novas
    return render(request, 'apconect/home.html', {'anuncios': anuncios, 'notificacoes': notificacoes})


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'apconect/cadastro.html', {'form': form})

def filtrar_por_categoria(request, categoria):
    anuncios = Anuncio.objects.filter(categoria=categoria)
    return render(request, 'apconect/home.html', {'anuncios': anuncios})


@login_required
def meus_anuncios(request):
    anuncios = Anuncio.objects.filter(usuario=request.user)
    return render(request, 'apconect/meus_anuncios.html', {'anuncios': anuncios})

@login_required
def criar_anuncio(request):
    if request.method == 'POST':
        form = AnuncioForm(request.POST, request.FILES)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.usuario = request.user
            anuncio.save()
            return redirect('meus_anuncios')  # ou redireciona para 'home'
    else:
        form = AnuncioForm()
    return render(request, 'apconect/criar_anuncio.html', {'form': form})

# Editar anúncio
@login_required
def editar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id, usuario=request.user)
    if request.method == 'POST':
        form = AnuncioForm(request.POST, request.FILES, instance=anuncio)
        if form.is_valid():
            form.save()
            return redirect('meus_anuncios')
    else:
        form = AnuncioForm(instance=anuncio)
    return render(request, 'apconect/editar_anuncio.html', {'form': form})

# Deletar anúncio
@login_required
def deletar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id, usuario=request.user)
    if request.method == 'POST':
        anuncio.delete()
        return redirect('meus_anuncios')
    return render(request, 'apconect/deletar_anuncio.html', {'anuncio': anuncio})
