"""
Classe de tests pour les fonctions login, logout, index, showSummary pour vérifier le comportement de l'application Flask.
"""

import pytest


class TestLoginClass:
    """
    Cette classe contient plusieurs méthodes de test pour vérifier le comportement de différentes routes de l'application.
    Attributes:
        client (TestClient): Un client de test Flask pour effectuer des requêtes HTTP.
    """

    @pytest.mark.parametrize("email, expected_status_code", [("kate@shelifts.co.uk", 200), ])
    def test_valid_email(self, client, email, expected_status_code):
        response = client.post('/showSummary', data={'email': email}, follow_redirects=True)
        data = response.data.decode()

        # Vérifie que le code de statut correspond à celui attendu.
        assert response.status_code == expected_status_code

        if email == "kate@shelifts.co.uk":
            # Vérifie que le contenu contient le message attendu pour l'email valide.
            assert f"Welcome, {email}" in data

        print(f"Test '{email}' passed")

    @pytest.mark.parametrize("email, expected_status_code", [("invalid_email", 200), ("", 200), ])
    def test_invalid_email(self, client, email, expected_status_code):
        response = client.post('/showSummary', data={'email': email}, follow_redirects=True)
        data = response.data.decode()

        # Vérifie que le page de résumé renvoie un code 200.
        assert response.status_code == expected_status_code

        if email == "invalid_email":
            # Vérifie que le contenu contient le message d'erreur attendu pour l'email invalide.
            assert "Email invalid" in data
            print(f"Test for '{email}' passed")

        elif email == "":
            assert "Enter your email" in data
            print("Test for empty email passed")

    def test_index(self, client):
        response = client.get('/')
        data = response.data.decode()

        # Vérifie que la page d'accueil renvoie un code 200.
        assert response.status_code == 200

        # Vérifie que le contenu contient le message attendu.
        assert "Welcome to the GUDLFT Registration Portal" in data
        print("Test index passed")

    def test_showSummary(self, client, mocker):
        mocker.patch('server.render_template', return_value="Welcome, {{club['email']}} - {{club['name']}}")
        response = client.get('/showSummary')
        data = response.data.decode()

        # Vérifie que la page d'accueil renvoie un code 200.
        assert response.status_code == 200

        # Vérifie que le contenu contient le message attendu.
        assert "Welcome, {{club['email']}} - {{club['name']}}" in data
        print("Test showSummary passed")

    def test_logout(self, client):
        response = client.get('/logout')

        # Vérifiez que le client est redirigé (code 302).
        assert response.status_code == 302
        print("Test logout passed")
