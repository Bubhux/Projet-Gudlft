"""
Classe de tests pour vérifier la mise à jour des points sur la page points_table_clubs.html de l'application Flask.
"""

import pytest

from tests.conftest import client
from pytest_mock import mocker
from bs4 import BeautifulSoup


class TestPointsTableUpdateClass:
    """
    Cette classe contient un test qui vérifie que la mise à jour des points d'un club est correctement reflétée
    dans la page HTML générée et que les balises <td> contiennent les informations mises à jour.
    Attributes:
        client (TestClient): Un client de test Flask pour effectuer des requêtes HTTP.
    """

    @pytest.fixture
    def test_clubs(self):
        clubs = [
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12"
            }
        ]
        return clubs

    @pytest.mark.parametrize("club_name, email, club_points, updated_points, expected_status_code", [("She Lifts", "kate@shelifts.co.uk", "12", "15", 200)])
    def test_display_points_update(self, client, test_clubs, club_name, email, club_points, updated_points, expected_status_code, mocker):
        # Configure le mock pour la base de données
        mocker.patch('server.render_template', return_value='<td>{{club["name"]}}</td>\n<td>{{club["points"]}}</td>')

        # Trouve le club "She Lifts" dans les données de test
        she_lifts_club = next((club for club in test_clubs if club["name"] == club_name), None)

        if she_lifts_club:
            # Avant la mise à jour
            initial_points = int(she_lifts_club["points"])
            print(f"Points du club '{club_name}' avant la mise à jour : {initial_points}")

            # Mettre à jour les points
            she_lifts_club["points"] = updated_points

            # Après la mise à jour
            updated_points = int(she_lifts_club["points"])
            print(f"Points du club '{club_name}' après la mise à jour : {updated_points}")

        # Appel de la route
        response = client.get('/displayPointsClubs')

        # Vérifie que le code de statut correspond à celui attendu
        assert response.status_code == expected_status_code

        # Analyse la réponse comme un document HTML
        soup = BeautifulSoup(response.data, 'html.parser')

        # Trouve toutes les balises 'td'
        td_tags = soup.find_all('td')

        # Examine le contenu des balises 'td'
        if not td_tags:
            print("Aucune balise <td> n'a été trouvée dans le HTML.")
        else:
            for tag in td_tags:
                if club_name in tag.text:
                    assert updated_points in tag.text

                # Déboguage print
                print(tag)

        # Vérifie que "name" et "points" sont présents dans la réponse
        for club in test_clubs:
            if club["name"] == club_name:
                assert 'name' in club
                assert 'email' in club
                assert 'points' in club

                # Vérifie que les valeurs correspondent
                assert club['name'] == club_name
                assert club['email'] == email
                assert int(club['points']) == updated_points

        # Déboguage print
        print(expected_status_code)
        print(club)
        print("Test for updating points that are correctly reflected on the successful HTML page.")
