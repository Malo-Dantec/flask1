from monApp.models import Auteur
from monApp import db

def login(client, username, password, next_path):
    return client.post(
        "/login/",
        data={"Login": username, "Password": password, "next": next_path},
        follow_redirects=True
    )

def test_auteur_save_success(client, testapp):
    with testapp.app_context():
        auteur = Auteur(Nom="Ancien Nom")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
    
    login(client, "CDAL", "AIGRE", "/auteur/save/")
    response = client.post(
        "/auteur/save/",
        data={"idA": idA, "Nom": "Alexandre Dumas"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b"Alexandre Dumas" in response.data
    
    with testapp.app_context():
        auteur = Auteur.query.get(idA)
        assert auteur.Nom == "Alexandre Dumas"

def test_auteur_insert_success(client, testapp):
    login(client, "CDAL", "AIGRE", "/auteur/insert/")
    response = client.post(
        "/auteur/insert/",
        data={"Nom": "Nouveau Auteur"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b"Nouveau Auteur" in response.data
    
    with testapp.app_context():
        auteur = Auteur.query.filter_by(Nom="Nouveau Auteur").first()
        assert auteur is not None

def test_auteur_erase_success(client, testapp):
    with testapp.app_context():
        auteur = Auteur(Nom="A Supprimer")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
    
    login(client, "CDAL", "AIGRE", "/auteur/erase/")
    response = client.post(
        "/auteur/erase/",
        data={"idA": idA, "Nom": "A Supprimer"},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    with testapp.app_context():
        auteur = Auteur.query.get(idA)
        assert auteur is None