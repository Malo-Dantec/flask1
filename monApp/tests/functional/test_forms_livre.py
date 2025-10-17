# -*- coding: utf-8 -*-

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

def test_livre_view(client):
    response = client.get('/livres/1/view/')
    assert response.status_code == 200
    assert b'Hugo' in response.data

def test_livre_update_before_login(client):
    response = client.get('/livres/1/update/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Connexion" in response.data

def test_livre_update_after_login(client):
    response = login(client, "CDAL", "AIGRE", "/livres/1/update/")
    assert response.status_code == 200