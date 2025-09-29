# Usa uma imagem base oficial do Python, leve e otimizada
FROM python:3.12-slim

# Exibe logs do Python em tempo real
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes e PostgreSQL
RUN apt-get update && \
    apt-get install -y libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install --no-cache-dir poetry

# Copia os arquivos de dependência do Poetry
COPY pyproject.toml poetry.lock /app/

# Configura o Poetry para não criar virtualenvs e instala dependências
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi

# Copia todo o código da aplicação
COPY . /app/

# Expõe a porta padrão do Django
EXPOSE 8000

# Define o comando padrão para iniciar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
