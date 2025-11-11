# Utiliser une image Python officielle
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier tout le code de l'application
COPY . .

# (Le CMD sera défini dans docker-compose pour plus de flexibilité)