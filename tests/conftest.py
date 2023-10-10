import pytest
import server


@pytest.fixture
def client():
    """
    yield client permet de fournir le client de test Flask créé dans la fixture au test qui dépend de cette fixture.
    En utilisant yield, permet au test d'accéder à client comme un return client,
    laisse pytest gérer la libération des ressources après l'exécution du test.
    """
    app = server.app  # Utilisez l'instance d'application Flask de votre application
    app.config['TESTING'] = True  # Configurez le mode TESTING
    with app.test_client() as client:
        yield client
