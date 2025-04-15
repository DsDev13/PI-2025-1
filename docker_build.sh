#!/usr/bin/env bash
set -o errexit  # Faz o script falhar se algum comando falhar
set -o pipefail # Faz o script falhar se comandos em pipe falharem
set -o nounset  # Faz o script falhar ao acessar variáveis não definidas

echo "=== Instalando dependências ==="
pip install --upgrade pip
pip install -r requirements.txt

# Configurações do Django
export DJANGO_SETTINGS_MODULE=pi2025.settings

echo "=== Aplicando migrações ==="
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput --clear

echo "=== Verificando arquivos estáticos ==="
if [ -d "staticfiles" ]; then
  echo "✓ Arquivos estáticos coletados com sucesso em staticfiles/"
  echo "  Total de arquivos: $(find staticfiles -type f | wc -l)"
else
  echo "✗ Erro: Pasta staticfiles não foi criada!"
  exit 1
fi

echo "=== Build concluído com sucesso ==="