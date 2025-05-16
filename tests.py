#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour l'application Reddit Cleaner.

Ce module contient des tests unitaires pour les fonctions de l'application.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ajout du répertoire parent au chemin de recherche de modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

class TestRedditCleaner(unittest.TestCase):
    """Tests pour l'application Reddit Cleaner."""

    def setUp(self):
        """Configure l'application pour les tests."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_page(self):
        """Vérifie que la page d'index renvoie un code 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.main.get_all_comments')
    def test_next_comment_empty(self, mock_get_all_comments):
        """Vérifie que next_comment renvoie 'done' quand il n'y a plus de commentaires."""
        # Simulation d'une liste vide de commentaires
        mock_get_all_comments.return_value = []
        
        # Force la réinitialisation de l'index et des commentaires
        import app.main
        app.main.comments = []
        app.main.index = 0
        
        response = self.client.get('/next')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['done'])

    @patch('app.main.delete_comment')
    def test_delete_comment(self, mock_delete_comment):
        """Vérifie que la fonction delete fonctionne correctement."""
        response = self.client.post(
            '/delete',
            json={"id": "test_id"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "deleted"})
        mock_delete_comment.assert_called_once_with("test_id")

if __name__ == '__main__':
    unittest.main()
