from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apconect import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cadastro/', views.registrar_usuario, name='cadastro'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('meus-anuncios/', views.meus_anuncios, name='meus_anuncios'),
    path('criar-anuncio/', views.criar_anuncio, name='criar_anuncio'),
    path('categoria/<str:categoria>/', views.filtrar_por_categoria, name='filtrar_por_categoria'),
    path('editar/<int:anuncio_id>/', views.editar_anuncio, name='editar_anuncio'),
    path('deletar/<int:anuncio_id>/', views.deletar_anuncio, name='deletar_anuncio'),
]

# Adicione essa linha para servir arquivos de mídia (imagens dos anúncios)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
