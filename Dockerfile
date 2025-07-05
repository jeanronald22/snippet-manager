# Étape 1 : utiliser une image Python légère
FROM python:3.12-slim

# Étape 2 : installer les paquets système nécessaires à pygraphviz
RUN apt-get update && apt-get install -y \
    graphviz \
    graphviz-dev \
    pkg-config \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Étape 3 : créer le répertoire de travail
WORKDIR /app

# Étape 4 : copier le contenu du projet dans l'image
COPY . .

# Étape 5 : installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 6 : configurer Django
WORKDIR /app/src

# Créer dossier pour collectstatic (même si Render définit STATIC_ROOT)
RUN mkdir -p staticfiles

# Collecte des fichiers statiques
RUN python manage.py collectstatic --no-input

# Migration de la base de données
RUN python manage.py migrate

# Étape 7 : exposer le port 8000 (Render utilisera $PORT)
EXPOSE 8000

# Étape 8 : démarrer le serveur ASGI avec Gunicorn + UvicornWorker
CMD ["gunicorn", "snippet_manager.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
