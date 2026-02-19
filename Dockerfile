FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 agent && chown -R agent:agent /app

# Changer vers l'utilisateur non-root
USER agent

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV MODEL_NAME=claude-3-5-haiku-20241022

# Point d'entrée: le CLI
ENTRYPOINT ["python", "cli.py"]

# Help par défaut
CMD ["--help"]
