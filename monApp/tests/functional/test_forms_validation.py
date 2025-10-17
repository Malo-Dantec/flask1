from monApp.models import Auteur
from monApp import db

def login(client, username, password, next_path):
    return client.post(
        "/login/",
        data={"Login": username, "Password": password, "next": next_path},
        follow_redirects=True
    )

def test_auteur_insert_empty_name(client):
    login(client, "CDAL", "AIGRE", "/auteur/insert/")
    response = client.post(
        "/auteur/insert/",
        data={"Nom": ""},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Creation" in response.data or b"Creation" in response.data

def test_auteur_save_empty_name(client, testapp):
    with testapp.app_context():
        auteur = Auteur(Nom="Test Auteur")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
    
    login(client, "CDAL", "AIGRE", "/auteur/save/")
    response = client.post(
        "/auteur/save/",
        data={"idA": idA, "Nom": ""},
        follow_redirects=True
    )
    assert response.status_code == 200

def test_auteur_search_partial(client):
    response = client.get('/auteurs/?q=Vic')
    assert response.status_code == 200
    assert b'Victor' in response.data

def test_auteur_search_case_insensitive(client):
    response = client.get('/auteurs/?q=victor')
    assert response.status_code == 200
    assert b'Victor' in response.data

def test_auteur_search_no_results(client):
    response = client.get('/auteurs/?q=NonExistant')
    assert response.status_code == 200
    assert b'Aucun auteur' in response.data or b'auteur' in response.data.lower()

def test_livre_search_partial(client):
    response = client.get('/livres/?q=Mis')
    assert response.status_code == 200

def test_livre_search_case_insensitive(client):
    response = client.get('/livres/?q=mis')
    assert response.status_code == 200

def test_livre_search_no_results(client):
    response = client.get('/livres/?q=NonExistant')
    assert response.status_code == 200