import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Crée et configure une nouvelle instance de l'application pour chaque test."""
    
    # Crée l'application en utilisant la configuration de test
    app = create_app()
    app.config.update({
        "TESTING": True,  # Active le mode "test" de Flask
        "SECRET_KEY": "cle-secrete-de-test",
        # Utilise une base de données en mémoire (rapide et isolée)
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False, # Désactive la sécurité CSRF pour les tests
        "LOGIN_DISABLED": True # Désactive l'obligation de se logger (optionnel)
    })

    # "yield" est la version "return" pour une fixture
    yield app 

    # (Optionnel, mais propre) Nettoyage après le test
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """Fournit un client de test pour l'application."""
    
    return app.test_client()