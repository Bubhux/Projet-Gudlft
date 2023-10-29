"""
Classe de tests pour la fonction purchasePlaces pour vérifier le comportement de l'application Flask.
"""

import pytest

from pytest_mock import mocker
from tests.conftest import client
from server import CompetitionFullException, InvalidPlacesException, NotEnoughPointsException, MaximumPlacesException


class TestPurchasePlacesClass:
    """
    Cette classe contient plusieurs méthodes de test pour vérifier le comportement de différentes actions de la fonction purchasePlaces.
    Attributes:
        client (TestClient): Un client de test Flask pour effectuer des requêtes HTTP.
    """

    @pytest.fixture
    def test_competitions(self):
        competitions = [
            {
                "name": "Spring Festival",
                "date": "2024-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13"
            },
            {
                "name": "Atomic Pro",
                "date": "2024-10-22 13:30:00",
                "numberOfPlaces": "0"
            }
        ]
        return competitions

    @pytest.fixture
    def test_clubs(self):
        clubs = [
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
        ]
        return clubs

    @pytest.mark.parametrize("competition_index, club_index", [(0, 1)])
    def test_purchase_places_not_enough_points(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="You do not have enough points to make this booking.")

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 5
        }, follow_redirects=True)

        # Vérification du message d'exception dans la réponse
        assert "You do not have enough points to make this booking." in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    @pytest.mark.parametrize("competition_index, club_index", [(1, 1)])
    def test_purchase_places_competition_not_found(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="Competition not found.")

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 3
        }, follow_redirects=True)

        # Vérification du message d'exception dans la réponse
        assert "Competition not found." in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    @pytest.mark.parametrize("competition_index, club_index", [(1, 1)])
    def test_purchase_places_competition_passed(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="The competition has already passed.")

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 2
        }, follow_redirects=True)

        # Vérification du message d'exception dans la réponse
        assert "The competition has already passed." in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    @pytest.mark.parametrize("competition_index, club_index", [(2, 1)])
    def test_purchase_places_competition_full(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="The competition is already full.")

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 3
        }, follow_redirects=True)

        # Vérification du message d'exception dans la réponse
        assert "The competition is already full." in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    @pytest.mark.parametrize("competition_index, club_index", [(2, 1)])
    def test_purchase_places_invalid_places(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="Please enter a valid number for places.")

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 0
        }, follow_redirects=True)

        # Vérification du message d'exception dans la réponse
        assert "Please enter a valid number for places." in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    @pytest.mark.parametrize("competition_index, club_index", [(0, 2)])
    def test_purchase_places_maximum_places(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="You can book a maximum of 12 athletes at once.")

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 10
        }, follow_redirects=True)

        # Vérification du message d'exception dans la réponse
        assert "You can book a maximum of 12 athletes at once." in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    @pytest.mark.parametrize("competition_index, club_index", [(0, 0)])
    def test_purchase_places_successful_booking(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="Great-booking complete!")

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 10
        }, follow_redirects=True)

        # Vérification du message d'exception dans la réponse
        assert "Great-booking complete!" in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    @pytest.mark.parametrize("competition_index, club_index", [(0, 0)])
    def test_purchase_places_update_points(self, client, competition_index, club_index, test_competitions, test_clubs, mocker):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="Great-booking complete!")

        places_input = "5"

        # Accés aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Convertir les données du club et de la compétition en entiers
        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])

        # Vérifie si l'utilisateur a suffisamment de points
        placesRequired = int(places_input)
        if club_points < placesRequired:
            with pytest.raises(NotEnoughPointsException):
                # Effectue la réservation
                competition_places -= placesRequired
                club_points -= placesRequired
        else:
            # Effectue la réservation
            competition_places -= placesRequired
            club_points -= placesRequired

        # Mettre à jour les valeurs dans les dictionnaires
        competition['numberOfPlaces'] = str(competition_places)
        club['points'] = str(club_points)

        # Appel de la route qui déclenchera l'exception
        response = client.post('/purchasePlaces', data={
            "club": club['name'],
            "competition": competition['name'],
            "places": 5
        }, follow_redirects=True)

        # Vérifie que les valeurs ont été mises à jour correctement
        assert competition['numberOfPlaces'] == "20"
        assert club['points'] == "8"

        # Vérification du message d'exception dans la réponse
        assert "Great-booking complete!" in response.data.decode()
        assert response.status_code == 200
        print(response.data.decode())

    def test_competition_full_exception(self, client, mocker):
        # Mocker loadClubs et loadCompetitions pour renvoyer des données spécifiques
        mocker.patch('server.loadClubs', return_value=[
            {
                "name": "Test Club",
                "email": "test@test.com",
                "points": "10"
            }
        ])
        mocker.patch('server.loadCompetitions', return_value=[
            {
                "name": "Test Competition",
                "date": "2024-01-01 10:00:00",
                "numberOfPlaces": "0"
            }
        ])

        # Utilise l'objet client Flask pour effectuer la requête POST
        response = client.post('/purchasePlaces', data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 3
        }, follow_redirects=True)

        # Vérifie que l'exception a été levée correctement
        assert "The competition is already full." in response.data.decode()
        assert response.status_code == 200

    def test_competition_maximum_places_exception(self, client, mocker):
        # Mocker loadClubs et loadCompetitions pour renvoyer des données spécifiques
        mocker.patch('server.loadClubs', return_value=[
            {
                "name": "Test Club",
                "email": "test@test.com",
                "points": "15"
            }
        ])
        mocker.patch('server.loadCompetitions', return_value=[
            {
                "name": "Test Competition",
                "date": "2024-01-01 10:00:00",
                "numberOfPlaces": "20"
            }
        ])

        # Utilise l'objet client Flask pour effectuer la requête POST
        response = client.post('/purchasePlaces', data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 13
        }, follow_redirects=True)

        # Vérifie que l'exception a été levée correctement
        assert "You can book a maximum of 12 athletes at once." in response.data.decode()
        assert response.status_code == 200

    def test_invalid_places_exception(self, client, mocker):
        # Mocker loadClubs et loadCompetitions pour renvoyer des données spécifiques
        mocker.patch('server.loadClubs', return_value=[
            {
                "name": "Test Club",
                "email": "test@test.com",
                "points": "10"
            }
        ])
        mocker.patch('server.loadCompetitions', return_value=[
            {
                "name": "Test Competition",
                "date": "2024-01-01 10:00:00",
                "numberOfPlaces": "10"
            }
        ])

        # Utilise l'objet client Flask pour effectuer la requête POST
        response = client.post('/purchasePlaces', data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": -3
        }, follow_redirects=True)
        assert "Please enter a valid number for places." in response.data.decode()
        assert response.status_code == 200

        # Utilise l'objet client Flask pour effectuer la requête POST
        response = client.post('/purchasePlaces', data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": "abc"
        }, follow_redirects=True)
        assert "Please enter a valid number for places." in response.data.decode()
        assert response.status_code == 200

        # Utilise l'objet client Flask pour effectuer la requête POST
        response = client.post('/purchasePlaces', data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": ""
        }, follow_redirects=True)
        assert "Please enter a valid number for places." in response.data.decode()
        assert response.status_code == 200

    def test_not_enough_points_exception(self, client, mocker):
        # Mocker loadClubs et loadCompetitions pour renvoyer des données spécifiques
        mocker.patch('server.loadClubs', return_value=[
            {
                "name": "Test Club",
                "email": "test@test.com",
                "points": "10"
            }
        ])
        mocker.patch('server.loadCompetitions', return_value=[
            {
                "name": "Test Competition",
                "date": "2024-01-01 10:00:00",
                "numberOfPlaces": "10"
            }
        ])

        # Utilise l'objet client Flask pour effectuer la requête POST
        response = client.post('/purchasePlaces', data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 15
        }, follow_redirects=True)
        assert "You do not have enough points to make this booking." in response.data.decode()
        assert response.status_code == 200

    def test_successful_reservation_and_dictionaries_update(self, client, mocker):
        # Mocker loadClubs et loadCompetitions pour renvoyer des données spécifiques
        loadClubs_mock = mocker.patch('server.loadClubs', return_value=[
            {
                "name": "Test Club",
                "email": "test@test.com",
                "points": "10"
            }
        ])
        loadCompetitions_mock = mocker.patch('server.loadCompetitions', return_value=[
            {
                "name": "Test Competition",
                "date": "2024-01-01 10:00:00",
                "numberOfPlaces": "25"
            }
        ])

        # Utilise l'objet client Flask pour effectuer la requête POST
        response = client.post('/purchasePlaces', data={
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 5
        }, follow_redirects=True)

        assert "Great-booking complete!" in response.data.decode()
        assert response.status_code == 200

        # Vérifie que les valeurs ont été mises à jour correctement
        competition_data = loadCompetitions_mock.return_value[0]
        club_data = loadClubs_mock.return_value[0]

        assert competition_data['numberOfPlaces'] == "20"
        assert club_data['points'] == "5"
