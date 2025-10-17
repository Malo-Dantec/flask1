def login(client, username, password, next_path):
    return client.post(
        "/login/",
        data={"Login": username, "Password": password, "next": next_path},
        follow_redirects=True
    )

def test_auteurs_liste(client):
    response = client.get('/auteurs/')
    assert response.status_code == 200
    assert b'Victor Hugo' in response.data

def test_auteurs_liste_search(client):
    response = client.get('/auteurs/?q=Victor')
    assert response.status_code == 200
    assert b'Victor Hugo' in response.data

def test_auteur_view(client):
    response = client.get('/auteurs/1/view/')
    assert response.status_code == 200
    assert b'Victor Hugo' in response.data

def test_auteur_update_before_login(client):
    response = client.get('/auteurs/1/update/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Connexion" in response.data

def test_auteur_update_after_login(client, testapp):
    response = login(client, "CDAL", "AIGRE", "/auteurs/1/update/")
    assert response.status_code == 200
    assert "Modification de l'auteur Victor Hugo".encode() in response.data

def test_auteur_delete_before_login(client):
    response = client.get('/auteurs/1/delete/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Connexion" in response.data

def test_auteur_delete_after_login(client):
    response = login(client, "CDAL", "AIGRE", "/auteurs/1/delete/")
    assert response.status_code == 200
    assert "Suppression de l'auteur Victor Hugo".encode() in response.data

def test_auteur_create_before_login(client):
    response = client.get('/auteur/')
    assert response.status_code == 200
    assert "Creation d'un auteur".encode() in response.data or b"Connexion" in response.data

def test_auteur_create_after_login(client):
    response = login(client, "CDAL", "AIGRE", "/auteur/")
    assert response.status_code == 200
    assert "Creation d'un auteur".encode() in response.data