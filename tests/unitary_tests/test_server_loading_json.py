"""
Classe de tests pour les fonctions loadClubs, loadCompetitions pour vérifier le comportement de l'application Flask.
"""

import pytest

from datetime import datetime
from server import loadClubs, loadCompetitions, load_mock_competitions


class TestLoadingJsonClass:
    """
        Classe de tests pour vérifier le comportement de l'application Flask
        lors du chargement de données depuis des fichiers JSON.

        Attributes:
            client (TestClient): Un client de test Flask pour effectuer des requêtes HTTP.
    """

    @pytest.mark.parametrize("club_data", [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ])
    def test_loading_clubs_json(self, client, club_data):
        # Charge les clubs depuis le fichier JSON
        clubs = loadClubs()

        # Vérifie qu'il y a au moins un club
        assert len(clubs) > 0

        # Vérifie les attributs du club
        for club in clubs:
            assert 'name' in club
            assert 'email' in club
            assert 'points' in club

            # Vérifie si les données du club correspondent aux données fournies
            if club['name'] == club_data['name']:
                assert club['email'] == club_data['email']
                assert club['points'] == club_data['points']

        print("Test for loading clubs passed")

    @pytest.mark.parametrize("competition_data", [
        {
            "name": "Spring Festival",
            "date": "2028-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ])
    def test_loading_competitions_json(self, client, competition_data, mocker):
        # Mock loadCompetitions pour utiliser load_mock_competitions
        mocker.patch('server.loadCompetitions', return_value=load_mock_competitions())

        competitions = load_mock_competitions()
        assert len(competitions) > 0
        for competition in competitions:
            assert 'name' in competition
            assert 'date' in competition
            assert 'numberOfPlaces' in competition
            try:
                datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pytest.fail("Date format is incorrect.")
            try:
                int(competition['numberOfPlaces'])
            except ValueError:
                pytest.fail("numberOfPlaces should be an integer.")
            if competition['name'] == competition_data['name']:
                assert competition['date'] == competition_data['date']
                assert competition['numberOfPlaces'] == competition_data['numberOfPlaces']

        print("Test for loading competitions passed")

    def test_loadClubs_file_not_found(self, client, mocker):
        # Crée un mock pour la fonction open qui lève FileNotError
        mocker.patch('builtins.open', side_effect=FileNotFoundError)

        try:
            clubs = loadClubs()
            # Enregistre un message ou une valeur pour vérifier qu'il renvoie bien None
            assert clubs is None
        except FileNotFoundError:
            # Gére l'erreur ici, par exemple, afficher un message à l'utilisateur
            print("Failed to load the clubs database not found.")

    def test_loadCompetitions_file_not_found(self, client, mocker):
        # Crée un mock pour la fonction open qui lève FileNotError
        mocker.patch('builtins.open', side_effect=FileNotFoundError)

        try:
            competitions = loadCompetitions()
            # Enregistre un message ou une valeur pour vérifier qu'il renvoie bien None
            assert competitions is None
        except FileNotFoundError:
            # Gére l'erreur ici, par exemple, afficher un message à l'utilisateur
            print("Failed to load the competitions database not found.")
