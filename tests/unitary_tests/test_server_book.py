"""
Classe de tests pour la fonction book pour vérifier le comportement de l'application Flask.
"""

import pytest

from flask import url_for


class TestBookClass:
    """
        Cette classe contient plusieurs méthodes de test
        pour vérifier le comportement de différentes actions de l'application.

        Attributes:
            client (TestClient): Un client de test Flask pour effectuer des requêtes HTTP.
    """

    @pytest.fixture
    def test_competitions(self):
        competitions = [
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
    def test_book_competition_and_club_found(
        self,
        client,
        competition_index,
        club_index,
        test_competitions,
        test_clubs,
        mocker
    ):
        # Mock de la fonction 'render_template' pour simuler le comportement de l'application
        mocker.patch('server.render_template', return_value="Places available: 25")

        # Accès aux compétitions et aux clubs directement depuis les objets de fixture
        competition = test_competitions[competition_index]
        club = test_clubs[club_index]

        # Appel de la route qui déclenchera l'exception
        response = client.get(f"/book/{competition['name']}/{club['name']}")

        assert response.status_code == 200
        assert "Places available: 25" in response.data.decode()
        print(response.data.decode())

    def test_book_competition_and_club_not_found(self, client, mocker):
        # Utilise mocker pour simuler les fonctions flash et redirect
        flash_mock = mocker.patch('server.flash')
        redirect_mock = mocker.patch('server.redirect')

        # Accès à une compétition et un club qui ne sont pas dans les fixtures
        competition_name = "Unknown Competition"
        club_name = "Unknown Club"

        # Appel de la route qui déclenchera l'exception
        response = client.get(f"/book/{competition_name}/{club_name}")

        # Vérification que flash et redirect ont été appelés avec les bons arguments
        flash_mock.assert_called_once_with("The competition or club does not exist. Please try again.", 'error')
        redirect_mock.assert_called_once_with(url_for('showSummary'))
        assert response.status_code == 200
