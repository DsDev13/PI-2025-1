from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Anuncio
from .forms import AnuncioForm
from .forms import RegistroUsuarioForm


def home(request):
    anuncios = Anuncio.objects.all().order_by('-data_criacao')  # mostra os mais recentes primeiro
    return render(request, 'apconect/home.html', {'anuncios': anuncios})


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
