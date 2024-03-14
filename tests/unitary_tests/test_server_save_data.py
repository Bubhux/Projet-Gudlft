"""
Fichier test_server_save_data.py pour effectuer des tests sur les fonctions saveClubs et saveCompetitions.
"""

import json
import pytest

from pytest_mock import mocker
from server import saveClubs, saveCompetitions


# Fonction mockée pour json.dump dans les tests
def mocked_json_dump(data, file, *args, **kwargs):
    """
        Fonction de substitution pour json.dump dans les tests.

        Cette fonction est utilisée pour remplacer json.dump dans les tests unitaires afin de simuler
        son comportement sans effectuer réellement d'opérations de sérialisation.

        Arguments :
            - data : Les données JSON à sérialiser.
            - file : Le fichier ouvert dans lequel les données JSON doivent être écrites.
            - *args : Arguments supplémentaires (non utilisés dans cette fonction).
            - **kwargs : Arguments supplémentaires par mot-clé (non utilisés dans cette fonction).

        Cette fonction ne fait rien et est utilisée uniquement pour empêcher les erreurs lors de l'appel
        de json.dump dans les tests.
    """
    pass


def test_saveClubs(mocker):
    # Crée un mock_open pour simuler l'ouverture du fichier 'clubs.json'
    mock_open = mocker.mock_open()

    # Utilise mocker pour patcher open() avec le mock_open
    mocker.patch('builtins.open', mock_open)

    # Utilise mocker pour patcher json.dump avec votre fonction mockée
    mocker.patch('json.dump', side_effect=mocked_json_dump)

    # Appele la fonction à tester
    saveClubs([])

    # Vérifie que la fonction open a été appelée avec le bon fichier et le bon mode
    mock_open.assert_called_once_with('clubs.json', 'w')

    # Vérifie que json.dump a été appelé avec les données appropriées
    json.dump.assert_called_once_with({'clubs': []}, mock_open(), indent=4)


def test_saveCompetitions(mocker):
    # Crée un mock_open pour simuler l'ouverture du fichier 'competitions.json'
    mock_open = mocker.mock_open()

    # Utilise mocker pour patcher open() avec le mock_open
    mocker.patch('builtins.open', mock_open)

    # Utilise mocker pour patcher json.dump avec votre fonction mockée
    mocker.patch('json.dump', side_effect=mocked_json_dump)

    # Appele la fonction à tester
    saveCompetitions([])

    # Vérifie que la fonction open a été appelée avec le bon fichier et le bon mode
    mock_open.assert_called_once_with('competitions.json', 'w')

    # Vérifie que json.dump a été appelé avec les données appropriées
    json.dump.assert_called_once_with({'competitions': []}, mock_open(), indent=4)
