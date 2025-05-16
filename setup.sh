#!/usr/bin/env bash
# Script pour configurer rapidement l'environnement de développement

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer avant de continuer."
    exit 1
fi

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null
then
    echo "⚠️ Docker n'est pas installé. Il est recommandé pour exécuter l'application."
    echo "Vous pouvez l'installer depuis https://www.docker.com/products/docker-desktop"
fi

# Créer un environnement virtuel Python si ce n'est pas déjà fait
if [ ! -d "venv" ]; then
    echo "🔧 Création de l'environnement virtuel Python..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé."
fi

# Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env à partir de env.example..."
    cp env.example .env
    echo "⚠️ N'oubliez pas de remplir le fichier .env avec vos identifiants Reddit."
fi

# Exécuter les tests
echo "🧪 Exécution des tests..."
python tests.py

# Instructions finales
echo ""
echo "🚀 Environnement de développement configuré avec succès !"
echo ""
echo "Pour lancer l'application avec Docker :"
echo "  docker compose up --build"
echo ""
echo "Pour lancer l'application manuellement :"
echo "  source venv/bin/activate  # Si ce n'est pas déjà fait"
echo "  cd app"
echo "  FLASK_APP=main.py flask run"
echo ""
echo "Pour vérifier la configuration :"
echo "  python setup.py"
echo ""
