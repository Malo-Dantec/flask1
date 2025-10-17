# -*- coding: utf-8 -*-
from monApp.models import Livre
from monApp import db

def login(client, username, password, next_path):
    return client.post(
        "/login/",
        data={"Login": username, "Password": password, "next": next_path},
        follow_redirects=True
    )

def test_livres_liste(client):
    response = client.get('/livres/')
    assert response.status_code == 200
    assert b'Mis' in response.data

def test_livres_search(client):
    response = client.get('/livres/?q=Mis')
    assert response.status_code == 200
    assert b'Mis' in response.data

def test_livres_search_empty(client):
    response = client.get('/livres/?q=')
    assert response.status_code == 200

def test_livre_view(client):
    response = client.get('/livres/1/view/')
    assert response.status_code == 200
    assert b'Hugo' in response.data

def test_livre_view_not_found(client):
    response = client.get('/livres/999/view/')
    assert response.status_code == 404

def test_livre_update_before_login(client):
    response = client.get('/livres/1/update/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Connexion" in response.data

def test_livre_update_after_login(client):
    login(client, "CDAL", "AIGRE", "/livres/1/update/")
    response = client.get('/livres/1/update/')
    assert response.status_code == 200
    assert b"Modification du livre" in response.data

def test_livre_save_success(client, testapp):
    login(client, "CDAL", "AIGRE", "/livre/save/")
    response = client.post(
        "/livre/save/",
        data={"idL": "1", "titre": "Les Misérables Edition Spéciale", "prix": "19.99"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b"Edition" in response.data
    
    with testapp.app_context():
        livre = Livre.query.get(1)
        assert livre.titre == "Les Misérables Edition Spéciale"
        assert livre.prix == 19.99

def test_livre_save_validation_error(client, testapp):
    login(client, "CDAL", "AIGRE", "/livre/save/")
    response = client.post(
        "/livre/save/",
        data={"idL": "1", "titre": "", "prix": "19.99"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b"Modification du livre" in response.data

def test_livre_save_invalid_price(client, testapp):
    login(client, "CDAL", "AIGRE", "/livre/save/")
    response = client.post(
        "/livre/save/",
        data={"idL": "1", "titre": "Test", "prix": "-5"},
        follow_redirects=True
    )
    
    assert response.status_code == 200