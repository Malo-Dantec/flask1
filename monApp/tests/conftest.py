import pytest
from monApp import app, db
from monApp.models import Auteur, Livre, User
from hashlib import sha256

@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.create_all()
        
        # Ajouter un auteur de test
        auteur = Auteur(Nom="Victor Hugo")
        db.session.add(auteur)
        db.session.commit()
        
        # Ajouter un livre de test
        livre = Livre(
            titre="Les Misérables",
            auteur=auteur,
            prix=15.99,
            url="http://example.com/miserables",
            img="miserables.jpg"
        )
        db.session.add(livre)
        
        # Ajouter un utilisateur de test
        m = sha256()
        m.update("AIGRE".encode())
        user = User(Login="CDAL", Password=m.hexdigest())
        db.session.add(user)
        
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(testapp):
    return testapp.test_client()