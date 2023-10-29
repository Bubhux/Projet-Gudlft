"""
Classe de tests pour vérifier le comportement des exceptions de l'application Flask.
"""

import pytest

from server import (
    CompetitionNotFoundException,
    CompetitionPassedException,
    CompetitionFullException,
    InvalidPlacesException,
    MaximumPlacesException,
    NotEnoughPointsException
)


class TestExceptionClass:
    """
    Classe de tests pour vérifier le comportement de l'application Flask lors de l'utilisation des classes qui gère les exceptions.
    Attributes:
        client (TestClient): Un client de test Flask pour effectuer des requêtes HTTP.
    """

    def test_competition_not_found_exception(self):
        with pytest.raises(CompetitionNotFoundException) as exc_info:
            raise CompetitionNotFoundException()
        assert str(exc_info.value.flash_message) == 'Competition not found.'

    def test_competition_passed_exception(self):
        with pytest.raises(CompetitionPassedException) as exc_info:
            raise CompetitionPassedException()
        assert str(exc_info.value.flash_message) == 'The competition has already passed.'

    def test_competition_full_exception(self):
        with pytest.raises(CompetitionFullException) as exc_info:
            raise CompetitionFullException()
        assert str(exc_info.value.flash_message) == 'The competition is already full.'

    def test_invalid_places_exception(self):
        with pytest.raises(InvalidPlacesException) as exc_info:
            raise InvalidPlacesException()
        assert str(exc_info.value.flash_message) == 'Please enter a valid number for places.'

    def test_maximum_places_exception(self):
        with pytest.raises(MaximumPlacesException) as exc_info:
            raise MaximumPlacesException()
        assert str(exc_info.value.flash_message) == 'You can book a maximum of 12 athletes at once.'

    def test_not_enough_points_exception(self):
        with pytest.raises(NotEnoughPointsException) as exc_info:
            raise NotEnoughPointsException()
        assert str(exc_info.value.flash_message) == 'You do not have enough points to make this booking.'
