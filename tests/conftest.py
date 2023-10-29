import pytest
import server


@pytest.fixture
def client():
    """
    Fixture pour le client de test Flask.

    Cette fixture permet de créer un client de test Flask pour effectuer des requêtes HTTP
    lors des tests unitaires. Le client est configuré en mode TESTING et gère la libération
    des ressources après l'exécution des tests.

    Returns:
        TestClient: Le client de test Flask.
    """

    app = server.app  # Utilise l'instance d'application Flask de votre application
    app.config['TESTING'] = True  # Configure le mode TESTING

    # Charge les données de compétitions et de clubs
    #app.config['COMPETITIONS'] = server.loadCompetitions()
    #app.config['CLUBS'] = server.loadClubs()

    with app.test_client() as client:
        yield client
