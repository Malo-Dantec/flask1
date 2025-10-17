import pytest
from monApp import app, db
from monApp.models import Auteur

@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.create_all()
        db.session.add(Auteur(Nom="Victor Hugo"))
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(testapp):
    return testapp.test_client()
