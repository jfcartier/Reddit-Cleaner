#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application principale pour Reddit Cleaner.

Ce module est le point d'entrée de l'application Flask qui permet
de parcourir et supprimer des commentaires Reddit.
"""

from flask import Flask, render_template, jsonify, request
from reddit_client import get_all_comments, delete_comment

# Initialisation de l'application Flask
app = Flask(__name__)
comments = get_all_comments()
index = 0

@app.route("/")
def index_page():
    """
    Route principale qui affiche l'interface utilisateur.
    
    Returns:
        str: Template HTML rendu
    """
    return render_template("index.html")

@app.route("/next", methods=["GET"])
def next_comment():
    """
    Route qui renvoie le prochain commentaire à évaluer.
    
    Returns:
        dict: JSON contenant les détails du commentaire ou un statut 'done' si tous
              les commentaires ont été parcourus.
    """
    global index
    if index >= len(comments):
        return jsonify({"done": True})
    c = comments[index]
    index += 1
    
    # Récupération des informations du subreddit
    subreddit = c.subreddit
    
    # Récupération explicite du thumbnail et vérification
    subreddit_icon = None
    try:
        if hasattr(subreddit, 'icon_img') and subreddit.icon_img:
            subreddit_icon = subreddit.icon_img
        elif hasattr(subreddit, 'community_icon') and subreddit.community_icon:
            subreddit_icon = subreddit.community_icon
    except Exception as e:
        print(f"Erreur lors de la récupération de l'icône: {e}")
    
    # Récupération du titre du subreddit
    subreddit_title = getattr(subreddit, 'display_name', "")
    if not subreddit_title:
        subreddit_title = getattr(subreddit, 'name', "")
    
    # Récupération du lien et titre du post
    post_url = ""
    post_title = ""
    try:
        if hasattr(c, 'permalink'):
            post_url = f"https://reddit.com{c.permalink}"
        
        # Récupération du titre du post
        if hasattr(c, 'submission'):
            post_title = getattr(c.submission, 'title', "")
            if not post_url and hasattr(c.submission, 'permalink'):
                post_url = f"https://reddit.com{c.submission.permalink}"
    except Exception as e:
        print(f"Erreur lors de la récupération des infos du post: {e}")
    
    # Récupération du score (upvotes)
    ups = 0
    try:
        ups = getattr(c, 'score', 0)
    except:
        ups = 0
    
    # Ajout de logs pour déboguer
    print(f"Subreddit: {subreddit_title}, Icon: {subreddit_icon is not None}, Ups: {ups}")
    
    return jsonify({
        "id": c.id,
        "body": c.body,
        "subreddit": subreddit_title,
        "subreddit_title": subreddit_title,
        "subreddit_icon": subreddit_icon if subreddit_icon else "",
        "created_utc": c.created_utc,
        "ups": ups,
        "post_url": post_url,
        "post_title": post_title
    })

@app.route("/delete", methods=["POST"])
def delete():
    """
    Route pour supprimer un commentaire Reddit.
    
    La requête POST doit contenir un JSON avec l'ID du commentaire à supprimer.
    
    Returns:
        dict: JSON contenant le statut de l'opération
    """
    data = request.json
    delete_comment(data["id"])
    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    # Démarrage de l'application en mode développement
    app.run(debug=True, host="0.0.0.0")
