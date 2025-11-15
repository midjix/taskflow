# Test simple pour vérifier que l'application se construit
def test_app_creation(client): # Vous devrez configurer un 'client' de test via pytest-flask
     assert client is not None

# Test que la page d'accueil renvoie un code 200 (OK)
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200