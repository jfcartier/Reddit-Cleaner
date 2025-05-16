#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuration de l'application Reddit Cleaner.

Ce script permet de vérifier que l'environnement est correctement configuré
pour exécuter l'application Reddit Cleaner.
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """
    Vérifie que toutes les variables d'environnement nécessaires sont définies.
    
    Returns:
        bool: True si toutes les variables sont définies, False sinon
    """
    required_vars = [
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USERNAME",
        "REDDIT_PASSWORD",
        "REDDIT_USER_AGENT"
    ]
    
    load_dotenv()
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Configuration incomplète. Variables manquantes :")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nAssurez-vous de créer un fichier .env avec toutes les variables requises.")
        print("Vous pouvez vous baser sur env.example pour créer votre fichier .env")
        return False
    
    return True

def check_dependencies():
    """
    Vérifie que toutes les dépendances Python sont installées.
    
    Returns:
        bool: True si toutes les dépendances sont installées, False sinon
    """
    try:
        import flask
        import praw
        return True
    except ImportError as e:
        print(f"⚠️  Dépendance manquante: {e}")
        print("Exécutez 'pip install -r requirements.txt' pour installer les dépendances.")
        return False

if __name__ == "__main__":
    print("🔍 Vérification de la configuration de Reddit Cleaner...")
    
    env_ok = check_environment()
    deps_ok = check_dependencies()
    
    if env_ok and deps_ok:
        print("✅ Configuration correcte ! L'application peut être démarrée.")
        print("   Utilisez 'docker compose up --build' pour lancer l'application.")
    else:
        print("❌ La configuration n'est pas complète. Veuillez corriger les erreurs ci-dessus.")
        sys.exit(1)
