#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Reddit pour l'application Reddit Cleaner.

Ce module gère les interactions avec l'API Reddit via PRAW.
Il permet de récupérer et de supprimer les commentaires de l'utilisateur.
"""

import praw
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Initialisation du client Reddit avec les identifiants de l'utilisateur
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

def get_all_comments():
    """
    Récupère tous les commentaires de l'utilisateur connecté.
    
    Returns:
        list: Liste des commentaires triés du plus ancien au plus récent.
    """
    # On récupère les commentaires du plus ancien au plus récent
    return list(reversed(list(reddit.redditor(os.getenv("REDDIT_USERNAME")).comments.new(limit=None))))

def delete_comment(comment_id):
    """
    Supprime un commentaire Reddit spécifié par son ID.
    
    Args:
        comment_id (str): L'identifiant unique du commentaire à supprimer.
        
    Returns:
        None
    """
    comment = reddit.comment(id=comment_id)
    comment.delete()
