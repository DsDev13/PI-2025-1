# Estágio de construção
FROM python:3.12-slim as builder

# Instala dependências de compilação
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Estágio final
FROM python:3.12-slim

# Instala apenas as dependências de runtime do PostgreSQL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN useradd -m appuser && \
    mkdir -p /app/staticfiles && \
    chown appuser:appuser /app /app/staticfiles

WORKDIR /app
USER appuser

# Copia as dependências instaladas
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Configura o PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PYTHONPATH="/home/appuser/.local/lib/python3.12/site-packages"

# Variáveis do Django
ENV DJANGO_SETTINGS_MODULE=pi2025.settings

# Porta exposta
EXPOSE 8000

# Comando de execução
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pi2025.wsgi:application"]